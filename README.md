# 遗忘的边界 · 有限容量下的记忆、智能与自我

> **DOI**：10.5281/zenodo.24227371　·　概念 DOI：10.5281/zenodo.23323276　·　324 页 / 7 部分 / 25 章 / 附录 A–F

本书处理一个被反复提出、却极少被严格表述的问题：大语言模型的键值缓存、AI 智能体的上下文窗口与人类的记忆—学习系统，是否由同一机制主导？本书给出的答案是一次有意的“降级”：三者不是同构（isomorphic）的，而是同约束（iso-constrained）的。它们都受制于同一组信息论约束——有限通道容量下的压缩、干扰与遗忘——却运行在相差九个数量级的时间尺度上，从而形成一个从毫秒（工作记忆）到终身（系统巩固）的“容量级联”。遗忘因此不是记忆的失败，而是学习的边界条件：一个不肯丢信息的系统，也丢不掉噪声；一个不肯改变的系统，也无法适应。本书的贡献不是宣布一个大一统理论，而是把这一主张拆解为可分级、可批判、可证伪的命题：逐一给出形式化定义（信息瓶颈、率失真、有效容量、表示坍塌、时间尺度分离），区分“已知／论证／假说／待验证”四类断言，并明确写出框架能解释什么、不能解释什么。在此过程中，本书把四个长期被排除在统一叙事之外的环节正式纳入：（一）清醒与睡眠构成两种不同的计算模式，梦不是副产品而是内源模拟与正则化的候选机制；（二）离线计算至少有两个方向——没有真值时向内重组（梦），有真值时向外对账（2026 年第一批在役智能体系统采用的整合方式），而区分二者的判据不是“像不像梦”，是“有没有账可对”；本书为此给出定义、上界与一次可复算的替身实验（收益近似正比于可验证性，Δa≈0.16ρ）；（三）潜意识是表达空间之外的高维计算，意识反而是对它的低维投影；（四）元认知是对容量使用本身的监控与再分配。全书以一张“母题下的理论地图”收束：信息瓶颈、自由能原理、Hopfield 网络、工作记忆模型、遗忘曲线、干扰论、系统巩固、强化学习、预测加工等二十余个理论，被安放在“信息约束下的多尺度自适应”这一母题的不同位置，各得其所，且各自标明其边界。结语主张：最好的理论不是权威的陈述，而是一份开放的邀请。卷首《总纲　现实中不存在无限》把有限容量写成生成条件而非背景：三个载体之所以同约束，正因为它们都有限；遗忘是有限记忆载体必须支付的账单。

---

## 结构

| 部分 | 标题 | 章数 | 起 → 止 |
|---|---|---:|---|
| 1 | 第一部分　问题的重述与框架的限定 | 3 | 三个观察 → 证据分级与可证伪性 |
| 2 | 第二部分　信息论基础：容量、干扰与时间 | 3 | 信息瓶颈与率失真 → 多时间尺度与自适应级联 |
| 3 | 第三部分　三个系统的分析 | 3 | 大语言模型 → 人类记忆 |
| 4 | 第四部分　跨越尺度的机制：离线、窗口与调度 | 5 | 清醒与睡眠 → 元认知与容量的自适应管理 |
| 5 | 第五部分　理论地图与批判对话 | 3 | 理论地图 → 与神经科学及意识理论的对话 |
| 6 | 第六部分　含义、局限与未来 | 3 | 设计含义 → 局限、开放问题与研究路线图 |
| 7 | 第七部分　记忆的延伸 | 6 | 记忆的训练与迁移 → 记忆研究的未来 |

以上是本版（2026-11-12）的结构。**第 12 章是本版新增的**，第四部分因此由 4 章扩为 5 章，旧 ch12—ch25 顺移为 ch13—ch26。

每章八段：主提问 → 场景开篇 → 导论 → 机制 → 表/图 → 反例 → 本章小结 → 一句话带走。
每个部分有满栏插图扉页（`assets/svg/part-NN.svg`）、一段部分导语与一段部分小结。

## 证据与自检

- 结论标注 **A/B/C** 证据等级与甲/乙/丙概念等级；结论强度不超过证据强度。
- 可证伪登记簿：`docs/preregistration/checkups.csv`（append-only）。
- 结构校阅：系列 lint 24 条规则，本书 **error 0 / warn 0**（见 `_series/lint/REPORT.md`）。

## 文件

| 路径 | 是什么 |
|---|---|
| `source/` | **唯一正文来源**（HTML）；`book.json` 元数据、`parts.json` 结构 |
| `analysis/` | 图表、统计、抓取脚本（可重跑） |
| `assets/` | 封面、SVG 图、CSS |
| `scripts/build.sh` | audit → 印刷 PDF → 电子版 → EPUB → Markdown |
| `docs/` | 方法、数据来源、缺口与登记簿 |

产物（`output/`、`release/`）不入库，可由 `source/` 重建。

## 引用

```
遗忘的边界：有限容量下的记忆、智能与自我。李毅芃，2026。10.5281/zenodo.23936852
```

## 系列（九本书）

| 书 | 仓库 |
|---|---|
| 只能选两样 | [knowledge-tradeoffs](https://github.com/lyp0746/knowledge-tradeoffs) |
| 区分的语言 | [distinction-evolution](https://github.com/lyp0746/distinction-evolution) |
| 错位的时间 | [entropy-spiral](https://github.com/lyp0746/entropy-spiral) |
| 选择的代价 | [impossibility-triangle](https://github.com/lyp0746/impossibility-triangle) |
| 诠释的权衡 | [interpretation-tradeoff](https://github.com/lyp0746/interpretation-tradeoff) |
| 涌现的临界 | [emergence-critical](https://github.com/lyp0746/emergence-critical) |
| 心灵的分岔 | [mind-forks](https://github.com/lyp0746/mind-forks) |
| 热点的账单 | [hotspot-bills](https://github.com/lyp0746/hotspot-bills) |

十五篇工作论文与全部条目的 DOI 见 [series-workspace](https://github.com/lyp0746/series-workspace)。

## 许可

正文与图件 CC BY 4.0；脚本 MIT。

<!-- viz-console -->
## 可视化阅读台 / Reading console

`遗忘的边界` 每件都有两个入口，**离线单文件、断网可开、零外部依赖**：

| 入口 | 文件 | 里面是什么 |
|---|---|---|
| 阅读页 | [`assets/capacity-cascade-reader.html`](assets/capacity-cascade-reader.html) | 三档切换（骨架／阅读／全展）＋ 每章末尾「审问卡」（带走／打脸条件／封顶／动手，四行全部原文摘录，可一键复制给自己的 AI 当严苛伴读） |
| 结构地图 | [`assets/capacity-cascade-explorer.html`](assets/capacity-cascade-explorer.html) | 章际引用的 3D 螺旋、部 × 部矩阵、附录原表台账（可搜）、图件账 |

两个页面顶部互跳；`375px` 窄屏与桌面都验过，0 外部请求。

Every item ships two offline single-file entries: a **reading console** (three density levels + a per-chapter audit card quoting the text verbatim) and a **structure map** (chapter-citation spiral, part × part matrix, appendix ledgers). No server, no external requests — double-click and it runs.

