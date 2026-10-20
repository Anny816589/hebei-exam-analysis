# -*- coding: utf-8 -*-
"""inspect_years.py - 侦察 2024 / 2025 表结构（只读，不改任何数据）"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 年份 -> (文件名, 引擎)。.xls 必须用 xlrd，.xlsx 用 openpyxl
YEARS = {
    2024: ('2024_positions.xls', 'xlrd'),
    2025: ('2025_positions.xlsx', 'openpyxl'),
}

for year, (fname, engine) in YEARS.items():
    path = os.path.join(BASE_DIR, 'data', fname)
    print('=' * 60)
    print(year, fname)

    # header=None：不把任何一行当表头，原样读进来
    raw = pd.read_excel(path, engine=engine, header=None)
    print('总行数：', raw.shape[0], ' 总列数：', raw.shape[1])
    print('--- 原始前 3 行（看第几行才是真表头）---')
    for i in range(3):
        print('第 %d 行：' % i, raw.iloc[i].tolist())

    print()
    print('--- 用 header=0 读，列名是 ---')
    d0 = pd.read_excel(path, engine=engine, header=0)
    print(d0.columns.tolist(), '| 行数', d0.shape[0])

    print('--- 用 header=1 读，列名是 ---')
    d1 = pd.read_excel(path, engine=engine, header=1)
    print(d1.columns.tolist(), '| 行数', d1.shape[0])
    print()
