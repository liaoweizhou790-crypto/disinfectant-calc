#!/usr/bin/env python3
"""
病媒生物监测数据库初始化脚本
创建 SQLite 数据库和表结构
"""

import sqlite3
import os

def init_database(db_path):
    """初始化数据库"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. 鼠密度监测表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rodent_monitoring (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monitor_date DATE NOT NULL,
        monitor_point TEXT NOT NULL,
        trap_count INTEGER DEFAULT 0,
        effective_trap_count INTEGER DEFAULT 0,
        brown_rat INTEGER DEFAULT 0,
        house_mouse INTEGER DEFAULT 0,
        other INTEGER DEFAULT 0,
        total_caught INTEGER DEFAULT 0,
        density_rate REAL GENERATED ALWAYS AS (
            CASE WHEN effective_trap_count > 0 
            THEN ROUND(CAST(total_caught AS REAL) / effective_trap_count * 100, 2)
            ELSE 0 END
        ) STORED,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 2. 蚊密度监测表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mosquito_monitoring (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monitor_date DATE NOT NULL,
        monitor_point TEXT NOT NULL,
        light_trap_count INTEGER DEFAULT 0,
        monitor_nights INTEGER DEFAULT 0,
        culex_pipiens INTEGER DEFAULT 0,
        culex_quinquefasciatus INTEGER DEFAULT 0,
        aedes_albopictus INTEGER DEFAULT 0,
        other INTEGER DEFAULT 0,
        total_count INTEGER DEFAULT 0,
        density_index REAL GENERATED ALWAYS AS (
            CASE WHEN light_trap_count > 0 AND monitor_nights > 0
            THEN ROUND(CAST(total_count AS REAL) / light_trap_count / monitor_nights, 2)
            ELSE 0 END
        ) STORED,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 3. 蝇密度监测表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fly_monitoring (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monitor_date DATE NOT NULL,
        monitor_point TEXT NOT NULL,
        trap_count INTEGER DEFAULT 0,
        house_fly INTEGER DEFAULT 0,
        chrysomya_megacephala INTEGER DEFAULT 0,
        lucilia_sericata INTEGER DEFAULT 0,
        other INTEGER DEFAULT 0,
        total_count INTEGER DEFAULT 0,
        density_index REAL GENERATED ALWAYS AS (
            CASE WHEN trap_count > 0
            THEN ROUND(CAST(total_count AS REAL) / trap_count, 2)
            ELSE 0 END
        ) STORED,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 4. 蟑密度监测表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cockroach_monitoring (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monitor_date DATE NOT NULL,
        monitor_point TEXT NOT NULL,
        sticky_paper_count INTEGER DEFAULT 0,
        german_cockroach INTEGER DEFAULT 0,
        american_cockroach INTEGER DEFAULT 0,
        other INTEGER DEFAULT 0,
        positive_papers INTEGER DEFAULT 0,
        total_count INTEGER DEFAULT 0,
        positive_rate REAL GENERATED ALWAYS AS (
            CASE WHEN sticky_paper_count > 0
            THEN ROUND(CAST(positive_papers AS REAL) / sticky_paper_count * 100, 2)
            ELSE 0 END
        ) STORED,
        density_index REAL GENERATED ALWAYS AS (
            CASE WHEN sticky_paper_count > 0
            THEN ROUND(CAST(total_count AS REAL) / sticky_paper_count, 2)
            ELSE 0 END
        ) STORED,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 5. 蜱虫监测表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tick_monitoring (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        monitor_date DATE NOT NULL,
        monitor_point TEXT NOT NULL,
        host_type TEXT,
        host_count INTEGER DEFAULT 0,
        haemaphysalis_longicornis INTEGER DEFAULT 0,
        dermacentor_silvarum INTEGER DEFAULT 0,
        other INTEGER DEFAULT 0,
        bunya_virus_test TEXT,
        rickettsia_test TEXT,
        total_count INTEGER DEFAULT 0,
        infestation_rate REAL GENERATED ALWAYS AS (
            CASE WHEN host_count > 0
            THEN ROUND(CAST(total_count AS REAL) / host_count, 2)
            ELSE 0 END
        ) STORED,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 6. 监测点位信息表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS monitor_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        point_name TEXT UNIQUE NOT NULL,
        point_type TEXT,
        address TEXT,
        longitude REAL,
        latitude REAL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_rodent_date ON rodent_monitoring(monitor_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_mosquito_date ON mosquito_monitoring(monitor_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_fly_date ON fly_monitoring(monitor_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_cockroach_date ON cockroach_monitoring(monitor_date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_tick_date ON tick_monitoring(monitor_date)')
    
    conn.commit()
    conn.close()
    print(f"✅ 数据库初始化完成: {db_path}")

if __name__ == "__main__":
    db_path = "/Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring/database/vector_monitoring.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    init_database(db_path)
