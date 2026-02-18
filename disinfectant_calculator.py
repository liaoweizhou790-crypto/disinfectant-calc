#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消毒剂配比计算器
专为疾控消毒工作设计
作者：廖维洲的AI助手
版本：1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

class DisinfectantCalculator:
    """消毒剂配比计算器主类"""
    
    # 消毒剂类型定义
    DISINFECTANT_TYPES = {
        "含氯消毒剂": {
            "84消毒液": {"concentration": 5.0, "unit": "%", "type": "液体"},
            "漂白粉": {"concentration": 25.0, "unit": "%", "type": "固体"},
            "次氯酸钠溶液": {"concentration": 10.0, "unit": "%", "type": "液体"},
            "二氯异氰尿酸钠": {"concentration": 60.0, "unit": "%", "type": "固体"},
            "三氯异氰尿酸": {"concentration": 90.0, "unit": "%", "type": "固体"},
            "氯胺T": {"concentration": 25.0, "unit": "%", "type": "固体"},
        },
        "醇类": {
            "95%乙醇": {"concentration": 95.0, "unit": "%", "type": "液体"},
            "无水乙醇": {"concentration": 99.5, "unit": "%", "type": "液体"},
        },
        "过氧化物类": {
            "过氧化氢(双氧水)": {"concentration": 30.0, "unit": "%", "type": "液体"},
            "过氧乙酸": {"concentration": 15.0, "unit": "%", "type": "液体"},
            "二氧化氯": {"concentration": 2.0, "unit": "%", "type": "液体"},
        },
        "季铵盐类": {
            "苯扎溴铵(新洁尔灭)": {"concentration": 5.0, "unit": "%", "type": "液体"},
            "双链季铵盐": {"concentration": 10.0, "unit": "%", "type": "液体"},
        },
        "其他": {
            "碘伏": {"concentration": 0.5, "unit": "%", "type": "液体"},
            "碘酊": {"concentration": 2.0, "unit": "%", "type": "液体"},
            "来苏儿(煤酚皂)": {"concentration": 50.0, "unit": "%", "type": "液体"},
            "戊二醛": {"concentration": 2.0, "unit": "%", "type": "液体"},
        }
    }
    
    # 消毒对象推荐浓度数据库 (含氯消毒剂以mg/L计)
    RECOMMENDED_CONCENTRATIONS = {
        "环境表面消毒": {
            "含氯消毒剂": [{"name": "一般物体表面", "value": 500, "time": "10-30分钟"},
                        {"name": "污染表面", "value": 1000, "time": "30分钟"},
                        {"name": "传染病疫区", "value": 2000, "time": "60分钟"}],
            "醇类": [{"name": "一般物体表面", "value": 75, "time": "3-10分钟"}],
            "过氧化物类": [{"name": "一般物体表面", "value": 0.5, "time": "10-30分钟", "note": "过氧乙酸%"}],
            "季铵盐类": [{"name": "一般物体表面", "value": 1000, "time": "10-15分钟"}],
        },
        "餐饮具消毒": {
            "含氯消毒剂": [{"name": "一般消毒", "value": 250, "time": "20分钟"},
                        {"name": "传染病消毒", "value": 500, "time": "30分钟"}],
            "过氧化物类": [{"name": "浸泡消毒", "value": 0.2, "time": "30分钟", "note": "过氧乙酸%"}],
        },
        "织物消毒": {
            "含氯消毒剂": [{"name": "一般织物", "value": 250, "time": "20分钟"},
                        {"name": "传染病织物", "value": 500, "time": "30分钟"},
                        {"name": "血污染物", "value": 2000, "time": "60分钟"}],
        },
        "手消毒": {
            "含氯消毒剂": [{"name": "卫生手消毒", "value": 500, "time": "1分钟"},
                        {"name": "外科手消毒", "value": 1000, "time": "3分钟"}],
            "醇类": [{"name": "卫生手消毒", "value": 75, "time": "1分钟"},
                    {"name": "外科手消毒", "value": 75, "time": "3-5分钟"}],
            "季铵盐类": [{"name": "卫生手消毒", "value": 1000, "time": "1分钟"}],
        },
        "皮肤消毒": {
            "醇类": [{"name": "注射部位", "value": 75, "time": "1分钟"},
                    {"name": "手术部位", "value": 75, "time": "3-5分钟"}],
            "其他": [{"name": "创面消毒", "value": 0.5, "time": "2分钟", "note": "碘伏%"}],
        },
        "医疗器械消毒": {
            "含氯消毒剂": [{"name": "高水平消毒", "value": 2000, "time": "30分钟"},
                        {"name": "中水平消毒", "value": 1000, "time": "20分钟"}],
            "过氧化物类": [{"name": "浸泡消毒", "value": 0.2, "time": "10-30分钟", "note": "过氧乙酸%"},
                        {"name": "高水平消毒", "value": 6, "time": "30分钟", "note": "过氧化氢%"}],
            "其他": [{"name": "高水平消毒", "value": 2.0, "time": "20-45分钟", "note": "戊二醛%"},
                    {"name": "灭菌", "value": 2.0, "time": "10小时", "note": "戊二醛%"}],
        },
        "疫源地消毒": {
            "含氯消毒剂": [{"name": "一般疫区", "value": 1000, "time": "60分钟"},
                        {"name": "严重疫区", "value": 2000, "time": "120分钟"},
                        {"name": "排泄物", "value": 20000, "time": "120分钟"}],
        },
        "饮用水消毒": {
            "含氯消毒剂": [{"name": "常规消毒", "value": 1, "time": "30分钟"},
                        {"name": "应急消毒", "value": 2, "time": "30分钟"}],
        },
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("消毒剂配比计算器 v1.0")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # 数据文件路径
        self.data_dir = os.path.expanduser("~/.disinfectant_calc")
        self.records_file = os.path.join(self.data_dir, "records.json")
        self.presets_file = os.path.join(self.data_dir, "presets.json")
        
        # 确保数据目录存在
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 加载保存的数据
        self.records = self.load_records()
        self.presets = self.load_presets()
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        """创建界面组件"""
        # 创建笔记本(标签页)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标签页1: 配比计算
        self.calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calc_frame, text="配比计算")
        self.create_calc_tab()
        
        # 标签页2: 推荐浓度
        self.recommend_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.recommend_frame, text="推荐浓度")
        self.create_recommend_tab()
        
        # 标签页3: 配比记录
        self.records_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.records_frame, text="配比记录")
        self.create_records_tab()
        
        # 标签页4: 常用方案
        self.presets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.presets_frame, text="常用方案")
        self.create_presets_tab()
        
    def create_calc_tab(self):
        """创建配比计算标签页"""
        # 左侧输入区域
        left_frame = ttk.LabelFrame(self.calc_frame, text="参数输入", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 计算模式选择
        ttk.Label(left_frame, text="计算模式:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.calc_mode = ttk.Combobox(left_frame, values=[
            "已知原液浓度，计算稀释倍数",
            "已知目标浓度和体积，计算原液量"
        ], width=30, state="readonly")
        self.calc_mode.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.calc_mode.current(0)
        self.calc_mode.bind("<<ComboboxSelected>>", self.on_mode_change)
        
        # 分隔线
        ttk.Separator(left_frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=10)
        
        # 消毒剂类型
        ttk.Label(left_frame, text="消毒剂类别:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.category_combo = ttk.Combobox(left_frame, values=list(self.DISINFECTANT_TYPES.keys()), width=20, state="readonly")
        self.category_combo.grid(row=2, column=1, sticky=tk.W, pady=5)
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_change)
        
        ttk.Label(left_frame, text="具体名称:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.disinfectant_combo = ttk.Combobox(left_frame, values=[], width=25, state="readonly")
        self.disinfectant_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        self.disinfectant_combo.bind("<<ComboboxSelected>>", self.on_disinfectant_change)
        
        # 原液浓度
        ttk.Label(left_frame, text="原液浓度:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.source_conc_frame = ttk.Frame(left_frame)
        self.source_conc_frame.grid(row=4, column=1, sticky=tk.W, pady=5)
        self.source_conc_var = tk.StringVar(value="5.0")
        self.source_conc_entry = ttk.Entry(self.source_conc_frame, textvariable=self.source_conc_var, width=10)
        self.source_conc_entry.pack(side=tk.LEFT)
        self.source_conc_unit = ttk.Label(self.source_conc_frame, text="%")
        self.source_conc_unit.pack(side=tk.LEFT, padx=5)
        
        # 目标浓度
        ttk.Label(left_frame, text="目标浓度:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.target_conc_frame = ttk.Frame(left_frame)
        self.target_conc_frame.grid(row=5, column=1, sticky=tk.W, pady=5)
        self.target_conc_var = tk.StringVar(value="500")
        self.target_conc_entry = ttk.Entry(self.target_conc_frame, textvariable=self.target_conc_var, width=10)
        self.target_conc_entry.pack(side=tk.LEFT)
        self.target_conc_unit = ttk.Combobox(self.target_conc_frame, values=["mg/L", "%"], width=8, state="readonly")
        self.target_conc_unit.pack(side=tk.LEFT, padx=5)
        self.target_conc_unit.current(0)
        self.target_conc_unit.bind("<<ComboboxSelected>>", self.on_target_unit_change)
        
        # 目标体积
        ttk.Label(left_frame, text="目标体积:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.target_vol_frame = ttk.Frame(left_frame)
        self.target_vol_frame.grid(row=6, column=1, sticky=tk.W, pady=5)
        self.target_vol_var = tk.StringVar(value="1000")
        self.target_vol_entry = ttk.Entry(self.target_vol_frame, textvariable=self.target_vol_var, width=10)
        self.target_vol_entry.pack(side=tk.LEFT)
        ttk.Label(self.target_vol_frame, text="mL").pack(side=tk.LEFT, padx=5)
        
        # 稀释倍数(模式2显示)
        ttk.Label(left_frame, text="稀释倍数:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.dilution_var = tk.StringVar(value="100")
        self.dilution_entry = ttk.Entry(left_frame, textvariable=self.dilution_var, width=10, state="disabled")
        self.dilution_entry.grid(row=7, column=1, sticky=tk.W, pady=5)
        
        # 按钮区域
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        ttk.Button(btn_frame, text="计算", command=self.calculate, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清空", command=self.clear_calc, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="保存方案", command=self.save_preset, width=12).pack(side=tk.LEFT, padx=5)
        
        # 右侧结果显示区域
        right_frame = ttk.LabelFrame(self.calc_frame, text="计算结果", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.result_text = tk.Text(right_frame, wrap=tk.WORD, font=("Arial", 11), height=20)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.insert(tk.END, "请输入参数后点击计算...\n")
        self.result_text.config(state=tk.DISABLED)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(self.result_text, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # 导出按钮
        ttk.Button(right_frame, text="导出结果", command=self.export_result).pack(pady=5)
        
    def create_recommend_tab(self):
        """创建推荐浓度标签页"""
        # 消毒对象选择
        select_frame = ttk.Frame(self.recommend_frame)
        select_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(select_frame, text="消毒对象:").pack(side=tk.LEFT)
        self.target_object = ttk.Combobox(select_frame, values=list(self.RECOMMENDED_CONCENTRATIONS.keys()), width=30, state="readonly")
        self.target_object.pack(side=tk.LEFT, padx=5)
        self.target_object.bind("<<ComboboxSelected>>", self.on_object_change)
        
        # 结果显示区域
        result_frame = ttk.LabelFrame(self.recommend_frame, text="推荐浓度", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 树形表格
        columns = ("消毒剂类型", "使用场景", "推荐浓度", "作用时间", "备注")
        self.recommend_tree = ttk.Treeview(result_frame, columns=columns, show="headings")
        
        for col in columns:
            self.recommend_tree.heading(col, text=col)
            self.recommend_tree.column(col, width=120)
        
        self.recommend_tree.column("消毒剂类型", width=100)
        self.recommend_tree.column("使用场景", width=150)
        self.recommend_tree.column("推荐浓度", width=100)
        self.recommend_tree.column("作用时间", width=100)
        self.recommend_tree.column("备注", width=150)
        
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.recommend_tree.yview)
        self.recommend_tree.configure(yscrollcommand=scrollbar.set)
        
        self.recommend_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 使用此配置按钮
        ttk.Button(self.recommend_frame, text="使用此配置进行计算", command=self.use_recommendation).pack(pady=10)
        
    def create_records_tab(self):
        """创建配比记录标签页"""
        # 工具栏
        toolbar = ttk.Frame(self.records_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="刷新", command=self.refresh_records).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="删除选中", command=self.delete_record).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="清空记录", command=self.clear_records).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="导出CSV", command=self.export_records_csv).pack(side=tk.LEFT, padx=2)
        
        # 记录列表
        columns = ("时间", "消毒剂", "原液浓度", "目标浓度", "稀释倍数", "配制量", "操作人")
        self.records_tree = ttk.Treeview(self.records_frame, columns=columns, show="headings")
        
        for col in columns:
            self.records_tree.heading(col, text=col)
            self.records_tree.column(col, width=100)
        
        self.records_tree.column("时间", width=150)
        self.records_tree.column("消毒剂", width=150)
        
        scrollbar = ttk.Scrollbar(self.records_frame, orient=tk.VERTICAL, command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=scrollbar.set)
        
        self.records_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # 加载记录
        self.refresh_records()
        
    def create_presets_tab(self):
        """创建常用方案标签页"""
        # 工具栏
        toolbar = ttk.Frame(self.presets_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="刷新", command=self.refresh_presets).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="删除选中", command=self.delete_preset).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="应用选中", command=self.apply_preset).pack(side=tk.LEFT, padx=2)
        
        # 方案列表
        columns = ("方案名称", "消毒剂", "原液浓度", "目标浓度", "目标体积", "创建时间")
        self.presets_tree = ttk.Treeview(self.presets_frame, columns=columns, show="headings")
        
        for col in columns:
            self.presets_tree.heading(col, text=col)
            self.presets_tree.column(col, width=120)
        
        self.presets_tree.column("方案名称", width=150)
        self.presets_tree.column("消毒剂", width=150)
        
        scrollbar = ttk.Scrollbar(self.presets_frame, orient=tk.VERTICAL, command=self.presets_tree.yview)
        self.presets_tree.configure(yscrollcommand=scrollbar.set)
        
        self.presets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # 加载预设
        self.refresh_presets()
        
    # ============== 事件处理 ==============
    
    def on_mode_change(self, event=None):
        """计算模式改变"""
        mode = self.calc_mode.current()
        if mode == 0:  # 模式1: 计算稀释倍数
            self.target_conc_entry.config(state="normal")
            self.target_vol_entry.config(state="disabled")
            self.dilution_entry.config(state="disabled")
        else:  # 模式2: 计算原液量
            self.target_conc_entry.config(state="normal")
            self.target_vol_entry.config(state="normal")
            self.dilution_entry.config(state="disabled")
            
    def on_category_change(self, event=None):
        """消毒剂类别改变"""
        category = self.category_combo.get()
        if category in self.DISINFECTANT_TYPES:
            names = list(self.DISINFECTANT_TYPES[category].keys())
            self.disinfectant_combo.config(values=names)
            if names:
                self.disinfectant_combo.current(0)
                self.on_disinfectant_change()
                
    def on_disinfectant_change(self, event=None):
        """消毒剂名称改变"""
        category = self.category_combo.get()
        name = self.disinfectant_combo.get()
        if category and name and category in self.DISINFECTANT_TYPES:
            if name in self.DISINFECTANT_TYPES[category]:
                info = self.DISINFECTANT_TYPES[category][name]
                self.source_conc_var.set(str(info["concentration"]))
                
    def on_target_unit_change(self, event=None):
        """目标浓度单位改变"""
        pass
        
    def on_object_change(self, event=None):
        """消毒对象改变"""
        obj = self.target_object.get()
        if not obj:
            return
            
        # 清空表格
        for item in self.recommend_tree.get_children():
            self.recommend_tree.delete(item)
            
        # 填充数据
        if obj in self.RECOMMENDED_CONCENTRATIONS:
            for disinfectant_type, items in self.RECOMMENDED_CONCENTRATIONS[obj].items():
                for item in items:
                    conc_str = f"{item['value']} "
                    if "note" in item and "过氧乙酸" in item["note"]:
                        conc_str += "%(过氧乙酸)"
                    elif "note" in item and "戊二醛" in item["note"]:
                        conc_str += "%(戊二醛)"
                    elif "note" in item and "碘伏" in item["note"]:
                        conc_str += "%(碘伏)"
                    elif "note" in item and "过氧化氢" in item["note"]:
                        conc_str += "%(过氧化氢)"
                    elif disinfectant_type == "含氯消毒剂":
                        conc_str += "mg/L"
                    elif disinfectant_type == "醇类":
                        conc_str += "%"
                    elif disinfectant_type == "季铵盐类":
                        conc_str += "mg/L"
                    else:
                        conc_str += "%"
                        
                    note = item.get("note", "")
                    self.recommend_tree.insert("", tk.END, values=(
                        disinfectant_type,
                        item["name"],
                        conc_str,
                        item["time"],
                        note
                    ))
                    
    # ============== 计算功能 ==============
    
    def calculate(self):
        """执行计算"""
        try:
            mode = self.calc_mode.current()
            disinfectant = self.disinfectant_combo.get()
            
            if not disinfectant:
                messagebox.showwarning("警告", "请选择消毒剂")
                return
                
            source_conc = Decimal(self.source_conc_var.get())
            target_unit = self.target_conc_unit.get()
            
            if mode == 0:  # 模式1: 计算稀释倍数
                target_conc = Decimal(self.target_conc_var.get())
                
                # 单位转换
                if target_unit == "mg/L":
                    # 含氯消毒剂: 原液浓度% 转换为 mg/mL (假设密度≈1)
                    # 5% = 50 mg/mL = 50000 mg/L
                    source_conc_mgl = source_conc * Decimal("10000")  # % to mg/L
                    dilution = source_conc_mgl / target_conc
                else:
                    dilution = source_conc / target_conc
                    
                dilution = dilution.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                result = f"""
【计算结果】

消毒剂: {disinfectant}
原液浓度: {source_conc}%
目标浓度: {target_conc} {target_unit}

稀释倍数: 1:{dilution}

【配制方法】
取 1 份 {disinfectant}
加 {dilution - 1} 份水
混匀即可

【示例】
如需配制 1000 mL 消毒液:
需要原液: {Decimal("1000") / dilution:.1f} mL
需要加水: {1000 - float(Decimal("1000") / dilution):.1f} mL
"""
                # 保存记录
                self.add_record(disinfectant, str(source_conc), f"{target_conc} {target_unit}", f"1:{dilution}", "")
                
            else:  # 模式2: 计算原液量
                target_conc = Decimal(self.target_conc_var.get())
                target_vol = Decimal(self.target_vol_var.get())
                
                # 单位转换
                if target_unit == "mg/L":
                    source_conc_mgl = source_conc * Decimal("10000")
                    source_needed = (target_conc * target_vol) / source_conc_mgl
                else:
                    source_needed = (target_conc * target_vol) / source_conc
                    
                source_needed = source_needed.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
                water_needed = target_vol - source_needed
                
                # 计算稀释倍数
                dilution = (target_vol / source_needed).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                
                result = f"""
【计算结果】

消毒剂: {disinfectant}
原液浓度: {source_conc}%
目标浓度: {target_conc} {target_unit}
目标体积: {target_vol} mL

需要原液: {source_needed} mL
需要加水: {water_needed} mL
稀释倍数: 1:{dilution}

【操作步骤】
1. 量取 {source_needed} mL {disinfectant}
2. 加入 {water_needed} mL 清水
3. 充分混匀
4. 标注浓度和配制日期
"""
                # 保存记录
                self.add_record(disinfectant, str(source_conc), f"{target_conc} {target_unit}", f"1:{dilution}", str(target_vol))
                
            self.show_result(result)
            
        except Exception as e:
            messagebox.showerror("错误", f"计算失败: {str(e)}")
            
    def show_result(self, text):
        """显示计算结果"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)
        
    def clear_calc(self):
        """清空计算"""
        self.source_conc_var.set("5.0")
        self.target_conc_var.set("500")
        self.target_vol_var.set("1000")
        self.dilution_var.set("100")
        self.category_combo.set("")
        self.disinfectant_combo.set("")
        self.show_result("请输入参数后点击计算...")
        
    # ============== 数据管理 ==============
    
    def load_records(self):
        """加载配比记录"""
        if os.path.exists(self.records_file):
            try:
                with open(self.records_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
        
    def save_records(self):
        """保存配比记录"""
        with open(self.records_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)
            
    def add_record(self, disinfectant, source_conc, target_conc, dilution, volume):
        """添加配比记录"""
        record = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "disinfectant": disinfectant,
            "source_conc": source_conc,
            "target_conc": target_conc,
            "dilution": dilution,
            "volume": volume,
            "operator": ""
        }
        self.records.insert(0, record)
        self.save_records()
        
    def refresh_records(self):
        """刷新记录列表"""
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
            
        for record in self.records:
            self.records_tree.insert("", tk.END, values=(
                record["time"],
                record["disinfectant"],
                record["source_conc"],
                record["target_conc"],
                record["dilution"],
                record["volume"],
                record.get("operator", "")
            ))
            
    def delete_record(self):
        """删除选中记录"""
        selected = self.records_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的记录")
            return
            
        if messagebox.askyesno("确认", "确定删除选中的记录吗？"):
            for item in selected:
                idx = self.records_tree.index(item)
                if idx < len(self.records):
                    del self.records[idx]
            self.save_records()
            self.refresh_records()
            
    def clear_records(self):
        """清空所有记录"""
        if messagebox.askyesno("确认", "确定清空所有配比记录吗？"):
            self.records = []
            self.save_records()
            self.refresh_records()
            
    def export_records_csv(self):
        """导出记录为CSV"""
        if not self.records:
            messagebox.showwarning("警告", "没有记录可导出")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                import csv
                with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(["时间", "消毒剂", "原液浓度", "目标浓度", "稀释倍数", "配制量", "操作人"])
                    for record in self.records:
                        writer.writerow([
                            record["time"],
                            record["disinfectant"],
                            record["source_conc"],
                            record["target_conc"],
                            record["dilution"],
                            record["volume"],
                            record.get("operator", "")
                        ])
                messagebox.showinfo("成功", f"已导出到: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")
                
    # ============== 预设方案 ==============
    
    def load_presets(self):
        """加载常用方案"""
        if os.path.exists(self.presets_file):
            try:
                with open(self.presets_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
        
    def save_presets(self):
        """保存常用方案"""
        with open(self.presets_file, 'w', encoding='utf-8') as f:
            json.dump(self.presets, f, ensure_ascii=False, indent=2)
            
    def save_preset(self):
        """保存当前配置为方案"""
        disinfectant = self.disinfectant_combo.get()
        if not disinfectant:
            messagebox.showwarning("警告", "请先选择消毒剂并完成计算")
            return
            
        # 弹窗输入方案名称
        dialog = tk.Toplevel(self.root)
        dialog.title("保存方案")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="方案名称:").pack(pady=10)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        name_entry.insert(0, f"{disinfectant}配比方案")
        
        def do_save():
            name = name_entry.get().strip()
            if not name:
                messagebox.showwarning("警告", "请输入方案名称")
                return
                
            preset = {
                "name": name,
                "disinfectant": disinfectant,
                "source_conc": self.source_conc_var.get(),
                "target_conc": self.target_conc_var.get(),
                "target_unit": self.target_conc_unit.get(),
                "target_vol": self.target_vol_var.get(),
                "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.presets.insert(0, preset)
            self.save_presets()
            self.refresh_presets()
            dialog.destroy()
            messagebox.showinfo("成功", "方案已保存")
            
        ttk.Button(dialog, text="保存", command=do_save).pack(pady=10)
        
    def refresh_presets(self):
        """刷新方案列表"""
        for item in self.presets_tree.get_children():
            self.presets_tree.delete(item)
            
        for preset in self.presets:
            self.presets_tree.insert("", tk.END, values=(
                preset["name"],
                preset["disinfectant"],
                preset["source_conc"],
                f"{preset['target_conc']} {preset['target_unit']}",
                preset.get("target_vol", ""),
                preset["created"]
            ))
            
    def delete_preset(self):
        """删除选中方案"""
        selected = self.presets_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的方案")
            return
            
        if messagebox.askyesno("确认", "确定删除选中的方案吗？"):
            for item in selected:
                idx = self.presets_tree.index(item)
                if idx < len(self.presets):
                    del self.presets[idx]
            self.save_presets()
            self.refresh_presets()
            
    def apply_preset(self):
        """应用选中方案"""
        selected = self.presets_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要应用的方案")
            return
            
        idx = self.presets_tree.index(selected[0])
        if idx >= len(self.presets):
            return
            
        preset = self.presets[idx]
        
        # 设置参数
        self.source_conc_var.set(preset["source_conc"])
        self.target_conc_var.set(preset["target_conc"])
        self.target_conc_unit.set(preset["target_unit"])
        if preset.get("target_vol"):
            self.target_vol_var.set(preset["target_vol"])
            
        # 查找并设置消毒剂
        disinfectant = preset["disinfectant"]
        for category, items in self.DISINFECTANT_TYPES.items():
            if disinfectant in items:
                self.category_combo.set(category)
                self.disinfectant_combo.config(values=list(items.keys()))
                self.disinfectant_combo.set(disinfectant)
                break
                
        # 切换到计算标签
        self.notebook.select(0)
        messagebox.showinfo("提示", "方案已应用，请检查参数后点击计算")
        
    def use_recommendation(self):
        """使用推荐配置"""
        selected = self.recommend_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择一条推荐配置")
            return
            
        values = self.recommend_tree.item(selected[0])["values"]
        if not values:
            return
            
        disinfectant_type, scene, conc_str, time, note = values
        
        # 解析浓度
        import re
        match = re.match(r'([\d.]+)\s*(.+)', conc_str)
        if match:
            conc_val = match.group(1)
            conc_unit = match.group(2)
            
            # 设置单位
            if "mg/L" in conc_unit:
                self.target_conc_unit.set("mg/L")
            else:
                self.target_conc_unit.set("%")
                
            self.target_conc_var.set(conc_val)
            
        # 切换到计算标签
        self.notebook.select(0)
        messagebox.showinfo("提示", "推荐配置已应用，请选择具体消毒剂后点击计算")
        
    def export_result(self):
        """导出计算结果"""
        result = self.result_text.get(1.0, tk.END).strip()
        if not result or result == "请输入参数后点击计算...":
            messagebox.showwarning("警告", "没有结果可导出")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("消毒剂配比计算结果\n")
                    f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(result)
                messagebox.showinfo("成功", f"已导出到: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")


def main():
    """主函数"""
    root = tk.Tk()
    
    # 设置主题
    style = ttk.Style()
    style.theme_use('clam')
    
    app = DisinfectantCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
