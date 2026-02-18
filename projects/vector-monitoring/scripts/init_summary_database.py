#!/usr/bin/env python3
"""
病媒生物监测数据库初始化脚本 - 汇总统计版
存储按年月汇总的监测数据
"""

import sqlite3
import os

def init_database(db_path):
    """初始化数据库"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. 鼠密度监测汇总表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rodent_monthly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        effective_traps INTEGER DEFAULT 0,
        total_caught INTEGER DEFAULT 0,
        capture_rate REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(year, month)
    )
    ''')
    
    # 2. 蚊密度监测汇总表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mosquito_monthly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        light_traps INTEGER DEFAULT 0,
        trap_nights INTEGER DEFAULT 0,
        total_caught INTEGER DEFAULT 0,
        density_index REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(year, month)
    )
    ''')
    
    # 3. 蝇密度监测汇总表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fly_monthly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        fly_cages INTEGER DEFAULT 0,
        total_caught INTEGER DEFAULT 0,
        density_index REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(year, month)
    )
    ''')
    
    # 4. 蟑密度监测汇总表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cockroach_monthly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER NOT NULL,
        rooms_monitored INTEGER DEFAULT 0,
        rooms_positive INTEGER DEFAULT 0,
        sticky_papers INTEGER DEFAULT 0,
        papers_positive INTEGER DEFAULT 0,
        total_caught INTEGER DEFAULT 0,
        trap_rate REAL DEFAULT 0,
        infestation_rate REAL DEFAULT 0,
        density_index REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(year, month)
    )
    ''')
    
    # 5. 蜱虫监测汇总表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tick_monthly (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        year INTEGER NOT NULL,
        month INTEGER DEFAULT 0,
        location TEXT,
        hosts_examined INTEGER DEFAULT 0,
        total_ticks INTEGER DEFAULT 0,
        bunya_virus_positive INTEGER DEFAULT 0,
        rickettsia_positive INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print(f"✅ 汇总统计数据库初始化完成: {db_path}")

if __name__ == "__main__":
    db_path = "/Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring/database/vector_monitoring_summary.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    init_database(db_path)
