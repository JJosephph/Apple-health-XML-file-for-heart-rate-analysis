import base64
import os
import time

import matplotlib
from flask import Flask, render_template, make_response, request, send_file, jsonify
import xml.etree.ElementTree as ET
from statistics import mean
import matplotlib.pyplot as plt
import io
import pdfkit
import datetime
import numpy as np

app = Flask(__name__)


matplotlib.use('Agg')  # 这一行告诉Matplotlib使用Agg后端，而不是Tkinter


def parse_xml(file_path):
    tree = ET.parse(file_path)
    records = tree.findall('.//Record[@type="HKQuantityTypeIdentifierHeartRate"]')

    heart_rates = []
    date_heart_rates = {}

    for record in records:
        timestamp_str = record.attrib['creationDate']
        timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S %z')
        date = timestamp.strftime('%Y-%m-%d')
        heart_rate = int(record.attrib['value'])

        heart_rates.append(heart_rate)

        if date in date_heart_rates:
            date_heart_rates[date].append(heart_rate)
        else:
            date_heart_rates[date] = [heart_rate]

    return heart_rates, date_heart_rates


# 分析心跳数据
def analyze_heart_rate(heart_rates):
    average_heart_rate = mean(heart_rates)
    max_heart_rate = max(heart_rates)
    min_heart_rate = min(heart_rates)
    total_heart_beats = sum(heart_rates)
    return average_heart_rate, max_heart_rate, min_heart_rate, total_heart_beats


def create_chart(heart_rates, chart_type='line', title='Heart Rate Over Time'):
    plt.clf()  # Clear the current figure (if any) before creating a new chart
    plt.figure(figsize=(8, 6))

    if chart_type == 'line':
        plt.plot(heart_rates)
        plt.title(title)
        plt.xlabel('Record Index')
        plt.ylabel('Heart Rate (count/min)')
        plt.grid(True)
    elif chart_type == 'pie':
        plt.pie(heart_rates, labels=[f'Record {i + 1}' for i in range(len(heart_rates))], autopct='%1.1f%%',
                startangle=140)
        plt.title(title)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the chart to a temporary file
    temp_file_path = f'temp_chart_{chart_type}.png'
    plt.savefig(temp_file_path, format='png')
    plt.close()  # Close the figure to release resources

    # Read the saved chart file and encode to base64
    with open(temp_file_path, 'rb') as temp_file:
        chart_image = io.BytesIO(temp_file.read())

    # Remove the temporary file
    os.remove(temp_file_path)

    chart_image.seek(0)
    return chart_image


# Flask路由
@app.route('/')
def index():
    # 解析 XML 文件获取健康数据
    file_path = './导出.xml'  # 替换为你的XML文件路径
    heart_rates, date_heart_rates = parse_xml(file_path)

    # 获取健康数据
    average_heart_rate, max_heart_rate, min_heart_rate, total_heart_beats = analyze_heart_rate(heart_rates)

    return render_template('index.html',
                           average_heart_rate=average_heart_rate,
                           max_heart_rate=max_heart_rate,
                           min_heart_rate=min_heart_rate,
                           total_heart_beats=total_heart_beats)

@app.route('/line_chart')
def line_chart():
    file_path = './导出.xml'  # 替换为你的XML文件路径
    heart_rates, date_heart_rates = parse_xml(file_path)
    chart_image = create_chart(heart_rates, chart_type='line', title='Heart Rate Over Time')
    chart_base64 = base64.b64encode(chart_image.read()).decode('utf-8')
    return render_template('line_chart.html', chart_image=chart_base64)


@app.route('/daily_average_chart')
def daily_average_chart():
    file_path = './导出.xml'  # 替换为你的XML文件路径
    heart_rates, date_heart_rates = parse_xml(file_path)

    # 获取日期和平均心率数据
    dates = list(date_heart_rates.keys())
    daily_average_heart_rates = [mean(date_heart_rates[date]) for date in dates]

    # 绘制折线图
    chart_image = create_daillyChart(dates, daily_average_heart_rates, chart_type='line', title='Daily Average Heart Rate')
    chart_base64 = base64.b64encode(chart_image.read()).decode('utf-8')
    return render_template('daily_average_chart.html', chart_image=chart_base64)

