# 遗忘的边界 · The Boundary of Forgetting

> 有限容量下的记忆、智能与自我
> Memory, Intelligence, and the Self under Finite Capacity

> 支撑本书的形式结构称为**容量级联**（capacity cascade）。仓库代号 `capacity-cascade` 即由此而来。

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23323276.svg)](https://doi.org/10.5281/zenodo.23323276)
[![License: CC BY 4.0](https://img.shields.io/badge/Content-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)
[![License: MIT](https://img.shields.io/badge/Code-MIT-green.svg)](LICENSE-MIT)

## 项目概述

大语言模型的键值缓存、AI 智能体的上下文窗口、以及人类的记忆—学习系统，是否由同一机制主导？

本书给出的是一次有意的**降级**：三者不是**同构**（isomorphic）的，而是**同约束**（iso-constrained）的。它们受制于同一组信息论约束——有限通道容量下的压缩、干扰与遗忘——却运行在相差约九个数量级的时间尺度上，形成一个从毫秒（工作记忆）到终身（系统巩固）的**容量级联**（capacity cascade）。

本书的贡献不是宣布一个大一统理论，而是把这一主张拆解为**可分级、可批判、可证伪**的命题，并明确写出框架能解释什么、不能解释什么。

> **English.** Are the KV cache of an LLM, the context window of an AI agent, and human memory–learning governed by the same mechanism? This monograph argues for a deliberate *demotion*: the three are not **isomorphic** but **iso-constrained** — bound by the same information-theoretic constraints (compression, interference, forgetting under finite capacity) while operating across roughly nine orders of magnitude in timescale, forming a **capacity cascade** from milliseconds (working memory) to a lifetime (systems consolidation).

## 核心主张

| 层 | 内容 | 强度 |
|---|---|---|
| 约束 | 有限有效容量下的压缩—相关性权衡（信息瓶颈） | A / 甲 |
| 时间 | 至少两个分离的时间尺度；丢弃是层间唯一的传送带 | B / 乙 |
| 系统 | LLM 位置偏差、智能体漂移、人类巩固的多机制分析 | B–C / 乙 |
| 协调 | 清醒—睡眠二元计算、内源模拟、元认知 | C / 丙（假说） |
| 地图 | 二十余个既有理论在母题下各得其所 | C / 甲–乙 |

## 目录结构

```
source/          唯一权威正文来源（HTML）
  book.json        书名 / 副标题 / 作者 / 摘要 / 关键词
  parts.json       部分 → 章 → 节
  front_*.html     版权、执行摘要、前言、十分钟、理论地图、术语
  ch01.html …      第 1—19 章
  back_*.html      结语、后记
  appendix_*.html  附录 A—G
assets/css/      paper.css / book.css / ereader.css（印刷与电子阅读版式）
assets/svg/      全部插图与满版封面（可复现生成）
analysis/        audit.py（校对）、make_figures.py、make_cover.py
scripts/         build.sh / validate.sh / release.sh / create_github_release.py
docs/            读者说明、方法、数据来源、修订说明、数据缺口、开放贡献
output/          构建产物（gitignore）
release/         发布包（gitignore）
versions/        CHANGELOG.md（内部版次记录，不进正文）
```

## 构建

```bash
# 生成插图与封面（确定性）
python analysis/make_figures.py && python analysis/make_cover.py

# 校对 → 印刷版 PDF → 电子阅读版 PDF → EPUB → Markdown
bash scripts/build.sh

# 质量门禁（校对 + EPUB 结构校验）
bash scripts/validate.sh

# 组装发布包到 release/
bash scripts/release.sh
```

PDF 由**无头 Chrome/Edge** 打印（含分级书签），非 weasyprint。`.env.build` 指向带 `lxml` / `pypdf` 的 Python 解释器。

## 发布与归档

本仓库采用 **一个产物一个 tag**：每个发布产物（印刷版 PDF、电子阅读版 PDF、EPUB、HTML、Markdown、封面等）各自对应一个 Git tag 与一个只承载该产物的 GitHub Release，使每个产物都能被独立引用与归档。

```bash
# 列出产物清单
python scripts/create_github_release.py --list
# 为每个产物创建 release（token 取自 git credential helper，不落盘）
python scripts/create_github_release.py --date 2026-10-14
```

工作约定（工具链路径、仓库规则）见 [`AGENTS.md`](AGENTS.md)。

## 方法

本书采用两套正交的等级：

- **证据等级** A（官方可复现）／B（稳定公开估计）／C（稀疏／构造／思辨）
- **概念等级** 甲（形式化且可检验）／乙（有框架，暂无独立判定）／丙（启发式类比）

以及四类断言标记：［已知］／［论证］／［假说］／［待验证］。所有可检验预言登记在附录 E；所有 C 级量级集中列于附录 F。

## 许可

- 正文与图表：**CC BY 4.0**
- 构建脚本与代码：**MIT**

## 引用

**DOI：** [10.5281/zenodo.23323276](https://doi.org/10.5281/zenodo.23323276)

```
李毅芃. 《遗忘的边界：有限容量下的记忆、智能与自我》. 2026-10-14.
Zenodo. https://doi.org/10.5281/zenodo.23323276. CC BY 4.0.
```

机器可读格式见 [`CITATION.cff`](CITATION.cff)。

---

## 本系列

- **通俗读本《只能选两样》**：从来不及、会忘记到说不清——五个核心，看懂复杂世界的取舍。
  面向所有人（小朋友 / 学生 / 成年人 / 专家），含 12 幅图解与 5 分钟小实验。
- **系列入口与外部登记库**：[github.com/lyp0746/knowledge-tradeoffs](https://github.com/lyp0746/knowledge-tradeoffs) —— 最小可验证单元、跨域盲测登记（append-only）、合并术语表、五核关系图。

---

## 归档 DOI（最新）

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23323276.svg)](https://doi.org/10.5281/zenodo.23323276)

本书的**最新版本**以该 DOI 为准（Zenodo 自动指向最新版本）；引用格式见 `CITATION.cff`。
本系列的通俗读本《只能选两样》与外部登记库见 [lyp0746/knowledge-tradeoffs](https://github.com/lyp0746/knowledge-tradeoffs)。
