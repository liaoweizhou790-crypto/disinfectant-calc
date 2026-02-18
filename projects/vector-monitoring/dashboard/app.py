#!/usr/bin/env python3
"""
病媒生物监测数据看板 - Flask Web 应用
"""

from flask import Flask, render_template, jsonify
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

DB_PATH = "/Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring/database/vector_monitoring.db"

def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    """主看板页面"""
    return render_template('dashboard.html')

@app.route('/api/summary')
def api_summary():
    """获取监测数据汇总"""
    conn = get_db_connection()
    
    summary = {}
    
    # 各病媒生物监测记录数
    tables = [
        ('rodent_monitoring', '鼠密度'),
        ('mosquito_monitoring', '蚊密度'),
        ('fly_monitoring', '蝇密度'),
        ('cockroach_monitoring', '蟑密度'),
        ('tick_monitoring', '蜱虫监测')
    ]
    
    for table, name in tables:
        count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
        summary[name] = count
    
    # 监测点位数量
    points = conn.execute('SELECT COUNT(DISTINCT monitor_point) FROM rodent_monitoring').fetchone()[0]
    summary['监测点位'] = points
    
    conn.close()
    return jsonify(summary)

@app.route('/api/rodent-stats')
def api_rodent_stats():
    """鼠密度统计数据"""
    conn = get_db_connection()
    
    # 按日期统计捕获数量
    rows = conn.execute('''
        SELECT monitor_date, SUM(total_caught) as total, 
               ROUND(AVG(density_rate), 2) as avg_rate
        FROM rodent_monitoring
        GROUP BY monitor_date
        ORDER BY monitor_date
    ''').fetchall()
    
    data = {
        'dates': [row['monitor_date'] for row in rows],
        'totals': [row['total'] for row in rows],
        'rates': [row['avg_rate'] for row in rows]
    }
    
    # 按点位统计
    point_rows = conn.execute('''
        SELECT monitor_point, SUM(total_caught) as total
        FROM rodent_monitoring
        GROUP BY monitor_point
        ORDER BY total DESC
    ''').fetchall()
    
    data['points'] = [row['monitor_point'] for row in point_rows]
    data['point_totals'] = [row['total'] for row in point_rows]
    
    conn.close()
    return jsonify(data)

@app.route('/api/mosquito-stats')
def api_mosquito_stats():
    """蚊密度统计数据"""
    conn = get_db_connection()
    
    rows = conn.execute('''
        SELECT monitor_date, SUM(total_count) as total,
               SUM(culex_pipiens) as culex_pipiens,
               SUM(culex_quinquefasciatus) as culex_quinquefasciatus,
               SUM(aedes_albopictus) as aedes_albopictus
        FROM mosquito_monitoring
        GROUP BY monitor_date
        ORDER BY monitor_date
    ''').fetchall()
    
    data = {
        'dates': [row['monitor_date'] for row in rows],
        'totals': [row['total'] for row in rows],
        'culex_pipiens': [row['culex_pipiens'] for row in rows],
        'culex_quinquefasciatus': [row['culex_quinquefasciatus'] for row in rows],
        'aedes_albopictus': [row['aedes_albopictus'] for row in rows]
    }
    
    conn.close()
    return jsonify(data)

@app.route('/api/fly-stats')
def api_fly_stats():
    """蝇密度统计数据"""
    conn = get_db_connection()
    
    rows = conn.execute('''
        SELECT monitor_date, SUM(total_count) as total,
               SUM(house_fly) as house_fly,
               SUM(chrysomya_megacephala) as chrysomya,
               SUM(lucilia_sericata) as lucilia
        FROM fly_monitoring
        GROUP BY monitor_date
        ORDER BY monitor_date
    ''').fetchall()
    
    data = {
        'dates': [row['monitor_date'] for row in rows],
        'totals': [row['total'] for row in rows],
        'house_fly': [row['house_fly'] for row in rows],
        'chrysomya': [row['chrysomya'] for row in rows],
        'lucilia': [row['lucilia'] for row in rows]
    }
    
    conn.close()
    return jsonify(data)

@app.route('/api/cockroach-stats')
def api_cockroach_stats():
    """蟑密度统计数据"""
    conn = get_db_connection()
    
    rows = conn.execute('''
        SELECT monitor_date, SUM(total_count) as total,
               ROUND(AVG(positive_rate), 2) as avg_positive_rate
        FROM cockroach_monitoring
        GROUP BY monitor_date
        ORDER BY monitor_date
    ''').fetchall()
    
    data = {
        'dates': [row['monitor_date'] for row in rows],
        'totals': [row['total'] for row in rows],
        'positive_rates': [row['avg_positive_rate'] for row in rows]
    }
    
    conn.close()
    return jsonify(data)

@app.route('/api/tick-stats')
def api_tick_stats():
    """蜱虫监测统计数据"""
    conn = get_db_connection()
    
    rows = conn.execute('''
        SELECT monitor_date, SUM(total_count) as total,
               SUM(haemaphysalis_longicornis) as longicornis,
               SUM(dermacentor_silvarum) as silvarum
        FROM tick_monitoring
        GROUP BY monitor_date
        ORDER BY monitor_date
    ''').fetchall()
    
    data = {
        'dates': [row['monitor_date'] for row in rows],
        'totals': [row['total'] for row in rows],
        'longicornis': [row['longicornis'] for row in rows],
        'silvarum': [row['silvarum'] for row in rows]
    }
    
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    print("🚀 启动病媒生物监测数据看板...")
    print("📊 访问地址: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
