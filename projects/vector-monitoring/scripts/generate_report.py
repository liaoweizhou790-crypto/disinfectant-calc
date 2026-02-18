#!/usr/bin/env python3
import sqlite3
import json

DB_PATH = "/Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring/database/vector_monitoring.db"
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 获取汇总数据
summary = {}
tables = [
    ('rodent_monitoring', '鼠密度'),
    ('mosquito_monitoring', '蚊密度'),
    ('fly_monitoring', '蝇密度'),
    ('cockroach_monitoring', '蟑密度'),
    ('tick_monitoring', '蜱虫监测')
]
for table, name in tables:
    count = cursor.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
    summary[name] = count

# 获取数据
def get_data(query):
    cursor.execute(query)
    columns = [description[0] for description in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

rodent = get_data('SELECT monitor_date, SUM(total_caught) as total, ROUND(AVG(density_rate), 2) as avg_rate FROM rodent_monitoring GROUP BY monitor_date ORDER BY monitor_date')

mosquito = get_data('''
    SELECT monitor_date, SUM(total_count) as total,
           SUM(culex_pipiens) as culex_pipiens,
           SUM(culex_quinquefasciatus) as culex_quinquefasciatus,
           SUM(aedes_albopictus) as aedes_albopictus
    FROM mosquito_monitoring GROUP BY monitor_date ORDER BY monitor_date
''')

fly = get_data('''
    SELECT monitor_date, SUM(total_count) as total,
           SUM(house_fly) as house_fly,
           SUM(chrysomya_megacephala) as chrysomya,
           SUM(lucilia_sericata) as lucilia
    FROM fly_monitoring GROUP BY monitor_date ORDER BY monitor_date
''')

cockroach = get_data('SELECT monitor_date, SUM(total_count) as total, ROUND(AVG(positive_rate), 2) as avg_positive_rate FROM cockroach_monitoring GROUP BY monitor_date ORDER BY monitor_date')

tick = get_data('''
    SELECT monitor_date, SUM(total_count) as total,
           SUM(haemaphysalis_longicornis) as longicornis,
           SUM(dermacentor_silvarum) as silvarum
    FROM tick_monitoring GROUP BY monitor_date ORDER BY monitor_date
''')

conn.close()

mosquito_pipiens = sum(r['culex_pipiens'] for r in mosquito)
mosquito_quinque = sum(r['culex_quinquefasciatus'] for r in mosquito)
mosquito_albo = sum(r['aedes_albopictus'] for r in mosquito)

fly_house = sum(r['house_fly'] for r in fly)
fly_chrysomya = sum(r['chrysomya'] for r in fly)
fly_lucilia = sum(r['lucilia'] for r in fly)

tick_longi = sum(r['longicornis'] for r in tick)
tick_silvarum = sum(r['silvarum'] for r in tick)

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>病媒生物监测数据看板</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; margin: 0; padding: 0; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
        .header h1 {{ margin: 0; font-size: 28px; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; border-radius: 12px; padding: 25px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .card-icon {{ font-size: 40px; margin-bottom: 10px; }}
        .card-value {{ font-size: 32px; font-weight: bold; color: #667eea; margin: 10px 0; }}
        .card-label {{ color: #666; font-size: 14px; }}
        .charts {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); gap: 30px; }}
        .chart-box {{ background: white; border-radius: 12px; padding: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
        .chart-title {{ font-size: 18px; font-weight: 600; margin-bottom: 20px; border-left: 4px solid #667eea; padding-left: 12px; }}
        .chart-container {{ position: relative; height: 300px; }}
        .section-title {{ font-size: 22px; font-weight: 600; margin: 40px 0 20px; padding-bottom: 10px; border-bottom: 2px solid #667eea; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🦟 病媒生物监测数据看板</h1>
        <p>实时监测数据分析与可视化</p>
    </div>
    
    <div class="container">
        <div class="summary">
            <div class="card"><div class="card-icon">🐭</div><div class="card-value">{summary['鼠密度']}</div><div class="card-label">鼠密度监测</div></div>
            <div class="card"><div class="card-icon">🦟</div><div class="card-value">{summary['蚊密度']}</div><div class="card-label">蚊密度监测</div></div>
            <div class="card"><div class="card-icon">🪰</div><div class="card-value">{summary['蝇密度']}</div><div class="card-label">蝇密度监测</div></div>
            <div class="card"><div class="card-icon">🪳</div><div class="card-value">{summary['蟑密度']}</div><div class="card-label">蟑密度监测</div></div>
            <div class="card"><div class="card-icon">🕷️</div><div class="card-value">{summary['蜱虫监测']}</div><div class="card-label">蜱虫监测</div></div>
        </div>
        
        <h2 class="section-title">🐭 鼠密度监测</h2>
        <div class="charts">
            <div class="chart-box"><div class="chart-title">捕获数量趋势</div><div class="chart-container"><canvas id="rodentChart1"></canvas></div></div>
            <div class="chart-box"><div class="chart-title">捕获率变化 (%)</div><div class="chart-container"><canvas id="rodentChart2"></canvas></div></div>
        </div>
        
        <h2 class="section-title">🦟 蚊密度监测</h2>
        <div class="charts">
            <div class="chart-box"><div class="chart-title">蚊虫种类分布</div><div class="chart-container"><canvas id="mosquitoChart1"></canvas></div></div>
            <div class="chart-box"><div class="chart-title">蚊密度趋势</div><div class="chart-container"><canvas id="mosquitoChart2"></canvas></div></div>
        </div>
        
        <h2 class="section-title">🪰 蝇密度监测</h2>
        <div class="charts">
            <div class="chart-box"><div class="chart-title">蝇类种类分布</div><div class="chart-container"><canvas id="flyChart1"></canvas></div></div>
            <div class="chart-box"><div class="chart-title">蝇密度趋势</div><div class="chart-container"><canvas id="flyChart2"></canvas></div></div>
        </div>
        
        <h2 class="section-title">🪳 蟑密度监测</h2>
        <div class="charts">
            <div class="chart-box"><div class="chart-title">蟑螂捕获趋势</div><div class="chart-container"><canvas id="cockroachChart1"></canvas></div></div>
            <div class="chart-box"><div class="chart-title">阳性率变化 (%)</div><div class="chart-container"><canvas id="cockroachChart2"></canvas></div></div>
        </div>
        
        <h2 class="section-title">🕷️ 蜱虫监测</h2>
        <div class="charts">
            <div class="chart-box"><div class="chart-title">蜱虫种类分布</div><div class="chart-container"><canvas id="tickChart1"></canvas></div></div>
            <div class="chart-box"><div class="chart-title">蜱虫监测趋势</div><div class="chart-container"><canvas id="tickChart2"></canvas></div></div>
        </div>
    </div>
    
    <script>
        const colors = {{ primary: '#667eea', secondary: '#764ba2', success: '#48bb78', warning: '#ed8936', danger: '#f56565', info: '#4299e1' }};
        
        // 鼠密度图表
        new Chart(document.getElementById('rodentChart1'), {{
            type: 'line',
            data: {{ labels: {json.dumps([r['monitor_date'] for r in rodent])}, datasets: [{{ label: '捕获总数', data: {json.dumps([r['total'] for r in rodent])}, borderColor: colors.primary, backgroundColor: colors.primary + '20', tension: 0.4, fill: true }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
        }});
        new Chart(document.getElementById('rodentChart2'), {{
            type: 'bar',
            data: {{ labels: {json.dumps([r['monitor_date'] for r in rodent])}, datasets: [{{ label: '捕获率(%)', data: {json.dumps([r['avg_rate'] for r in rodent])}, backgroundColor: colors.warning }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
        }});
        
        // 蚊密度图表
        new Chart(document.getElementById('mosquitoChart1'), {{
            type: 'doughnut',
            data: {{ labels: ['淡色库蚊', '致倦库蚊', '白纹伊蚊'], datasets: [{{ data: [{mosquito_pipiens}, {mosquito_quinque}, {mosquito_albo}], backgroundColor: [colors.primary, colors.secondary, colors.success] }}] }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});
        new Chart(document.getElementById('mosquitoChart2'), {{
            type: 'line',
            data: {{ labels: {json.dumps([r['monitor_date'] for r in mosquito])}, datasets: [{{ label: '蚊虫总数', data: {json.dumps([r['total'] for r in mosquito])}, borderColor: colors.primary, backgroundColor: colors.primary + '20', tension: 0.4, fill: true }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
        }});
        
        // 蝇密度图表
        new Chart(document.getElementById('flyChart1'), {{
            type: 'doughnut',
            data: {{ labels: ['家蝇', '大头金蝇', '丝光绿蝇'], datasets: [{{ data: [{fly_house}, {fly_chrysomya}, {fly_lucilia}], backgroundColor: [colors.warning, colors.danger, colors.info] }}] }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});
        new Chart(document.getElementById('flyChart2'), {{
            type: 'line',
            data: {{ labels: {json.dumps([r['monitor_date'] for r in fly])}, datasets: [{{ label: '蝇类总数', data: {json.dumps([r['total'] for r in fly])}, borderColor: colors.warning, backgroundColor: colors.warning + '20', tension: 0.4, fill: true }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
        }});
        
        // 蟑密度图表
        new Chart(document.getElementById('cockroachChart1'), {{
            type: 'line',
            data: {{ labels: {json.dumps([r['monitor_date'] for r in cockroach])}, datasets: [{{ label: '捕获总数', data: {json.dumps([r['total'] for r in cockroach])}, borderColor: colors.danger, backgroundColor: colors.danger + '20', tension: 0.4, fill: true }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
        }});
        new Chart(document.getElementById('cockroachChart2'), {{
            type: 'bar',
            data: {{ labels: {json.dumps([r['monitor_date'] for r in cockroach])}, datasets: [{{ label: '阳性率(%)', data: {json.dumps([r['avg_positive_rate'] for r in cockroach])}, backgroundColor: colors.danger }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
        }});
        
        // 蜱虫图表
        new Chart(document.getElementById('tickChart1'), {{
            type: 'doughnut',
            data: {{ labels: ['长角血蜱', '森林革蜱'], datasets: [{{ data: [{tick_longi}, {tick_silvarum}], backgroundColor: [colors.secondary, colors.info] }}] }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});
        new Chart(document.getElementById('tickChart2'), {{
            type: 'line',
            data: {{ labels: {json.dumps([r['monitor_date'] for r in tick])}, datasets: [{{ label: '蜱虫总数', data: {json.dumps([r['total'] for r in tick])}, borderColor: colors.secondary, backgroundColor: colors.secondary + '20', tension: 0.4, fill: true }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
        }});
    </script>
</body>
</html>'''

with open('/Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring/dashboard/病媒监测看板.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("✅ 静态看板已生成！")
