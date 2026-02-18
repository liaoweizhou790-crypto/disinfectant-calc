#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将Markdown转换为PDF
"""

import markdown
from weasyprint import HTML, CSS
import sys

# 读取Markdown文件
with open('/Users/liaoweizhou/Desktop/消毒剂配比系统_操作说明书.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# 转换为HTML
html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

# 添加CSS样式
html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>消毒剂配比系统操作说明书</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
            @bottom-center {{
                content: "第 " counter(page) " 页";
                font-size: 10pt;
                color: #666;
            }}
        }}
        body {{
            font-family: "PingFang SC", "Microsoft YaHei", "WenQuanYi Micro Hei", sans-serif;
            font-size: 11pt;
            line-height: 1.8;
            color: #333;
        }}
        h1 {{
            font-size: 22pt;
            color: #2c3e50;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-top: 30px;
        }}
        h2 {{
            font-size: 16pt;
            color: #34495e;
            border-left: 4px solid #667eea;
            padding-left: 10px;
            margin-top: 25px;
        }}
        h3 {{
            font-size: 13pt;
            color: #445566;
            margin-top: 20px;
        }}
        h4 {{
            font-size: 12pt;
            color: #556677;
        }}
        p {{
            margin: 10px 0;
            text-align: justify;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}
        li {{
            margin: 5px 0;
        }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "Courier New", monospace;
            font-size: 10pt;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 20px 0;
        }}
        strong {{
            color: #2c3e50;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background: #667eea;
            color: white;
        }}
        tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        blockquote {{
            border-left: 4px solid #667eea;
            margin: 15px 0;
            padding: 10px 20px;
            background: #f8f9fa;
            color: #666;
        }}
        .cover {{
            text-align: center;
            padding: 100px 0;
            page-break-after: always;
        }}
        .cover h1 {{
            font-size: 28pt;
            border: none;
            color: #667eea;
        }}
        .cover .subtitle {{
            font-size: 16pt;
            color: #666;
            margin-top: 20px;
        }}
        .cover .version {{
            font-size: 14pt;
            color: #999;
            margin-top: 40px;
        }}
    </style>
</head>
<body>
    <div class="cover">
        <h1>🧴 消毒剂配比系统</h1>
        <div class="subtitle">操作说明书</div>
        <div class="version">版本 V1.3.1</div>
        <div style="margin-top: 60px; color: #999;">
            柳州市疾病预防控制中心<br>
            消毒与病媒生物防制所<br><br>
            2026年2月
        </div>
    </div>
    {html_content}
</body>
</html>
"""

# 保存为PDF
output_path = '/Users/liaoweizhou/Desktop/消毒剂配比系统_操作说明书.pdf'
HTML(string=html_template).write_pdf(output_path)

print(f"PDF已生成: {output_path}")
