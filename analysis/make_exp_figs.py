# -*- coding: utf-8 -*-
"""make_exp_figs.py ——《遗忘的边界》实验插图（系列版式的 SVG）。"""
import json
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "assets", "svg")
INK, GRY = "#1a1a1a", "#666666"
BLU, GRN, ORG, RED, GLD = "#2f6db0", "#2e7d32", "#ef6c00", "#c62828", "#b8862f"
d = json.load(open(os.path.join(HERE, "data", "exp_memory.json"), encoding="utf-8"))


def head(W, H, t, sub=None):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Microsoft YaHei, PingFang SC, SimHei, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
         f'<text x="{W/2}" y="38" text-anchor="middle" font-size="22" font-weight="bold" fill="{INK}">{t}</text>']
    if sub:
        s.append(f'<text x="{W/2}" y="62" text-anchor="middle" font-size="14" fill="{GRY}">{sub}</text>')
    return s


def txt(x, y, t, size=12, fill=INK, anchor="middle", weight="normal"):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" font-weight="{weight}">{t}</text>'


def axis(x0, y0, w, h, xl, yl):
    return [f'<line x1="{x0}" y1="{y0}" x2="{x0+w}" y2="{y0}" stroke="#333" stroke-width="1.8"/>',
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0-h}" stroke="#333" stroke-width="1.8"/>',
            txt(x0 + w / 2, y0 + 40, xl, 13, GRY),
            f'<text x="{x0-48}" y="{y0-h/2}" text-anchor="middle" font-size="13" fill="{GRY}" '
            f'transform="rotate(-90 {x0-48} {y0-h/2})">{yl}</text>']


def save(name, s):
    open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8").write("\n".join(s + ["</svg>"]))
    print("wrote", name)


# ---------------------------------------------------------------- 图 1
def hopfield_fig():
    W, H = 860, 500
    s = head(W, H, "容量不是一个数字，是一段斜坡",
             "Hopfield 网络（N=300，Hebbian 规则，20 次试验）；理论临界 α_c≈0.138")
    x0, y0, w, h = 100, 390, 660, 280
    s += axis(x0, y0, w, h, "负荷 α = P/N", "检索重叠 |m|")
    pts = [(r["alpha"], r["overlap"]) for r in d["hopfield"]["curve"]]
    xmax = 0.30
    fx = lambda v: x0 + v / xmax * w
    fy = lambda v: y0 - v * h
    for v in (0.0, 0.5, 1.0):
        s.append(f'<line x1="{x0-5}" y1="{fy(v):.1f}" x2="{x0}" y2="{fy(v):.1f}" stroke="#333"/>')
        s.append(txt(x0 - 10, fy(v) + 4, f"{v:.1f}", 11, GRY, "end"))
    for a in (0.05, 0.10, 0.15, 0.20, 0.25, 0.30):
        s.append(f'<line x1="{fx(a):.1f}" y1="{y0}" x2="{fx(a):.1f}" y2="{y0+5}" stroke="#333"/>')
        s.append(txt(fx(a), y0 + 20, f"{a:.2f}", 11, GRY))
    dd = " ".join(("M" if i == 0 else "L") + f"{fx(a):.1f},{fy(m):.1f}" for i, (a, m) in enumerate(pts))
    s.append(f'<path d="{dd}" fill="none" stroke="{BLU}" stroke-width="2.6"/>')
    for a, m in pts:
        s.append(f'<circle cx="{fx(a):.1f}" cy="{fy(m):.1f}" r="3.2" fill="{BLU}"/>')
    xc = fx(0.138)
    s.append(f'<line x1="{xc:.1f}" y1="{y0}" x2="{xc:.1f}" y2="{y0-h}" stroke="{RED}" stroke-width="1.5" stroke-dasharray="6,5"/>')
    s.append(txt(xc + 6, y0 - h + 14, "α_c≈0.138（理论）", 12, RED, "start"))
    s.append(txt(x0 + 30, fy(0.86), "重叠≈1：几乎完美检索", 12, GRN, "start"))
    s.append(txt(fx(0.20), fy(0.66), "负荷一过，检索迅速变差", 12, ORG, "start"))
    s.append(txt(W / 2, H - 16, "“容量”不是“能记多少条”，而是“负荷到哪里，检索开始不可靠”。", 12, GRY))
    save("fig-exp-hopfield", s)


# ---------------------------------------------------------------- 图 2
def tracking_fig():
    W, H = 880, 500
    s = head(W, H, "双时间尺度：只在一个窄窗口里更好",
             "环境=稳定水平（中期漂移）+ 快变成分 + 噪声；纵轴为末段均方误差（越低越好）")
    x0, y0, w, h = 110, 390, 660, 280
    s += axis(x0, y0, w, h, "切换周期 T（对数轴）", "末段均方误差（MSE）")
    P = d["tracking"]["periods"]
    single = d["tracking"]["single_best"]
    dual = d["tracking"]["dual"]
    import math
    lx0, lx1 = math.log10(200), math.log10(10000)
    ymax = max(single + dual) * 1.15
    fx = lambda v: x0 + (math.log10(v) - lx0) / (lx1 - lx0) * w
    fy = lambda v: y0 - v / ymax * h
    for T in (200, 500, 1000, 2000, 5000, 10000):
        s.append(f'<line x1="{fx(T):.1f}" y1="{y0}" x2="{fx(T):.1f}" y2="{y0+5}" stroke="#333"/>')
        s.append(txt(fx(T), y0 + 20, str(T), 11, GRY))
    for v in (0.0, 0.1, 0.2, 0.3):
        if v <= ymax:
            s.append(f'<line x1="{x0-5}" y1="{fy(v):.1f}" x2="{x0}" y2="{fy(v):.1f}" stroke="#333"/>')
            s.append(txt(x0 - 10, fy(v) + 4, f"{v:.1f}", 11, GRY, "end"))
    for series, col, lab in ((single, BLU, "单速率（网格内最优）"), (dual, ORG, "快+慢双速率")):
        dd = " ".join(("M" if i == 0 else "L") + f"{fx(T):.1f},{fy(v):.1f}" for i, (T, v) in enumerate(zip(P, series)))
        s.append(f'<path d="{dd}" fill="none" stroke="{col}" stroke-width="2.4"/>')
        for T, v in zip(P, series):
            s.append(f'<circle cx="{fx(T):.1f}" cy="{fy(v):.1f}" r="3.2" fill="{col}"/>')
    s.append(f'<line x1="{x0+10}" y1="{y0-h+16}" x2="{x0+34}" y2="{y0-h+16}" stroke="{BLU}" stroke-width="2.4"/>')
    s.append(txt(x0 + 40, y0 - h + 20, "单速率（最优网格）", 11, BLU, "start"))
    s.append(f'<line x1="{x0+10}" y1="{y0-h+34}" x2="{x0+34}" y2="{y0-h+34}" stroke="{ORG}" stroke-width="2.4"/>')
    s.append(txt(x0 + 40, y0 - h + 38, "快+慢双速率", 11, ORG, "start"))
    s.append(txt(W / 2, H - 34, "T=200 时双速率好 3.8%，T=500 时好 3.6%；T≥1000 后两者无差别。", 12, GRY))
    s.append(txt(W / 2, H - 14, "这个窄窗口，是对“多时间尺度是矛盾的数学解”的一次限定：它只在切换快于学习率时成立。", 12, GRY))
    save("fig-exp-timescale", s)


hopfield_fig()
tracking_fig()
