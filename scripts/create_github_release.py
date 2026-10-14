# -*- coding: utf-8 -*-
"""create_github_release.py — 为每个发布产物创建一个独立的 GitHub Release（一个产物一个 tag）。

设计原则
--------
* **一个产物一个 tag**：每个 release 只承载一个资产，使每个产物都能被独立引用、
  独立归档（例如各获得一个 Zenodo 版本 DOI）。
* Token 从 git credential helper 读取，**不落盘、不打印**。
* 幂等：同名 tag / 同名资产已存在时复用，不重复创建。

用法
----
    python scripts/create_github_release.py --date 2026-10-12
    python scripts/create_github_release.py --date 2026-10-12 --draft
    python scripts/create_github_release.py --list
    python scripts/create_github_release.py --date 2026-10-12 --only epub
"""
import argparse
import os
import subprocess
import sys

import requests

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIT = os.environ.get("GIT_BIN", r"D:\Git\cmd\git.exe")

# (kind, 源文件, GitHub 资产名, release 名称, 说明)
# 顺序即“产物清单”，与 release/MANIFEST.txt 对应。
ARTIFACTS = [
    ("print-pdf", "release/capacity-cascade-print.pdf",
     "capacity-cascade-print.pdf", "印刷版 PDF（A4）",
     "A4 单栏、宋体＋Times、四级 PDF 书签，适合打印与正式引用。"),
    ("ereader-pdf", "release/capacity-cascade-ereader.pdf",
     "capacity-cascade-ereader.pdf", "电子阅读版 PDF（B5）",
     "B5 重排、12pt／1.8 倍行距、斑马纹表格，适合平板与屏幕阅读。"),
    ("epub", "release/capacity-cascade.epub",
     "capacity-cascade.epub", "EPUB 3",
     "EPUB 3（含 nav + NCX 四级目录），可在 Kindle、Apple Books、多看等阅读。"),
    ("html", "release/capacity-cascade.html",
     "capacity-cascade.html", "网页版（自包含）",
     "单文件自包含 HTML，含内嵌图片，可直接浏览器打开。"),
    ("ereader-html", "release/capacity-cascade-ereader.html",
     "capacity-cascade-ereader.html", "电子阅读网页版",
     "网页版 + 电子阅读样式叠加。"),
    ("markdown", "release/capacity-cascade.md",
     "capacity-cascade.md", "合并 Markdown",
     "全书合一的 GFM Markdown（含表格与公式行）。"),
    ("markdown-zip", "release/capacity-cascade-markdown.zip",
     "capacity-cascade-markdown.zip", "分文件 Markdown 打包",
     "逐文件 Markdown + assets 图片，便于二次编辑与再发布。"),
    ("cover", "release/cover.svg",
     "cover.svg", "封面矢量图",
     "满版封面 SVG（A4 比例），可无损缩放。"),
]


