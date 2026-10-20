# -*- coding: utf-8 -*-
"""
explore_2026.py - 2026 岗位表分析
Day 2: 考区分布
Day 3: 学历要求分布 + 招录人数求和
Day 4: 「其他要求」门槛拆解 + 我的最终可用池
"""
import os
import pandas as pd

# 用 __file__ 拼绝对路径，不管从哪个目录运行都找得到文件
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', '2026_positions.xlsx')


def load():
    # 2026 第 0 行是免责声明，必须 header=1
    df = pd.read_excel(DATA_PATH, engine='openpyxl', header=1)
    return df


def by_region(df):
    # 数岗位个数：一列里每个值出现几次
    return df['考区'].value_counts()


def by_education(df):
    return df['学历低限'].value_counts()


def by_recruitment(df):
    # 按考区分组，只对"招录人数"这一列求和，再降序排
    return df.groupby('考区')['招录人数'].sum().sort_values(ascending=False)


def by_major(df, keyword='计算机'):
    # 造掩码：专业要求里含 keyword 的行是 True，其余 False
    mask = df['专业要求'].str.contains(keyword, na=False)
    return df[mask]


def my_real_pool(df):
    # 三不限：专业要求这一列是空的（政府表没写专业限制）
    mask_unlimited = df['专业要求'].isnull()
    # 计算机类：专业要求里含"计算机"三个字
    mask_cs = df['专业要求'].str.contains('计算机', na=False)
    return df[mask_unlimited | mask_cs]


def check_keywords(df):
    """门槛侦察：打印每个关键词在全省的命中数。

    铁律：命中数非零的关键词，必须再打印 value_counts() 看原文，
    确认它是「硬限制」还是「软提示」，不能凭字面下判断。
    Day4 因此救回了 82 + 134 + 37 个被误杀的岗位。
    """
    req = df['其他要求'].fillna('')
    print('非空行数：', (req != '').sum())
    for kw in ['应届毕业生', '男性', '适合男性', '女性', '户籍', '生源',
               '中共党员', '共青团员', '服务基层项目', '退役大学生士兵']:
        print(' ', kw, '→', req.str.contains(kw).sum())


def my_pool(df, as_fresh):
    """我的可用池。

    as_fresh=True  应届视角：我是当年应届生，应届限制对我无效
    as_fresh=False 往届视角：应届限制生效，把限应届的岗全砍掉

    写法要点：keep 一层层往下收窄，每层都打印 keep.sum()。
    这样漏斗最后一行必然等于最终结果，不会像之前那样出现
    「漏斗打印 668、实际结果 683」的两边不一致。
    """
    req = df['其他要求'].fillna('')

    # 专业：三不限 或 计算机类
    m_major = df['专业要求'].isnull() | df['专业要求'].str.contains('计算机', na=False)

    # 应届：必须用"应届毕业生"。写"应届硕士、博士研究生"的是年龄放宽条款，不是限制
    m_fresh = req.str.contains('应届毕业生')

    # 性别：'男性'是硬限制，'适合男性'只是工作强度提示（134 个），要放行
    m_male = req.str.contains('男性') & ~req.str.contains('适合男性')
    m_female = req.str.contains('女性')

    # 定向招录（三支一扶/大学生村官/西部计划实测为 0，不必再加）
    m_target = req.str.contains('服务基层项目|退役大学生士兵')

    # 政治面貌：'中共党员或共青团员' 我作为团员能报（37 个），排除时要留着
    m_party = req.str.contains('中共党员') & ~req.str.contains('共青团员')

    # 户籍：不限户籍的放行，限张家口市/阳原县的放行，限其他县区的一律排除
    m_hukou = req.str.contains('户籍|生源')
    m_hukou_ok = (~m_hukou) | req.str.contains('张家口市所辖|阳原县')

    keep = m_major
    print('  专业池        ', keep.sum())
    if not as_fresh:
        keep = keep & (~m_fresh)
        print('  - 限应届      ', keep.sum())
    keep = keep & (~m_male)
    print('  - 限男性      ', keep.sum())
    keep = keep & (~m_target)
    print('  - 定向招录    ', keep.sum())
    keep = keep & (~m_party)
    print('  - 党员限制    ', keep.sum())
    keep = keep & m_hukou_ok
    print('  - 外地户籍    ', keep.sum())

    favor = keep & m_female          # 限女性：我的性别红利岗
    fresh_only = keep & m_fresh      # 仅限应届：2028 年才对我开放的岗
    print('  其中限女性（性别红利）：', favor.sum())
    print('  其中仅限应届（应届专属）：', fresh_only.sum())
    return df[keep], df[favor]


def main():
    df = load()

    print('=== 0. 门槛关键词命中数（全省 6487 个岗位）===')
    check_keywords(df)

    print()
    print('=== 1. 各考区岗位数 ===')
    print(by_region(df))
    print('合计岗位数：', df.shape[0])

    print()
    print('=== 2. 学历要求分布 ===')
    print(by_education(df))

    print()
    print('=== 3. 各考区招录人数 ===')
    print(by_recruitment(df))
    print('全省招录总数：', df['招录人数'].sum())

    print()
    print('=== 4. 计算机类岗位 ===')
    cs = by_major(df)
    print('岗位数：', cs.shape[0])
    print('招录人数：', cs['招录人数'].sum())
    print(cs['考区'].value_counts())

    print()
    print('=== 5. 我的真实岗位池（只看专业）===')
    mask_unlimited = df['专业要求'].isnull()
    mask_cs = df['专业要求'].str.contains('计算机', na=False)
    print('三不限岗位：', mask_unlimited.sum(), '个')
    print('计算机岗位：', mask_cs.sum(), '个')

    pool = my_real_pool(df)
    print('合并池子：', pool.shape[0], '个岗位')
    print('招录人数：', pool['招录人数'].sum())
    print('平均每岗招：', round(pool['招录人数'].sum() / pool.shape[0], 2), '人')
    print(pool['考区'].value_counts())

    print()
    print('=== 6. 往届视角（假设 2028 年没考上，应届限制生效）===')
    pool_past, favor_past = my_pool(df, as_fresh=False)
    print('岗位：', pool_past.shape[0], '个，', pool_past['招录人数'].sum(), '人')
    print('平均每岗招：', round(pool_past['招录人数'].sum() / pool_past.shape[0], 2), '人')

    print()
    print('=== 7. 应届视角（2028 年首次报考，应届限制无效）===')
    pool_fresh, favor_fresh = my_pool(df, as_fresh=True)
    print('岗位：', pool_fresh.shape[0], '个，', pool_fresh['招录人数'].sum(), '人')
    print('平均每岗招：', round(pool_fresh['招录人数'].sum() / pool_fresh.shape[0], 2), '人')
    print(pool_fresh['考区'].value_counts())


if __name__ == '__main__':
    main()
