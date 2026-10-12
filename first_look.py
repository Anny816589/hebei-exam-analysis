# -*- coding: utf-8 -*-
"""
first_look.py — 2026 河北省考岗位表首次勘查
============================================

只做"读 + 打印基础信息"，不做任何清洗或筛选。
按种子文档约束，输出严格四项：
  [1] shape (行, 列)
  [2] 各列名 + dtype
  [3] head(3) 预览
  [4] isnull().sum() 各列缺失值 + 总缺失值

【运行环境】
项目当前固定使用 hermes-agent venv 下的 Python（含 pandas/openpyxl/xlrd）：

    "C:/Users/lenovo/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe" first_look.py

PATH 上另有 managed python 3.13.12（无 pandas），用裸 `python` 会跑错。
"""
import pandas as pd

# ---------- 路径常量（英文文件名；中文表头交给 pandas 本身处理） ----------
FILE = "data/2026_positions.xlsx"

# 期望的列名集合 —— 如果政府发布版本列名变了，这里会立即报警
EXPECTED_COLS = {
    "职位代码", "考区", "部门", "单位", "职位名称",
    "招录人数", "学历低限", "学位低限", "专业要求",
    "其他要求", "申论试卷类型",
}


def load() -> pd.DataFrame:
    """读 2026 岗位表。

    注意：xlsx 第 1 行（0-indexed = 0）是免责声明，
    真正的列名在第 2 行（0-indexed = 1），所以 header=1。
    """
    df = pd.read_excel(FILE, engine="openpyxl", header=1)
    # 校验：列名集合必须与 EXPECTED_COLS 完全一致（顺序无所谓）
    actual = set(df.columns)
    missing = EXPECTED_COLS - actual
    extra = actual - EXPECTED_COLS
    if missing or extra:
        raise ValueError(
            f"列名变化报警\n"
            f"  缺列: {missing}\n"
            f"  多列: {extra}\n"
            f"  实际: {sorted(actual)}"
        )
    return df


def report(df: pd.DataFrame) -> None:
    """打印 first_look 的四项核心观察。"""
    bar = "=" * 64
    print(bar)
    print(f"  文件: {FILE}")
    print(f"  shape: {df.shape}   <-- (行, 列)")
    print(bar)

    # [1] 列名 + dtype
    print("\n[1] 列名 + dtype")
    for col, dtype in df.dtypes.items():
        print(f"  {col!r:<14s} {dtype}")

    # [2] head(3)
    print("\n[2] head(3)")
    with pd.option_context(
        "display.max_columns", None,
        "display.width", 200,
        "display.max_colwidth", 30,
    ):
        print(df.head(3))

    # [3] 缺失值
    print("\n[3] 各列缺失值计数")
    nulls = df.isnull().sum()
    bad = nulls[nulls > 0]
    if len(bad):
        print(bad.to_string())
    else:
        print("  (无缺失)")
    print(f"\n  总缺失值: {nulls.sum()}")


def main() -> None:
    df = load()
    report(df)


if __name__ == "__main__":
    main()
