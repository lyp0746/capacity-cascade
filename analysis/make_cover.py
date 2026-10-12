# -*- coding: utf-8 -*-
"""make_cover.py — 生成《容量级联》满版封面 SVG（A4 比例 1000×1414）。

输出：assets/svg/cover.svg
封面须满版：配合 assets/css/book.css 中 .cover-page 的 210mm×297mm 与
@page :first { margin: 0 }，让底色铺满整页。
"""
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "assets", "svg", "cover.svg")


def build():
    W, H = 1000, 1414
    ink = "#e8e6df"
    dim = "#9aa0a6"
    layers = []
    # 容量级联：三层同心弧，自上而下
    for i, (r, op, col) in enumerate([(300, 0.16, "#3a6ea5"),
                                      (230, 0.24, "#b8862f"),
                                      (160, 0.34, "#009E73")]):
        cy = 560 + i * 10
        layers.append(f'<circle cx="500" cy="{cy}" r="{r}" fill="none" '
                      f'stroke="{col}" stroke-width="2" opacity="{op}"/>')
        layers.append(f'<circle cx="500" cy="{cy}" r="{r-30}" fill="none" '
                      f'stroke="{col}" stroke-width="1" opacity="{op*0.7:.3f}" stroke-dasharray="6,7"/>')
    # 级联向下的虚线
    for i in range(6):
        y = 900 + i * 34
        w = 420 - i * 56
        layers.append(f'<line x1="{500-w/2:.0f}" y1="{y}" x2="{500+w/2:.0f}" y2="{y}" '
                      f'stroke="{dim}" stroke-width="1" opacity="{0.5-0.06*i:.2f}"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#10131a"/><stop offset="0.55" stop-color="#161b24"/>
<stop offset="1" stop-color="#0c0f15"/>
</linearGradient>
</defs>
<rect x="0" y="0" width="{W}" height="{H}" fill="url(#bg)"/>
<rect x="0" y="0" width="{W}" height="8" fill="#b8862f" opacity="0.85"/>
{chr(10).join(layers)}
<style>
text{{font-family:'Microsoft YaHei','SimHei',Arial,sans-serif;}}
.ttl{{font-size:104px;font-weight:700;letter-spacing:10px;fill:{ink};}}
.sub{{font-size:30px;fill:{dim};letter-spacing:2px;}}
.eng{{font-size:22px;fill:{dim};letter-spacing:1px;}}
.au{{font-size:30px;fill:{ink};letter-spacing:2px;}}
.rule{{stroke:{dim};stroke-width:1;opacity:0.6;}}
</style>
<text x="80" y="180" class="eng">CAPACITY&#160;·&#160;CASCADE</text>
<text x="80" y="300" class="ttl">容量级联</text>
<line x1="84" y1="340" x2="620" y2="340" class="rule"/>
<text x="84" y="392" class="sub">有限容量下的多尺度自适应</text>
<text x="84" y="432" class="sub">从大语言模型、智能体到人类记忆</text>
<text x="80" y="1180" class="au">李毅芃　著</text>
<text x="80" y="1230" class="eng">Capacity-Cascade: Multi-Scale Adaptation under Finite Capacity</text>
<text x="80" y="1270" class="eng">理论专著 · 2026</text>
</svg>
'''
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
