#!/usr/bin/env python3
"""
生成柳州市病媒监测汇总数据看板
"""

import sqlite3
import json

DB_PATH = "/Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring/database/vector_monitoring_summary.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 获取各年度汇总数据
rodent_yearly = cursor.execute("SELECT year, SUM(total_caught) as total, ROUND(AVG(capture_rate), 4) as rate FROM rodent_monthly GROUP BY year ORDER BY year").fetchall()
mosquito_yearly = cursor.execute("SELECT year, SUM(total_caught) as total, ROUND(AVG(density_index), 4) as density FROM mosquito_monthly GROUP BY year ORDER BY year").fetchall()
fly_yearly = cursor.execute("SELECT year, SUM(total_caught) as total, ROUND(AVG(density_index), 4) as density FROM fly_monthly GROUP BY year ORDER BY year").fetchall()
cockroach_yearly = cursor.execute("SELECT year, SUM(total_caught) as total, ROUND(AVG(infestation_rate), 2) as rate, ROUND(AVG(density_index), 2) as density FROM cockroach_monthly GROUP BY year ORDER BY year").fetchall()

# 获取月度趋势数据
rodent_monthly = cursor.execute("SELECT year || '-' || printf('%02d', month) as ym, total_caught, capture_rate FROM rodent_monthly ORDER BY year, month").fetchall()
mosquito_monthly = cursor.execute("SELECT year || '-' || printf('%02d', month) as ym, total_caught, density_index FROM mosquito_monthly ORDER BY year, month").fetchall()
fly_monthly = cursor.execute("SELECT year || '-' || printf('%02d', month) as ym, total_caught, density_index FROM fly_monthly ORDER BY year, month").fetchall()
cockroach_monthly = cursor.execute("SELECT year || '-' || printf('%02d', month) as ym, total_caught, infestation_rate, density_index FROM cockroach_monthly ORDER BY year, month").fetchall()

