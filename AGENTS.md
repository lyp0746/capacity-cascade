# AGENTS.md — 本仓库工作约定与工具链（记忆）

> pi 会把本文件作为目录级上下文/记忆自动加载（无需项目信任）。改动后新会话生效。

## 工具链（本机实测，2026-10）

- **Git**：`D:\Git\cmd\git.exe`（不在 WSL 的 PATH 里，请用绝对路径 `/mnt/d/Git/cmd/git.exe`）
  - remote：`https://github.com/lyp0746/capacity-cascade.git`，默认分支 `main`
  - 凭据已缓存，可直接 `push`；脚本里加 `GIT_TERMINAL_PROMPT=0` 防卡住
- **Python（构建/分析）**：`/mnt/d/0_Code/Iris Series/.venv/Scripts/python.exe`
  - 已装：numpy pandas scipy matplotlib bs4 lxml pypdf requests（**无** weasyprint / markdown）
  - `.env.build` 的 `PYTHON` 已指向该解释器
  - 注意：WSL 的 `export VAR=...` **不会**传入 Windows Python（interop）；需要 token 时在 Python 里自己调 git credential fill
- **PDF 生成**：`build_book.py --pdf` 调**无头 Chrome**（`C:\Program Files\Google\Chrome\Application\chrome.exe`）打印，**不是** weasyprint

## 常用命令

```bash
PY="/mnt/d/0_Code/Iris Series/.venv/Scripts/python.exe"
GIT="/mnt/d/Git/cmd/git.exe"

"$PY" analysis/make_figures.py   # 生成 assets/svg/fig*.svg
"$PY" analysis/make_cover.py     # 生成 assets/svg/cover.svg
"$PY" analysis/audit.py          # 校对：术语/编号/交叉引用 → 刷新 校对清单.md
bash scripts/build.sh            # audit→印刷PDF→电子阅读PDF→EPUB→Markdown
bash scripts/validate.sh         # 校对 + EPUB 结构校验
bash scripts/release.sh          # 组装 release/（刷新发布包）
"$PY" scripts/create_github_release.py --list                 # 资产清单
"$PY" scripts/create_github_release.py --date 2026-10-14      # 单一 release、单一 tag
```

## 仓库约定

- **`source/*.html` 是唯一权威正文来源**；`output/`、`release/` 是派生产物（见 `.gitignore`）。
- 图表：脚本输出 `assets/svg/*.svg`；正文用相对路径 `assets/svg/...` 引用。
- 改正文后顺序：`analysis/make_figures.py`（如改图）→ `analysis/audit.py`（应无“引用但未定义的表/图”、无“无效章节引用”）→ `bash scripts/build.sh`。
- 结论标注：证据等级 A/B/C 与概念等级 甲/乙/丙 双重标注；全书数字必须带等级。
- **一个 release、一个 tag（本仓库采用）**：`scripts/create_github_release.py` 建**一个** tag（日期作后缀，`edition-YYYY-MM-DD`）与**一个** release，release 内承载**全部**产物（印刷/电子阅读 PDF、EPUB、HTML、Markdown、封面、文档）。该 release 标为 GitHub **Latest**。
  - 只保留最新一套；不另建多套 tag。旧的多产物 tag（`edition-<kind>-<date>`）已废弃。
- **硬不变式——一个 tag 对应且仅对应一个 release**：无孤立 tag、无无 tag 的 release。发布后校验：`"$PY" scripts/create_github_release.py --verify`。
- **同版重发 = 把同一个 tag 移到新提交并替换资产**（删旧资产、传新资产），不另建第二套 tag（含只改完成日期）。
- **可证伪登记簿**（`source/appendix_e_preregistration.html`）与发布包中的对应条目为 **append-only**：只追加，绝不改写旧行。
- **正文与元数据不含版本号**；日期使用真实完成日期（`source/book.json` 单一来源）。

## 写作风格（重要）

见 skill `academic-book-pipeline` 的 `references/voice.md`。要点：

- **张力，不宿命**：约束是交易的条件，不是判决。禁止把“必然／不可避免／无法消除／注定／死路”当作结论。
- **分级在装置，不在每句**：证据/概念等级放表格与附录；正文一句一个精确限定即可，不反复“本书不宣称”。
- **反例进正文**；**地图只定性**。
- 每个硬约束章必须带反向力量：这条限制**使什么成为可能**。

## 版本脉络

见 `versions/CHANGELOG.md`（首版）。
