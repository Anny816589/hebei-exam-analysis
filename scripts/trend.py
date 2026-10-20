# -*- coding: utf-8 -*-
"""trend.py - 三年趋势：考区归一化 + 石家庄/张家口对比 + 查漏项"""
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YEARS = {
    2024: ('2024_positions.xls', 'xlrd', 0),
    2025: ('2025_positions.xlsx', 'openpyxl', 0),
    2026: ('2026_positions.xlsx', 'openpyxl', 1),
}


def load(year):
    fname, engine, header = YEARS[year]
    df = pd.read_excel(os.path.join(BASE_DIR, 'data', fname),
                       engine=engine, header=header)
    # 2024 写作"雄安新区（保定）"，统一后才能跨年比
    df['考区'] = df['考区'].str.replace('雄安新区（保定）', '雄安新区', regex=False)
    return df


for year in sorted(YEARS):
    df = load(year)
    pos = df['考区'].value_counts()
    rec = df.groupby('考区')['招录人数'].sum()
    print('=' * 40)
    print(year, '全省 岗位', df.shape[0], '招录', df['招录人数'].sum(),
          '每岗', round(df['招录人数'].sum() / df.shape[0], 2))
    for city in ['石家庄', '张家口']:
        print('  %s：岗位 %d，招录 %d' % (city, pos.get(city, 0), rec.get(city, 0)))
    m = df['专业要求'].str.contains('计算机', na=False)
    print('  计算机岗：', m.sum(), '个，招录', df[m]['招录人数'].sum(), '人')

df26 = load(2026)
req = df26['其他要求'].fillna('')
print()
print('--- 2026 含"基层工作经历"的原文 ---')
print(req[req.str.contains('基层工作经历')].value_counts())
