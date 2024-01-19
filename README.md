# 健康数据分析应用

这个应用通过解析上传的健康数据 XML 文件，提供了对心率数据的分析和可视化。用户可以上传文件，查看心率随时间变化的折线图、每日平均心率折线图和心率分布饼图。同时，还支持将综合图表导出为 PDF 文件。

## 功能特点

- 数据分析：平均心率、最高心率、最低心率、总心跳数等统计。
- 可视化图表：折线图、每日平均心率折线图和心率分布饼图。
- PDF 导出：将综合图表导出为 PDF 文件。
- 动态弹窗：使用 SweetAlert2 实现上传成功和失败的动态弹窗。

## 如何运行

1. 安装依赖：`pip install Flask matplotlib pdfkit numpy`.
2. 运行应用：`python app.py`.
3. 访问 `http://localhost:5000` 查看应用。

## 项目结构

- `app.py`: 主程序文件，包含 Flask 应用的路由和核心功能实现。
- `templates/`: 存放 HTML 模板文件。
- `uploads/`: 存放生成的 PDF 文件的文件夹。

## 注意事项

- 请确保上传的文件为 XML 格式的健康数据文件。
- 在运行应用之前，检查网络连接以获取 SweetAlert2 的 CDN 资源。

![image](https://github.com/JJosephph/Apple-health-XML-file-for-heart-rate-analysis/assets/124876944/20dfdb40-e1c7-46a5-83e8-2f5b25359eed)![1705649133236](https://github.com/JJosephph/Apple-health-XML-file-for-heart-rate-analysis/assets/124876944/1f6405eb-f733-4ec4-ab97-06bac0ed8674)
![image](https://github.com/JJosephph/Apple-health-XML-file-for-heart-rate-analysis/assets/124876944/b20dbd01-5bb9-4d54-965e-583b314aeadb)
![image](https://github.com/JJosephph/Apple-health-XML-file-for-heart-rate-analysis/assets/124876944/2fe44411-79e6-4139-b359-62030f79767f)
![image](https://github.com/JJosephph/Apple-health-XML-file-for-heart-rate-analysis/assets/124876944/ed22184a-5441-4bb4-9a75-c03bb9c20976)
![image](https://github.com/JJosephph/Apple-health-XML-file-for-heart-rate-analysis/assets/124876944/51aaabf3-c94a-4c4e-a6aa-29a890531541)
![image](https://github.com/JJosephph/Apple-health-XML-file-for-heart-rate-analysis/assets/124876944/35d0377a-658f-48a4-bcc5-791eb1cf2384)
# 数据从哪来？
![image](https://github.com/JJosephph/Apple-health-XML-file-for-heart-rate-analysis/assets/124876944/53d59837-2613-45f4-8285-1243459881ed)
![image](https://github.com/JJosephph/Apple-health-XML-file-for-heart-rate-analysis/assets/124876944/b34280e0-f155-41db-8f08-924550879e4f)