def create_daillyChart(x_values, y_values, chart_type='line', title='Heart Rate Over Time'):
    plt.clf()  # Clear the current figure (if any) before creating a new chart
    plt.figure(figsize=(8, 6))

    if chart_type == 'line':
        plt.plot(x_values, y_values)
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Daily Average Heart Rate (count/min)')
        plt.grid(True)
    elif chart_type == 'pie':
        plt.pie(y_values, labels=x_values, autopct='%1.1f%%', startangle=140)
        plt.title(title)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the chart to a temporary file
    temp_file_path = f'temp_chart_{chart_type}.png'
    plt.savefig(temp_file_path, format='png')
    plt.close()  # Close the figure to release resources

    # Read the saved chart file and encode to base64
    with open(temp_file_path, 'rb') as temp_file:
        chart_image = io.BytesIO(temp_file.read())

    # Remove the temporary file
    os.remove(temp_file_path)

    chart_image.seek(0)
    return chart_image
@app.route('/pie_chart')
def pie_chart():
    file_path = './导出.xml'  # 替换为你的XML文件路径
    heart_rates, date_heart_rates = parse_xml(file_path)

    # 获取日期和平均心率数据
    dates = list(date_heart_rates.keys())
    daily_average_heart_rates = [mean(date_heart_rates[date]) for date in dates]

    # 获取每日平均心率的分布
    unique_daily_average_heart_rates = sorted(set(daily_average_heart_rates))
    daily_average_distribution = [daily_average_heart_rates.count(rate) for rate in unique_daily_average_heart_rates]

    # 绘制饼图
    chart_image = create_pieChart(unique_daily_average_heart_rates, daily_average_distribution, chart_type='pie',
                                  title='Daily Average Heart Rate Distribution')
    chart_base64 = base64.b64encode(chart_image.read()).decode('utf-8')
    return render_template('pie_chart.html', chart_image=chart_base64)
# 在 create_chart 函数中修改
def create_pieChart(x_values, y_values, chart_type='line', title='Heart Rate Over Time'):
    plt.clf()  # Clear the current figure (if any) before creating a new chart
    plt.figure(figsize=(8, 6))

    if chart_type == 'line':
        plt.plot(x_values, y_values)
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Heart Rate (count/min)')
        plt.grid(True)
    elif chart_type == 'pie':
        plt.pie(y_values, labels=x_values, autopct='%1.1f%%', startangle=140)
        plt.title(title)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the chart to a temporary file
    temp_file_path = f'temp_chart_{chart_type}.png'
    plt.savefig(temp_file_path, format='png')
    plt.close()  # Close the figure to release resources

    # Read the saved chart file and encode to base64
    with open(temp_file_path, 'rb') as temp_file:
        chart_image = io.BytesIO(temp_file.read())

    # Remove the temporary file
    os.remove(temp_file_path)

    chart_image.seek(0)
    return chart_image

# 导出为PDF
@app.route('/all_chart')
def export_pdf():
    file_path = './导出.xml'
    heart_rates, date_heart_rates = parse_xml(file_path)

    # 创建折线图
    line_chart_image = create_chart(heart_rates, chart_type='line', title='Heart Rate Over Time')
    line_chart_base64 = base64.b64encode(line_chart_image.read()).decode('utf-8')
    heart_rates, date_heart_rates = parse_xml(file_path)

    # 获取日期和平均心率数据
    dates = list(date_heart_rates.keys())
    daily_average_heart_rates = [mean(date_heart_rates[date]) for date in dates]
    # 创建每日平均心率的折线图
    daily_average_heart_rates = [mean(date_heart_rates[date]) for date in date_heart_rates]
    daily_average_chart_image = create_daillyChart(dates, daily_average_heart_rates, chart_type='line', title='Daily Average Heart Rate')
    daily_average_chart_base64 = base64.b64encode(daily_average_chart_image.read()).decode('utf-8')
    # 获取日期和平均心率数据
    dates = list(date_heart_rates.keys())
    daily_average_heart_rates = [mean(date_heart_rates[date]) for date in dates]

    # 获取每日平均心率的分布
    unique_daily_average_heart_rates = sorted(set(daily_average_heart_rates))
    daily_average_distribution = [daily_average_heart_rates.count(rate) for rate in unique_daily_average_heart_rates]
    # 创建心率分布的饼图
    heart_rate_distribution = np.histogram(heart_rates, bins=range(40, 201, 10))[0]
    pie_chart_image = create_pieChart(unique_daily_average_heart_rates, daily_average_distribution, chart_type='pie',
                                  title='Daily Average Heart Rate Distribution')
    pie_chart_base64 = base64.b64encode(pie_chart_image.read()).decode('utf-8')

    # 心率建议
    heart_rate_advice = get_heart_rate_advice(mean(heart_rates))

    return render_template(
        'all_chart.html',
        line_chart_image=line_chart_base64,
        daily_average_chart_image=daily_average_chart_base64,
        pie_chart_image=pie_chart_base64,
        heart_rate_advice=heart_rate_advice
    )


