# 🦟 病媒生物监测数据库与看板系统

## 项目概述

为廖所长搭建的病媒生物监测数据管理系统，支持五种病媒生物（鼠、蚊、蝇、蟑、蜱虫）的数据存储、管理和可视化看板展示。

## 项目结构

```
projects/vector-monitoring/
├── database/
│   └── vector_monitoring.db    # SQLite 数据库
├── scripts/
│   ├── init_database.py        # 数据库初始化脚本
│   └── import_data.py          # 数据导入脚本
└── dashboard/
    ├── app.py                  # Flask Web 应用
    └── templates/
        └── dashboard.html      # 看板页面
```

## 数据库设计

### 监测数据表

1. **rodent_monitoring** - 鼠密度监测
   - 监测日期、点位、布放夹数、有效夹数
   - 褐家鼠、小家鼠、其他捕获数量
   - 自动计算捕获率

2. **mosquito_monitoring** - 蚊密度监测
   - 监测日期、点位、诱蚊灯数、监测夜数
   - 淡色库蚊、致倦库蚊、白纹伊蚊数量
   - 自动计算密度指数

3. **fly_monitoring** - 蝇密度监测
   - 监测日期、点位、捕蝇笼数
   - 家蝇、大头金蝇、丝光绿蝇数量
   - 自动计算密度指数

4. **cockroach_monitoring** - 蟑密度监测
   - 监测日期、点位、粘蟑纸数
   - 德国小蠊、美洲大蠊数量
   - 自动计算阳性率

5. **tick_monitoring** - 蜱虫监测
   - 监测日期、点位、宿主类型和数量
   - 长角血蜱、森林革蜱数量
   - 布尼亚病毒和立克次体检测结果

## 使用方法

### 1. 启动看板

```bash
cd /Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring/dashboard
python3 app.py
```

访问地址: http://127.0.0.1:5000

### 2. 导入新数据

将新的 Excel 文件放入数据目录，然后运行：

```bash
cd /Users/liaoweizhou/.openclaw/workspace/projects/vector-monitoring
python3 scripts/import_data.py
```

### 3. 数据库查询示例

```python
import sqlite3

conn = sqlite3.connect('database/vector_monitoring.db')
cursor = conn.cursor()

# 查询鼠密度监测数据
cursor.execute('SELECT * FROM rodent_monitoring LIMIT 10')
results = cursor.fetchall()
```

## 看板功能

- 📊 **数据汇总卡片**: 显示各类病媒生物监测记录数
- 📈 **趋势图表**: 各类病媒生物密度随时间变化趋势
- 🥧 **分布图表**: 不同种类病媒生物的占比分布
- 📍 **点位统计**: 监测点位分布情况

## 数据来源

原始数据文件位于: `~/Desktop/工作/10-病媒监测数据/`

- 鼠密度监测_2024示例.xlsx
- 蚊密度监测_2024示例.xlsx
- 蝇密度监测_2024示例.xlsx
- 蟑密度监测_2024示例.xlsx
- 蜱虫监测_2024示例.xlsx

## 技术栈

- **后端**: Python + Flask
- **数据库**: SQLite
- **前端**: HTML5 + Chart.js
- **数据处理**: Pandas

## 当前状态

✅ 数据库已初始化
✅ 示例数据已导入 (共50条记录)
✅ Flask看板已启动 (http://127.0.0.1:5000)
