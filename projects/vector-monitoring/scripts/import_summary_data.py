#!/usr/bin/env python3
"""
导入柳州市病媒监测汇总数据
从Excel文件导入2023-2025年按月汇总数据
"""

import pandas as pd
import sqlite3
import os

DB_PATH = "/Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring/database/vector_monitoring_summary.db"
DATA_DIR = "/Users/liaoweizhou/Desktop/工作/10-病媒监测数据"

def import_rodent_data():
    """导入鼠密度数据"""
    filepath = os.path.join(DATA_DIR, "柳州市鼠密度（粘捕法）数据库.xlsx")
    df = pd.read_excel(filepath, header=None)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    current_year = None
    for idx, row in df.iterrows():
        # 检测年份行
        if str(row[0]).endswith('年') and '202' in str(row[0]):
            current_year = int(str(row[0]).replace('年', ''))
            continue
        
        # 检测数据行（月份）
        if current_year and str(row[0]).endswith('月') and str(row[0]) != '合计':
            month = int(str(row[0]).replace('月', ''))
            effective_traps = int(row[1]) if pd.notna(row[1]) else 0
            total_caught = int(row[2]) if pd.notna(row[2]) else 0
            capture_rate = float(row[3]) if pd.notna(row[3]) else 0
            
            cursor.execute('''
            INSERT OR REPLACE INTO rodent_monthly 
            (year, month, effective_traps, total_caught, capture_rate)
            VALUES (?, ?, ?, ?, ?)
            ''', (current_year, month, effective_traps, total_caught, capture_rate))
    
    conn.commit()
    conn.close()
    print("✅ 鼠密度数据导入完成")

def import_mosquito_data():
    """导入蚊密度数据"""
    filepath = os.path.join(DATA_DIR, "柳州市蚊密度（诱蚊灯法）数据库.xlsx")
    df = pd.read_excel(filepath, header=None)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    current_year = None
    for idx, row in df.iterrows():
        if str(row[0]).endswith('年') and '202' in str(row[0]):
            current_year = int(str(row[0]).replace('年', ''))
            continue
        
        if current_year and str(row[0]).endswith('月') and str(row[0]) != '合计':
            month = int(str(row[0]).replace('月', ''))
            light_traps = int(row[1]) if pd.notna(row[1]) else 0
            trap_nights = int(row[2]) if pd.notna(row[2]) else 0
            total_caught = int(row[3]) if pd.notna(row[3]) else 0
            density_index = float(row[4]) if pd.notna(row[4]) else 0
            
            cursor.execute('''
            INSERT OR REPLACE INTO mosquito_monthly 
            (year, month, light_traps, trap_nights, total_caught, density_index)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (current_year, month, light_traps, trap_nights, total_caught, density_index))
    
    conn.commit()
    conn.close()
    print("✅ 蚊密度数据导入完成")

def import_fly_data():
    """导入蝇密度数据"""
    filepath = os.path.join(DATA_DIR, "柳州市蝇密度（捕蝇笼法）.xlsx")
    df = pd.read_excel(filepath, header=None)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    current_year = None
    for idx, row in df.iterrows():
        if str(row[0]).endswith('年') and '202' in str(row[0]):
            current_year = int(str(row[0]).replace('年', ''))
            continue
        
        if current_year and str(row[0]).endswith('月') and str(row[0]) != '合计':
            month = int(str(row[0]).replace('月', ''))
            fly_cages = int(row[1]) if pd.notna(row[1]) else 0
            total_caught = int(row[2]) if pd.notna(row[2]) else 0
            density_index = float(row[3]) if pd.notna(row[3]) else 0
            
            cursor.execute('''
            INSERT OR REPLACE INTO fly_monthly 
            (year, month, fly_cages, total_caught, density_index)
            VALUES (?, ?, ?, ?, ?)
            ''', (current_year, month, fly_cages, total_caught, density_index))
    
    conn.commit()
    conn.close()
    print("✅ 蝇密度数据导入完成")

def import_cockroach_data():
    """导入蟑密度数据"""
    filepath = os.path.join(DATA_DIR, "柳州市蟑密度（粘蟑法)数据库.xlsx")
    df = pd.read_excel(filepath, header=None)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    current_year = None
    for idx, row in df.iterrows():
        if str(row[0]).endswith('年') and '202' in str(row[0]):
            current_year = int(str(row[0]).replace('年', ''))
            continue
        
        if current_year and str(row[0]).endswith('月') and str(row[0]) != '合计':
            month = int(str(row[0]).replace('月', ''))
            rooms_monitored = int(row[1]) if pd.notna(row[1]) else 0
            rooms_positive = int(row[2]) if pd.notna(row[2]) else 0
            sticky_papers = int(row[3]) if pd.notna(row[3]) else 0
            papers_positive = int(row[4]) if pd.notna(row[4]) else 0
            total_caught = int(row[5]) if pd.notna(row[5]) else 0
            trap_rate = float(row[6]) if pd.notna(row[6]) else 0
            infestation_rate = float(row[7]) if pd.notna(row[7]) else 0
            density_index = float(row[9]) if pd.notna(row[9]) else 0
            
            cursor.execute('''
            INSERT OR REPLACE INTO cockroach_monthly 
            (year, month, rooms_monitored, rooms_positive, sticky_papers, papers_positive, 
             total_caught, trap_rate, infestation_rate, density_index)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (current_year, month, rooms_monitored, rooms_positive, sticky_papers, 
                  papers_positive, total_caught, trap_rate, infestation_rate, density_index))
    
    conn.commit()
    conn.close()
    print("✅ 蟑密度数据导入完成")

if __name__ == "__main__":
    import_rodent_data()
    import_mosquito_data()
    import_fly_data()
    import_cockroach_data()
    print("\n✅ 所有数据导入完成！")