def get_token():
    out = subprocess.run(
        [GIT, "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    for line in out.stdout.splitlines():
        if line.startswith("password="):
            return line[len("password="):].strip()
    raise SystemExit("未能从 git credential helper 取得 token")


def api(tok, method, url, extra_headers=None, **kw):
    headers = {
        "Authorization": f"token {tok}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "capacity-cascade-release"}
    if extra_headers:
        headers.update(extra_headers)
    return requests.request(method, url, headers=headers, timeout=180, **kw)


def ensure_release(tok, repo, tag, name, body, draft, prerelease):
    base = f"https://api.github.com/repos/{repo}"
    r = api(tok, "GET", f"{base}/releases/tags/{tag}")
    if r.status_code == 200:
        rel = r.json()
        print(f"[reuse] {tag} id={rel['id']}")
        return rel
    r = api(tok, "POST", f"{base}/releases", json={
        "tag_name": tag, "name": name, "body": body,
        "draft": draft, "prerelease": prerelease})
    if r.status_code not in (200, 201):
        raise SystemExit(f"创建 release 失败（{tag}）：{r.status_code} {r.text[:300]}")
    rel = r.json()
    print(f"[new] {tag} id={rel['id']} draft={draft}")
    return rel


def upload(tok, repo, rel, src, dst):
    p = os.path.join(HERE, src)
    if not os.path.exists(p):
        print(f"  [skip] 缺文件 {src}")
        return
    have = {a["name"] for a in rel.get("assets", [])}
    if dst in have:
        print(f"  [have] {dst}")
        return
    with open(p, "rb") as fh:
        up = api(tok, "POST",
                 f"https://uploads.github.com/repos/{repo}/releases/{rel['id']}/assets",
                 params={"name": dst}, data=fh,
                 extra_headers={"Content-Type": "application/octet-stream"})
    ok = up.status_code in (200, 201)
    print(f"  [{'ok' if ok else 'FAIL'}] {dst}"
          + ("" if ok else f" {up.status_code} {up.text[:200]}"))


def verify(tok, repo, do_fix=False):
    """校验「一个 tag ↔ 一个 release」不变式：
    - 每个远端 tag 必须有对应的 release；
    - 每个 release 必须恰好承载一个资产；
    - 不存在没有 tag 的 release。
    返回违规数。do_fix=True 时，为缺 release 的 tag 创建单资产 release。"""
    base = f"https://api.github.com/repos/{repo}"
    tags = [t["name"] for t in api(tok, "GET", f"{base}/tags").json()]
    rels = {r["tag_name"]: r for r in api(tok, "GET", f"{base}/releases").json()}
    kind_src = {kind: (src, dst, name) for kind, src, dst, name, _ in ARTIFACTS}
    problems = 0
    print(f"tags={len(tags)}  releases={len(rels)}")
    for t in sorted(tags):
        if t not in rels:
            problems += 1
            print(f"  [缺 release] {t}")
            if do_fix:
                # tag 形如 <prefix>-<date>-<kind>；kind 可能含连字符（print-pdf）
                matched = next((k for k in kind_src if t.endswith("-" + k)), None)
                if not matched:
                    print(f"    [skip] 无法从 tag 推断产物种类：{t}")
                    continue
                src, dst, name = kind_src[matched]
                rel = ensure_release(tok, repo, t, f"{name}（{t}）",
                                     "单产物 release（一个 release 一个 tag）。", False, False)
                upload(tok, repo, rel, src, dst)
        else:
            n = len(rels[t].get("assets", []))
            if n != 1:
                problems += 1
                print(f"  [资产数 {n} ≠ 1] {t}")
    for t in rels:
        if t not in tags:
            problems += 1
            print(f"  [release 无 tag] {t}")
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="lyp0746/capacity-cascade")
    ap.add_argument("--date", default="", help="版本日期，用于 tag，如 2026-10-12")
    ap.add_argument("--tag-prefix", default="edition")
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--prerelease", action="store_true")
    ap.add_argument("--only", default="", help="只发布某个 kind")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--verify", action="store_true",
                    help="校验“一个 tag 一个 release”不变式；配合 --fix 补建缺失 release")
    ap.add_argument("--fix", action="store_true", help="配合 --verify：为缺 release 的 tag 补建")
    args = ap.parse_args()

    if args.verify:
        tok = get_token()
        bad = verify(tok, args.repo, do_fix=args.fix)
        print("OK：每个 tag 对应且仅对应一个 release。" if bad == 0 else f"发现 {bad} 处违规。")
        sys.exit(0 if bad == 0 else 1)

    if args.list or not args.date:
        print("产物清单（一个产物一个 tag）：")
        for kind, src, dst, name, desc in ARTIFACTS:
            tag = f"{args.tag_prefix}-<date>-{kind}"
            print(f"  {tag:44s} {name}  <- {src}")
        return

    tok = get_token()
    for kind, src, dst, name, desc in ARTIFACTS:
        if args.only and kind != args.only:
            continue
        tag = f"{args.tag_prefix}-{args.date}-{kind}"
        rel_name = f"遗忘的边界 · {name}（{args.date}）"
        body = (f"{desc}\n\n"
                f"本书为理论专著《遗忘的边界：有限容量下的记忆、智能与自我》。"
                f"本 release 仅承载一个产物（一个产物一个 tag）。\n"
                f"内容许可 CC BY 4.0；代码许可 MIT。")
        rel = ensure_release(tok, args.repo, tag, rel_name, body,
                             args.draft, args.prerelease)
        upload(tok, args.repo, rel, src, dst)
        print(f"      -> {rel.get('html_url')}")
    print("完成。")


if __name__ == "__main__":
    main()