conn.close()

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>柳州市病媒生物监测数据看板 (2023-2025)</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; margin: 0; padding: 0; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; border-radius: 12px; padding: 25px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .card-icon {{ font-size: 40px; margin-bottom: 10px; }}
        .card-value {{ font-size: 28px; font-weight: bold; color: #667eea; margin: 10px 0; }}
        .card-label {{ color: #666; font-size: 14px; }}
        .charts {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 30px; }}
        .chart-box {{ background: white; border-radius: 12px; padding: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .chart-title {{ font-size: 18px; font-weight: 600; margin-bottom: 20px; border-left: 4px solid #667eea; padding-left: 12px; }}
        .chart-container {{ position: relative; height: 300px; }}
        .section-title {{ font-size: 22px; font-weight: 600; margin: 40px 0 20px; padding-bottom: 10px; border-bottom: 2px solid #667eea; }}
        .data-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .data-table th {{ background: #667eea; color: white; padding: 15px; text-align: center; }}
        .data-table td {{ padding: 12px 15px; text-align: center; border-bottom: 1px solid #eee; }}
        .data-table tr:hover {{ background: #f5f7fa; }}
        .trend-up {{ color: #e74c3c; }}
        .trend-down {{ color: #27ae60; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦟 柳州市病媒生物监测数据看板</h1>
        <p>2023-2025年汇总统计数据</p>
    </div>
    
    <div class="container">
        <h2 class="section-title">📊 年度数据汇总</h2>
        
        <table class="data-table">
            <thead>
                <tr>
                    <th>监测项目</th>
                    <th>2023年</th>
                    <th>2024年</th>
                    <th>2025年</th>
                    <th>趋势</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>🐭 鼠密度捕获数</td>
                    <td>{rodent_yearly[0][1] if len(rodent_yearly) > 0 else '-'}只</td>
                    <td>{rodent_yearly[1][1] if len(rodent_yearly) > 1 else '-'}只</td>
                    <td>{rodent_yearly[2][1] if len(rodent_yearly) > 2 else '-'}只</td>
                    <td class="trend-down">↓下降</td>
                </tr>
                <tr>
                    <td>🦟 蚊密度捕获数</td>
                    <td>{mosquito_yearly[0][1] if len(mosquito_yearly) > 0 else '-'}只</td>
                    <td>{mosquito_yearly[1][1] if len(mosquito_yearly) > 1 else '-'}只</td>
                    <td>{mosquito_yearly[2][1] if len(mosquito_yearly) > 2 else '-'}只</td>
                    <td class="trend-up">↑回升</td>
                </tr>
                <tr>
                    <td>🪰 蝇密度捕获数</td>
                    <td>{fly_yearly[0][1] if len(fly_yearly) > 0 else '-'}只</td>
                    <td>{fly_yearly[1][1] if len(fly_yearly) > 1 else '-'}只</td>
                    <td>{fly_yearly[2][1] if len(fly_yearly) > 2 else '-'}只</td>
                    <td>→稳定</td>
                </tr>
                <tr>
                    <td>🪳 蟑密度捕获数</td>
                    <td>{cockroach_yearly[0][1] if len(cockroach_yearly) > 0 else '-'}只</td>
                    <td>{cockroach_yearly[1][1] if len(cockroach_yearly) > 1 else '-'}只</td>
                    <td>{cockroach_yearly[2][1] if len(cockroach_yearly) > 2 else '-'}只</td>
                    <td class="trend-down">↓下降</td>
                </tr>
            </tbody>
        </table>

        <h2 class="section-title">🐭 鼠密度监测趋势</h2>
        <div class="charts">
            <div class="chart-box">
                <div class="chart-title">月度捕获数量趋势</div>
                <div class="chart-container"><canvas id="rodentChart1"></canvas></div>
            </div>
            <div class="chart-box">
                <div class="chart-title">捕获率变化趋势</div>
                <div class="chart-container"><canvas id="rodentChart2"></canvas></div>
            </div>
        </div>

        <h2 class="section-title">🦟 蚊密度监测趋势</h2>
        <div class="charts">
            <div class="chart-box">
                <div class="chart-title">月度捕获数量趋势</div>
                <div class="chart-container"><canvas id="mosquitoChart1"></canvas></div>
            </div>
            <div class="chart-box">
                <div class="chart-title">密度指数变化</div>
                <div class="chart-container"><canvas id="mosquitoChart2"></canvas></div>
            </div>
        </div>

        <h2 class="section-title">🪰 蝇密度监测趋势</h2>
        <div class="charts">
            <div class="chart-box">
                <div class="chart-title">月度捕获数量趋势</div>
                <div class="chart-container"><canvas id="flyChart1"></canvas></div>
            </div>
            <div class="chart-box">
                <div class="chart-title">密度指数变化</div>
                <div class="chart-container"><canvas id="flyChart2"></canvas></div>
            </div>
        </div>

        <h2 class="section-title">🪳 蟑密度监测趋势</h2>
        <div class="charts">
            <div class="chart-box">
                <div class="chart-title">月度捕获数量趋势</div>
                <div class="chart-container"><canvas id="cockroachChart1"></canvas></div>
            </div>
            <div class="chart-box">
                <div class="chart-title">侵害率与密度指数</div>
                <div class="chart-container"><canvas id="cockroachChart2"></canvas></div>
            </div>
        </div>
    </div>
    
    <script>
        const colors = {{ primary: '#667eea', secondary: '#764ba2', success: '#27ae60', warning: '#f39c12', danger: '#e74c3c', info: '#3498db' }};
        
        // 鼠密度图表
        new Chart(document.getElementById('rodentChart1'), {{
            type: 'line',
            data: {{ labels: {json.dumps([r[0] for r in rodent_monthly])}, datasets: [{{ label: '捕获数量', data: {json.dumps([r[1] for r in rodent_monthly])}, borderColor: colors.primary, backgroundColor: colors.primary + '20', tension: 0.3, fill: true }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});
        new Chart(document.getElementById('rodentChart2'), {{
            type: 'line',
            data: {{ labels: {json.dumps([r[0] for r in rodent_monthly])}, datasets: [{{ label: '捕获率(%)', data: {json.dumps([r[2]*100 for r in rodent_monthly])}, borderColor: colors.warning, backgroundColor: colors.warning + '20', tension: 0.3, fill: true }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});
        
        // 蚊密度图表
        new Chart(document.getElementById('mosquitoChart1'), {{
            type: 'bar',
            data: {{ labels: {json.dumps([r[0] for r in mosquito_monthly])}, datasets: [{{ label: '捕获数量', data: {json.dumps([r[1] for r in mosquito_monthly])}, backgroundColor: colors.primary }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});
        new Chart(document.getElementById('mosquitoChart2'), {{
            type: 'line',
            data: {{ labels: {json.dumps([r[0] for r in mosquito_monthly])}, datasets: [{{ label: '密度指数', data: {json.dumps([r[2] for r in mosquito_monthly])}, borderColor: colors.primary, backgroundColor: colors.primary + '20', tension: 0.3, fill: true }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});
        
        // 蝇密度图表
        new Chart(document.getElementById('flyChart1'), {{
            type: 'bar',
            data: {{ labels: {json.dumps([r[0] for r in fly_monthly])}, datasets: [{{ label: '捕获数量', data: {json.dumps([r[1] for r in fly_monthly])}, backgroundColor: colors.warning }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});
        new Chart(document.getElementById('flyChart2'), {{
            type: 'line',
            data: {{ labels: {json.dumps([r[0] for r in fly_monthly])}, datasets: [{{ label: '密度指数', data: {json.dumps([r[2] for r in fly_monthly])}, borderColor: colors.warning, backgroundColor: colors.warning + '20', tension: 0.3, fill: true }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});
        
        // 蟑密度图表
        new Chart(document.getElementById('cockroachChart1'), {{
            type: 'bar',
            data: {{ labels: {json.dumps([r[0] for r in cockroach_monthly])}, datasets: [{{ label: '捕获数量', data: {json.dumps([r[1] for r in cockroach_monthly])}, backgroundColor: colors.danger }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});
        new Chart(document.getElementById('cockroachChart2'), {{
            type: 'line',
            data: {{ labels: {json.dumps([r[0] for r in cockroach_monthly])}, datasets: [{{ label: '侵害率(%)', data: {json.dumps([r[2] for r in cockroach_monthly])}, borderColor: colors.danger, backgroundColor: colors.danger + '20', tension: 0.3, fill: true }}, {{ label: '密度指数', data: {json.dumps([r[3] for r in cockroach_monthly])}, borderColor: colors.secondary, backgroundColor: colors.secondary + '20', tension: 0.3, fill: true }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});
    </script>
</body>
</html>'''

with open('/Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring/dashboard/柳州市病媒监测看板_2023-2025.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ 看板已生成！")
