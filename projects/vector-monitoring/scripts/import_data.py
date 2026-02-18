#!/usr/bin/env python3
"""
病媒生物监测数据导入脚本
从 Excel 文件导入数据到 SQLite 数据库
"""

import pandas as pd
import sqlite3
import os
from datetime import datetime

def import_rodent_data(excel_path, db_path):
    """导入鼠密度监测数据"""
    df = pd.read_excel(excel_path)
    conn = sqlite3.connect(db_path)
    
    for _, row in df.iterrows():
        conn.execute('''
        INSERT INTO rodent_monitoring 
        (monitor_date, monitor_point, trap_count, effective_trap_count, 
         brown_rat, house_mouse, other, total_caught)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['监测日期'],
            row['监测点位'],
            row['布放夹数'],
            row['有效夹数'],
            row['褐家鼠'],
            row['小家鼠'],
            row['其他'],
            row['捕获总数']
        ))
    
    conn.commit()
    conn.close()
    print(f"✅ 鼠密度数据导入完成: {len(df)} 条记录")

def import_mosquito_data(excel_path, db_path):
    """导入蚊密度监测数据"""
    df = pd.read_excel(excel_path)
    conn = sqlite3.connect(db_path)
    
    for _, row in df.iterrows():
        conn.execute('''
        INSERT INTO mosquito_monitoring 
        (monitor_date, monitor_point, light_trap_count, monitor_nights,
         culex_pipiens, culex_quinquefasciatus, aedes_albopictus, other, total_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['监测日期'],
            row['监测点位'],
            row['诱蚊灯数'],
            row['监测夜数'],
            row['淡色库蚊'],
            row['致倦库蚊'],
            row['白纹伊蚊'],
            row['其他'],
            row['合计']
        ))
    
    conn.commit()
    conn.close()
    print(f"✅ 蚊密度数据导入完成: {len(df)} 条记录")

def import_fly_data(excel_path, db_path):
    """导入蝇密度监测数据"""
    df = pd.read_excel(excel_path)
    conn = sqlite3.connect(db_path)
    
    for _, row in df.iterrows():
        conn.execute('''
        INSERT INTO fly_monitoring 
        (monitor_date, monitor_point, trap_count,
         house_fly, chrysomya_megacephala, lucilia_sericata, other, total_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['监测日期'],
            row['监测点位'],
            row['捕蝇笼数'],
            row['家蝇'],
            row['大头金蝇'],
            row['丝光绿蝇'],
            row['其他'],
            row['合计']
        ))
    
    conn.commit()
    conn.close()
    print(f"✅ 蝇密度数据导入完成: {len(df)} 条记录")

def import_cockroach_data(excel_path, db_path):
    """导入蟑密度监测数据"""
    df = pd.read_excel(excel_path)
    conn = sqlite3.connect(db_path)
    
    for _, row in df.iterrows():
        conn.execute('''
        INSERT INTO cockroach_monitoring 
        (monitor_date, monitor_point, sticky_paper_count,
         german_cockroach, american_cockroach, other, positive_papers, total_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['监测日期'],
            row['监测点位'],
            row['粘蟑纸数'],
            row['德国小蠊'],
            row['美洲大蠊'],
            row['其他'],
            row['阳性张数'],
            row['合计']
        ))
    
    conn.commit()
    conn.close()
    print(f"✅ 蟑密度数据导入完成: {len(df)} 条记录")

def import_tick_data(excel_path, db_path):
    """导入蜱虫监测数据"""
    df = pd.read_excel(excel_path)
    conn = sqlite3.connect(db_path)
    
    for _, row in df.iterrows():
        conn.execute('''
        INSERT INTO tick_monitoring 
        (monitor_date, monitor_point, host_type, host_count,
         haemaphysalis_longicornis, dermacentor_silvarum, other,
         bunya_virus_test, rickettsia_test, total_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['监测日期'],
            row['监测点位'],
            row['宿主类型'],
            row['宿主数量'],
            row['长角血蜱'],
            row['森林革蜱'],
            row['其他'],
            row['布尼亚病毒检测'],
            row['立克次体检测'],
            row['合计']
        ))
    
    conn.commit()
    conn.close()
    print(f"✅ 蜱虫监测数据导入完成: {len(df)} 条记录")

def import_all_data(data_dir, db_path):
    """导入所有数据"""
    files = {
        '鼠密度监测': ('鼠密度监测_2024示例.xlsx', import_rodent_data),
        '蚊密度监测': ('蚊密度监测_2024示例.xlsx', import_mosquito_data),
        '蝇密度监测': ('蝇密度监测_2024示例.xlsx', import_fly_data),
        '蟑密度监测': ('蟑密度监测_2024示例.xlsx', import_cockroach_data),
        '蜱虫监测': ('蜱虫监测_2024示例.xlsx', import_tick_data),
    }
    
    for name, (filename, import_func) in files.items():
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            try:
                import_func(filepath, db_path)
            except Exception as e:
                print(f"❌ {name}导入失败: {e}")
        else:
            print(f"⚠️ 文件不存在: {filepath}")

if __name__ == "__main__":
    data_dir = "/Users/liaoweizhou/Desktop/工作/10-病媒监测数据"
    db_path = "/Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring/database/vector_monitoring.db"
    import_all_data(data_dir, db_path)
    print("\n✅ 所有数据导入完成！")
