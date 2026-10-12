\# Week 2 开发日志



\## Day 1 (2026-10-12)



\### 完成

\- 环境验证：PATH 上有 4 个 python，目前 `python` 指向 uv cpython-3.11（含 pandas，可用）

\- first\_look.py：2026 岗位表基础勘查（shape 6487×11，缺失 2585）

\- first\_look\_v2.py：三年汇总（2024=6372/2413、2025=7143/3190、2026=6487/2585）



\### 踩坑

\- 2026 xlsx 第 0 行是免责声明，必须 `header=1`；2024 是 .xls 老格式，必须 `engine='xlrd'`

\- 重要数字必须文本复制粘贴，截图 OCR 两次失真

\- 多个 python 共存 + cwd 切换时，先 `pwd` 再写路径



\### 明天 Day 2

\- 2026 深入：考区分布、学历要求、招录人数

\- 启动 PROBLEMS.md：固化 4 个 python 解释器问题



