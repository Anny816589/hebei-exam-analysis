# -*- coding: utf-8 -*-
"""compare_years.py - 跨年侦察：确认三年口径是否一致"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 年份 -> (文件名, 引擎, 表头行)。只有 2026 有免责声明行，必须 header=1
YEARS = {
    2024: ('2024_positions.xls', 'xlrd', 0),
    2025: ('2025_positions.xlsx', 'openpyxl', 0),
    2026: ('2026_positions.xlsx', 'openpyxl', 1),
}

KEYWORDS = ['应届毕业生', '男性', '适合男性', '女性', '中共党员', '共青团员',
            '户籍', '生源', '服务基层项目', '退役大学生士兵', '基层工作经历']

for year in sorted(YEARS):
    fname, engine, header = YEARS[year]
    df = pd.read_excel(os.path.join(BASE_DIR, 'data', fname),
                       engine=engine, header=header)
    req = df['其他要求'].fillna('')
    print('=' * 50)
    print(year, '| 岗位', df.shape[0], '| 招录', df['招录人数'].sum(),
          '| 其他要求非空', (req != '').sum())
    for kw in KEYWORDS:
        print('  ', kw, '→', req.str.contains(kw).sum())
    print('  考区取值：', df['考区'].value_counts().to_dict())
    print('  学历取值：', df['学历低限'].value_counts().to_dict())