def get_heart_rate_advice(average_heart_rate):
    if average_heart_rate < 60:
        return "您的平均心率低于正常范围。建议咨询医疗专业人士。"
    elif average_heart_rate > 100:
        return "您的平均心率高于正常范围。建议咨询医疗专业人士。"
    else:
        return "您的平均心率处于正常范围内。继续保持良好状态！"


UPLOAD_FOLDER = './uploads'  # 上传文件保存的文件夹
ALLOWED_EXTENSIONS = {'xml'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_xml', methods=['POST'])
def upload_xml():
    uploaded_file = request.files['xmlFile']

    if uploaded_file.filename == '' or not allowed_file(uploaded_file.filename):
        return jsonify({'error': 'Invalid file or file type. Please upload a valid XML file.'})

    # 保存上传的文件为“导出.xml”
    file_path = './导出.xml'  # 替换为您的项目路径
    uploaded_file.save(file_path)

    # 返回上传成功的 JSON 响应
    response = {'message': 'File uploaded successfully'}
    return jsonify(response)

@app.route('/download_pdf')
def download_pdf():
    file_path = './导出.xml'
    heart_rates, date_heart_rates = parse_xml(file_path)

    # 创建折线图
    line_chart_image = create_chart(heart_rates, chart_type='line', title='Heart Rate Over Time')
    line_chart_base64 = base64.b64encode(line_chart_image.read()).decode('utf-8')
    heart_rates, date_heart_rates = parse_xml(file_path)

    # 获取日期和平均心率数据
    dates = list(date_heart_rates.keys())
    daily_average_heart_rates = [mean(date_heart_rates[date]) for date in dates]
    # 创建每日平均心率的折线图
    daily_average_heart_rates = [mean(date_heart_rates[date]) for date in date_heart_rates]
    daily_average_chart_image = create_daillyChart(dates, daily_average_heart_rates, chart_type='line',
                                                  title='Daily Average Heart Rate')
    daily_average_chart_base64 = base64.b64encode(daily_average_chart_image.read()).decode('utf-8')
    # 获取日期和平均心率数据
    dates = list(date_heart_rates.keys())
    daily_average_heart_rates = [mean(date_heart_rates[date]) for date in dates]

    # 获取每日平均心率的分布
    unique_daily_average_heart_rates = sorted(set(daily_average_heart_rates))
    daily_average_distribution = [daily_average_heart_rates.count(rate) for rate in unique_daily_average_heart_rates]
    # 创建心率分布的饼图
    heart_rate_distribution = np.histogram(heart_rates, bins=range(40, 201, 10))[0]
    pie_chart_image = create_pieChart(unique_daily_average_heart_rates, daily_average_distribution, chart_type='pie',
                                      title='Daily Average Heart Rate Distribution')
    pie_chart_base64 = base64.b64encode(pie_chart_image.read()).decode('utf-8')

    # 心率建议
    heart_rate_advice = get_heart_rate_advice(mean(heart_rates))

    # 生成 HTML 内容并保存到文件
    html_content = render_template(
        'all_chart.html',
        line_chart_image=line_chart_base64,
        daily_average_chart_image=daily_average_chart_base64,
        pie_chart_image=pie_chart_base64,
        heart_rate_advice=heart_rate_advice
    )

    # 创建一个以年月日为名的文件夹
    today_folder = time.strftime("%Y%m%d")
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], today_folder)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 为了确保文件名的唯一性，给文件名增加时间戳
    timestamped_filename = f"{time.strftime('%Y%m%d%H%M%S')}_all_chart.html"
    html_file_path = os.path.join(folder_path, timestamped_filename)

    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    # 返回生成的 PDF 文件
    return send_file(html_file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)