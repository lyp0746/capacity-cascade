# -*- coding: utf-8 -*-
"""make_figures.py — 生成《容量级联》全部 SVG 插图（确定性、无外部依赖）。

输出：assets/svg/fig*.svg
风格：house palette（蓝 #3a6ea5 / 红 #c94f4f / 金 #b8862f / 绿 #009E73 / 灰 #666），
白底、细线、无阴影；文本由浏览器渲染（保留中文字体）。
"""
import math
import os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "assets", "svg")
os.makedirs(OUT, exist_ok=True)

BLUE, RED, GOLD, GREEN, GREY = "#3a6ea5", "#c94f4f", "#b8862f", "#009E73", "#666"
INK, LIGHT = "#1a1a1a", "#cfcfcf"
FONT = "'Microsoft YaHei','SimHei',Arial,sans-serif"
SERIF = "'Times New Roman',SimSun,serif"


def svg(w, h, body, bg="#ffffff"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}">\n'
            f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}"/>\n'
            f'<style>text{{font-family:{FONT};fill:{INK};}}'
            f'.s{{font-family:{SERIF};}}'
            f'.t{{font-size:15px;font-weight:700;}}'
            f'.l{{font-size:11px;}}'
            f'.ax{{stroke:{GREY};stroke-width:1;}}'
            f'.g{{stroke:{LIGHT};stroke-width:1;}}</style>\n'
            f'{body}\n</svg>\n')


def axes(x0, y0, x1, y1, xlabel="", ylabel=""):
    b = [f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" class="ax"/>',
         f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" class="ax"/>']
    if xlabel:
        b.append(f'<text x="{(x0+x1)/2}" y="{y0+34}" class="l" text-anchor="middle">{xlabel}</text>')
    if ylabel:
        b.append(f'<text x="{x0-8}" y="{(y0+y1)/2}" class="l" text-anchor="middle" '
                 f'transform="rotate(-90 {x0-8} {(y0+y1)/2})">{ylabel}</text>')
    return "\n".join(b)


def polyline(pts, color=BLUE, w=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{w}"{d}/>'


def txt(x, y, s, anchor="start", cls="l", color=INK, weight="normal"):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}">{s}</text>'


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name)


# ---------------------------------------------------------------- fig 1.1
def fig01():
    w, h = 760, 300
    b = []
    # (a) 位置偏差
    b.append(f'<text x="20" y="26" class="t">（a）长上下文位置偏差</text>')
    b.append(axes(40, 200, 220, 50, "相对位置", "正确率"))
    pts = [(40, 80), (70, 120), (100, 160), (130, 175), (160, 160), (190, 120), (220, 80)]
    b.append(polyline(pts, BLUE, 2.4))
    # (b) 漂移
    b.append(f'<text x="280" y="26" class="t">（b）上下文漂移</text>')
    b.append(axes(300, 200, 480, 50, "轮次", "与初始目标距离"))
    b.append(polyline([(300, 190), (350, 185), (400, 175), (450, 158), (480, 145)], RED, 2.4))
    b.append(polyline([(300, 190), (350, 183), (400, 172), (450, 158), (480, 140)], BLUE, 1.6, "5,4"))
    b.append(txt(390, 210, "偏置（线性）", "middle", "l", RED))
    b.append(txt(390, 226, "随机（√n）", "middle", "l", BLUE))
    # (c) 忒修斯
    b.append(f'<text x="540" y="26" class="t">（c）自我改写</text>')
    cx, cy = 620, 140
    for i, r in enumerate((70, 52, 34)):
        b.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*0.62:.1f}" fill="none" '
                 f'stroke="{GOLD if i==0 else GREY}" stroke-width="{2 if i==0 else 1}" '
                 f'{"" if i==0 else "stroke-dasharray=\"4,3\""}/>')
    b.append(txt(cx, 230, "物质被替换，结构保持", "middle", "l", GREY))
    save("fig01-three-observations.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 2.1
def fig02():
    w, h = 720, 320
    b = [f'<text x="20" y="26" class="t">统一的四级阶梯与本书的位置</text>']
    levels = [("U4 同一", "本体上的同一", 0), ("U3 可模拟", "一方可在另一方机制上实现", 1),
              ("U2 同律", "粗化后遵循同一组方程", 2), ("U1 同约束", "受同一组约束", 3)]
    for name, desc, i in levels:
        y = 60 + i * 58
        col = GREEN if i == 3 else GREY
        b.append(f'<rect x="60" y="{y}" width="600" height="42" rx="6" fill="#f7f7f5" stroke="{col}" stroke-width="1.4"/>')
        b.append(txt(80, y + 27, name, "start", "l", col, "700"))
        b.append(txt(180, y + 27, desc, "start", "l", INK))
        b.append(txt(640, y + 27, "易检验" if i == 3 else "难检验", "end", "l", GREY))
    b.append(f'<line x1="60" y1="{60+3*58-10}" x2="660" y2="{60+3*58-10}" stroke="{GREEN}" stroke-width="1.6" stroke-dasharray="6,4"/>')
    b.append(txt(360, 305, "本书承诺线：只主张 U1", "middle", "l", GREEN, "700"))
    save("fig02-unification-ladder.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 4.1
def fig04():
    w, h = 620, 340
    b = [f'<text x="20" y="26" class="t">信息曲线与三相位</text>']
    b.append(axes(70, 280, 560, 50, "压缩增强  I(X;Z) 下降 →", "任务相关性 I(Z;Y)"))
    # 信息曲线
    pts = []
    for i in range(0, 101):
        t = i / 100
        x = 70 + t * 470
        y = 280 - (250 * (1 - math.exp(-3.2 * t)) * (1 - 0.28 * max(0, t - 0.6)))
        pts.append((x, y))
    b.append(polyline(pts, BLUE, 2.6))
    for x, lab in ((150, "拟合"), (330, "临界"), (500, "压缩")):
        b.append(f'<line x1="{x}" y1="50" x2="{x}" y2="280" class="g"/>')
        b.append(txt(x, 42, lab, "middle", "l", GREY))
    b.append(txt(120, 300, "表示获得任务结构", "middle", "l", GREY))
    b.append(txt(510, 300, "与任务无关的信息被丢弃", "middle", "l", GREY))
    save("fig04-information-bottleneck.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 5.1
def fig05():
    w, h = 620, 340
    b = [f'<text x="20" y="26" class="t">有效容量随干扰的衰减（示意）</text>']
    b.append(axes(70, 280, 560, 50, "归一化干扰 ι", "C_eff / C_max"))
    exp_pts, log_pts, lin_pts = [], [], []
    for i in range(0, 101):
        x = 70 + (i / 100) * 470
        t = i / 100 * 4
        exp_pts.append((x, 280 - 225 * math.exp(-0.55 * t)))
        log_pts.append((x, 280 - 225 / (1 + 0.35 * t)))
        lin_pts.append((x, 280 - 225 * max(0, 1 - 0.22 * t)))
    b.append(polyline(lin_pts, GREY, 1.6, "4,4"))
    b.append(polyline(log_pts, GOLD, 1.8, "7,4"))
    b.append(polyline(exp_pts, BLUE, 2.6))
    b.append(txt(500, 120, "指数", "start", "l", BLUE, "700"))
    b.append(txt(500, 148, "对数", "start", "l", GOLD))
    b.append(txt(500, 176, "线性", "start", "l", GREY))
    save("fig05-capacity-interference.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 6.1
def fig06():
    w, h = 640, 360
    b = [f'<text x="20" y="26" class="t">容量级联（三时间尺度）</text>']
    layers = [("快 · 选择层（毫秒—秒）", 90, BLUE, "工作记忆 / 注意力：约 4–7 项"),
              ("中 · 暂存层（秒—小时）", 170, GOLD, "上下文窗口 / KV 缓存：易受干扰"),
              ("慢 · 结构层（小时—终身）", 250, GREEN, "长期记忆 / 权重：缓慢固化")]
    for name, y, col, sub in layers:
        b.append(f'<rect x="60" y="{y}" width="520" height="52" rx="6" fill="#fafafa" stroke="{col}" stroke-width="1.6"/>')
        b.append(txt(80, y + 23, name, "start", "l", col, "700"))
        b.append(txt(80, y + 42, sub, "start", "l", GREY))
        b.append(f'<line x1="560" y1="{y+6}" x2="560" y2="{y+46}" stroke="{col}" stroke-width="3" stroke-dasharray="3,3"/>')
    for y in (142, 222):
        b.append(f'<line x1="320" y1="{y}" x2="320" y2="{y+28}" stroke="{GREY}" stroke-width="1.4" marker-end="url(#a)"/>')
    b.append('<defs><marker id="a" markerWidth="8" markerHeight="8" refX="4" refY="6" orient="auto">'
             f'<path d="M0,0 L4,6 L8,0" fill="none" stroke="{GREY}"/></marker></defs>')
    b.append(txt(330, 168, "丢弃是层间唯一传送带", "start", "l", GREY))
    b.append(txt(320, 335, "总吞吐不随层数线性增加", "middle", "l", INK, "700"))
    save("fig06-timescale-cascade.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 7.1
def fig07():
    w, h = 640, 350
    b = [f'<text x="20" y="26" class="t">位置偏差与三个候选机制</text>']
    b.append(axes(70, 285, 580, 50, "信息在输入中的相对位置", "被正确使用的概率"))
    # U 形（观察）
    obs = []
    for i in range(0, 101):
        t = i / 100
        x = 70 + t * 500
        y = 285 - (215 * (0.42 + 0.58 * (2 * t - 1) ** 2))
        obs.append((x, y))
    b.append(polyline(obs, INK, 2.8))
    # 单调衰减（H1）
    b.append(polyline([(70 + i / 100 * 500, 285 - 215 * (1 - 0.55 * i / 100)) for i in range(101)], BLUE, 1.6, "6,4"))
    # 中段低谷（H2）
    mid = []
    for i in range(0, 101):
        t = i / 100
        y = 285 - 215 * (0.85 - 0.45 * math.exp(-((t - 0.5) ** 2) / 0.02))
        mid.append((70 + t * 500, y))
    b.append(polyline(mid, GOLD, 1.6, "7,4"))
    # 振荡（H4）
    osc = []
    for i in range(0, 101):
        t = i / 100
        y = 285 - 215 * (0.72 + 0.10 * math.sin(10 * t))
        osc.append((70 + t * 500, y))
    b.append(polyline(osc, GREEN, 1.4, "2,3"))
    b.append(txt(90, 300, "观察（U 形）", "start", "l", INK, "700"))
    b.append(txt(300, 300, "H1 干扰累积", "start", "l", BLUE))
    b.append(txt(440, 300, "H2 压缩阶段", "start", "l", GOLD))
    b.append(txt(470, 318, "H4 注意力振荡", "start", "l", GREEN))
    save("fig07-attention-position.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 8.1
def fig08():
    w, h = 640, 350
    b = [f'<text x="20" y="26" class="t">目标漂移的两种尺度</text>']
    b.append(axes(70, 285, 580, 50, "对话轮次 n", "与初始目标的距离"))
    lin = [(70 + i, 285 - 230 * min(1.0, (i - 70) / 500)) for i in range(70, 571, 5)]
    sq = [(70 + i, 285 - 230 * math.sqrt(max(0, (i - 70) / 500))) for i in range(70, 571, 5)]
    b.append(polyline(lin, RED, 2.4))
    b.append(polyline(sq, BLUE, 2.4))
    b.append(f'<line x1="70" y1="120" x2="570" y2="120" stroke="{GOLD}" stroke-width="1.6" stroke-dasharray="6,4"/>')
    b.append(txt(575, 124, "盆边界 r", "start", "l", GOLD, "700"))
    b.append(txt(430, 90, "有偏漂移（线性）", "start", "l", RED, "700"))
    b.append(txt(430, 66, "随机游走（√n）", "start", "l", BLUE, "700"))
    b.append(txt(320, 330, "压掉偏置：临界轮次可从 n_c≈r/μ 提升到 n_c≈r²/σ²", "middle", "l", INK))
    save("fig08-agent-drift.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 9.1
def fig09():
    w, h = 640, 330
    b = [f'<text x="20" y="26" class="t">系统巩固的互补学习系统（示意）</text>']
    b.append(f'<rect x="60" y="70" width="220" height="150" rx="8" fill="#f4f8fb" stroke="{BLUE}" stroke-width="1.6"/>')
    b.append(txt(170, 100, "海马体", "middle", "l", BLUE, "700"))
    b.append(txt(170, 125, "快 · 一次编码", "middle", "l", INK))
    b.append(txt(170, 148, "高情境特异性", "middle", "l", GREY))
    b.append(txt(170, 171, "容量有限、脆弱", "middle", "l", GREY))
    b.append(f'<rect x="380" y="70" width="220" height="150" rx="8" fill="#f3f9f5" stroke="{GREEN}" stroke-width="1.6"/>')
    b.append(txt(490, 100, "皮质", "middle", "l", GREEN, "700"))
    b.append(txt(490, 125, "慢 · 缓慢固化", "middle", "l", INK))
    b.append(txt(490, 148, "低情境特异性", "middle", "l", GREY))
    b.append(txt(490, 171, "容量大、稳定", "middle", "l", GREY))
    b.append(f'<line x1="280" y1="145" x2="380" y2="145" stroke="{GOLD}" stroke-width="2.4" marker-end="url(#m)"/>')
    b.append('<defs><marker id="m" markerWidth="9" markerHeight="9" refX="5" refY="6" orient="auto">'
             f'<path d="M0,0 L5,6 L10,0" fill="none" stroke="{GOLD}"/></marker></defs>')
    b.append(txt(330, 135, "睡眠重放", "middle", "l", GOLD, "700"))
    b.append(txt(330, 265, "快系统 + 慢系统 = 同时得到“快”与“稳”", "middle", "l", INK, "700"))
    b.append(txt(330, 290, "这是容量级联在生物上的实例", "middle", "l", GREY))
    save("fig09-consolidation.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 10.1
def fig10():
    w, h = 700, 320
    b = [f'<text x="20" y="26" class="t">两种计算模式</text>']
    # 左：清醒
    b.append(f'<rect x="40" y="60" width="280" height="200" rx="8" fill="#f4f8fb" stroke="{BLUE}" stroke-width="1.6"/>')
    b.append(txt(180, 90, "清醒计算", "middle", "l", BLUE, "700"))
    for i, (name, yy) in enumerate((("外部输入", 130), ("注意力选择", 170), ("局部拟合（梯度下降）", 210))):
        b.append(f'<rect x="80" y="{yy}" width="200" height="28" rx="4" fill="#ffffff" stroke="{BLUE}"/>')
        b.append(txt(180, yy + 19, name, "middle", "l", INK))
        if i < 2:
            b.append(f'<line x1="180" y1="{yy+28}" x2="180" y2="{yy+40}" stroke="{BLUE}" stroke-width="1.4"/>')
    b.append(txt(180, 290, "适应 · 风险：过拟合、僵化", "middle", "l", GREY))
    # 右：睡眠
    b.append(f'<rect x="380" y="60" width="280" height="200" rx="8" fill="#f3f9f5" stroke="{GREEN}" stroke-width="1.6"/>')
    b.append(txt(520, 90, "睡眠计算", "middle", "l", GREEN, "700"))
    for i, (name, yy) in enumerate((("外部输入切断", 130), ("内源激活", 170), ("全局重排（高熵采样）", 210))):
        b.append(f'<rect x="420" y="{yy}" width="200" height="28" rx="4" fill="#ffffff" stroke="{GREEN}"/>')
        b.append(txt(520, yy + 19, name, "middle", "l", INK))
        if i < 2:
            b.append(f'<line x1="520" y1="{yy+28}" x2="520" y2="{yy+40}" stroke="{GREEN}" stroke-width="1.4"/>')
    b.append(txt(520, 290, "泛化 · 风险：脱离现实", "middle", "l", GREY))
    b.append(f'<line x1="330" y1="160" x2="370" y2="160" stroke="{GOLD}" stroke-width="2.4"/>')
    b.append(txt(350, 150, "协调", "middle", "l", GOLD, "700"))
    save("fig10-wake-dream.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 11.1
def fig11():
    w, h = 660, 340
    b = [f'<text x="20" y="26" class="t">内源模拟打破局部吸引子（示意）</text>']
    b.append(axes(70, 290, 600, 60, "表示空间 S", "能量"))
    # 能量曲面（双谷）
    def energy(t):
        return 0.5 + 0.0 * t
    pts = []
    for i in range(0, 101):
        t = i / 100
        x = 70 + t * 530
        e = 0.55 - 0.32 * math.exp(-((t - 0.30) ** 2) / 0.005) - 0.52 * math.exp(-((t - 0.72) ** 2) / 0.006)
        pts.append((x, 90 + (1 - e) * 150))
    b.append(polyline(pts, GREY, 2.0, "6,4"))
    # 退火后（更深）
    pts2 = []
    for i in range(0, 101):
        t = i / 100
        x = 70 + t * 530
        e = 0.55 - 0.30 * math.exp(-((t - 0.30) ** 2) / 0.006) - 0.66 * math.exp(-((t - 0.72) ** 2) / 0.008)
        pts2.append((x, 90 + (1 - e) * 150))
    b.append(polyline(pts2, BLUE, 2.6))
    b.append(f'<circle cx="{70+0.30*530:.0f}" cy="{90+(1-(0.55-0.32))*150:.0f}" r="7" fill="{RED}"/>')
    b.append(f'<circle cx="{70+0.72*530:.0f}" cy="{90+(1-(0.55-0.66))*150:.0f}" r="7" fill="{GREEN}"/>')
    b.append(txt(230, 300, "局部最优（清醒学习后）", "middle", "l", RED, "700"))
    b.append(txt(470, 300, "更深的解（内源重组后）", "middle", "l", GREEN, "700"))
    b.append(txt(330, 325, "虚线：原始曲面；实线：加噪退火后", "middle", "l", GREY))
    save("fig11-dream-attractor.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 12.1
def fig12():
    w, h = 620, 340
    b = [f'<text x="20" y="26" class="t">意识窗口与潜意识空间（示意）</text>']
    b.append(f'<circle cx="310" cy="185" r="135" fill="#fafafa" stroke="{GREY}" stroke-width="1.4"/>')
    b.append(f'<circle cx="310" cy="185" r="46" fill="#f4f8fb" stroke="{BLUE}" stroke-width="2"/>')
    b.append(txt(310, 182, "C", "middle", "l", BLUE, "700"))
    b.append(txt(310, 202, "意识窗口", "middle", "l", BLUE))
    b.append(txt(310, 330, "Ω", "middle", "l", GREY, "700"))
    b.append(txt(440, 90, "U = Ω \\ C", "start", "l", GREY, "700"))
    b.append(txt(440, 112, "潜意识：维度更高", "start", "l", GREY))
    b.append(f'<line x1="330" y1="230" x2="410" y2="120" stroke="{GOLD}" stroke-width="1.8" marker-end="url(#f)"/>')
    b.append('<defs><marker id="f" markerWidth="8" markerHeight="8" refX="4" refY="6" orient="auto">'
             f'<path d="M0,0 L4,6 L8,0" fill="none" stroke="{GOLD}"/></marker></defs>')
    b.append(txt(392, 250, "浮现", "start", "l", GOLD, "700"))
    b.append(txt(310, 60, "意识是极小的广播窗口，潜意识是极大的补集", "middle", "l", INK, "700"))
    save("fig12-consciousness-window.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 13.1
def fig13():
    w, h = 640, 340
    b = [f'<text x="20" y="26" class="t">元认知的监控—调节环路</text>']
    b.append(f'<rect x="220" y="60" width="200" height="60" rx="8" fill="#fff6ee" stroke="{GOLD}" stroke-width="1.8"/>')
    b.append(txt(320, 88, "元认知层", "middle", "l", GOLD, "700"))
    b.append(txt(320, 108, "估计容量使用与效果", "middle", "l", INK))
    b.append(f'<rect x="220" y="230" width="200" height="60" rx="8" fill="#f4f8fb" stroke="{BLUE}" stroke-width="1.8"/>')
    b.append(txt(320, 258, "底层学习", "middle", "l", BLUE, "700"))
    b.append(txt(320, 278, "清醒 / 睡眠", "middle", "l", INK))
    b.append(f'<path d="M420,90 C520,90 520,260 420,260" fill="none" stroke="{GOLD}" stroke-width="1.8" marker-end="url(#g2)"/>')
    b.append(f'<path d="M220,260 C120,260 120,90 220,90" fill="none" stroke="{BLUE}" stroke-width="1.8" marker-end="url(#g1)"/>')
    b.append('<defs>'
             f'<marker id="g1" markerWidth="8" markerHeight="8" refX="4" refY="6" orient="auto"><path d="M0,0 L4,6 L8,0" fill="none" stroke="{BLUE}"/></marker>'
             f'<marker id="g2" markerWidth="8" markerHeight="8" refX="4" refY="6" orient="auto"><path d="M0,0 L4,6 L8,0" fill="none" stroke="{GOLD}"/></marker>'
             '</defs>')
    b.append(txt(500, 175, "调节：学习率、容量分配、模式切换", "start", "l", GOLD))
    b.append(txt(100, 175, "反馈：本次学习的效果", "end", "l", BLUE))
    save("fig13-metacognition-loop.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 14.1
def fig14():
    w, h = 760, 400
    b = [f'<text x="20" y="26" class="t">母题下的理论地图</text>']
    b.append(f'<circle cx="380" cy="205" r="72" fill="#fff6ee" stroke="{GOLD}" stroke-width="2.2"/>')
    b.append(txt(380, 198, "信息约束下的", "middle", "l", INK, "700"))
    b.append(txt(380, 218, "多尺度自适应", "middle", "l", INK, "700"))
    groups = [
        ("结构", 120, 90, BLUE, ["Shannon", "率失真", "有效秩", "Hopfield"]),
        ("动力学", 120, 300, GREEN, ["信息瓶颈", "预测加工", "强化学习", "遗忘曲线"]),
        ("协调", 610, 195, RED, ["主动推理", "系统巩固", "全脑工作空间", "元认知"]),
    ]
    for name, gx, gy, col, items in groups:
        b.append(f'<ellipse cx="{gx}" cy="{gy}" rx="96" ry="66" fill="#fafafa" stroke="{col}" stroke-width="1.6"/>')
        b.append(txt(gx, gy - 44, name, "middle", "l", col, "700"))
        for j, it in enumerate(items):
            b.append(txt(gx, gy - 20 + j * 20, it, "middle", "l", GREY))
        b.append(f'<line x1="{gx+96 if gx<380 else gx-96}" y1="{gy}" x2="{380 + (72 if gx<380 else -72)}" y2="205" stroke="{col}" stroke-width="1" stroke-dasharray="4,3"/>')
    b.append(txt(380, 385, "虚线 = 安放位置仍有争议；地图只定性，不含权重", "middle", "l", GREY))
    save("fig14-theory-map.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 15.1
def fig15():
    w, h = 700, 340
    b = [f'<text x="20" y="26" class="t">信息瓶颈、自由能原理与强化学习的分工</text>']
    boxes = [("信息瓶颈", "如何压缩", 60, BLUE), ("自由能原理", "如何行动", 270, GOLD), ("强化学习", "何为重要", 480, GREEN)]
    for name, role, x, col in boxes:
        b.append(f'<rect x="{x}" y="110" width="170" height="90" rx="8" fill="#fafafa" stroke="{col}" stroke-width="1.8"/>')
        b.append(txt(x + 85, 148, name, "middle", "l", col, "700"))
        b.append(txt(x + 85, 176, role, "middle", "l", INK))
    b.append(f'<line x1="230" y1="155" x2="270" y2="155" stroke="{GREY}" stroke-width="1.6" marker-end="url(#h1)"/>')
    b.append(f'<line x1="440" y1="155" x2="480" y2="155" stroke="{GREY}" stroke-width="1.6" marker-end="url(#h1)"/>')
    b.append('<defs><marker id="h1" markerWidth="8" markerHeight="8" refX="4" refY="6" orient="auto">'
             f'<path d="M0,0 L4,6 L8,0" fill="none" stroke="{GREY}"/></marker></defs>')
    b.append(txt(250, 145, "定义相关性", "middle", "l", GREY))
    b.append(txt(460, 145, "约束目标", "middle", "l", GREY))
    b.append(txt(350, 260, "三者交汇于母题，但各守其问题域：不是竞争关系，而是分工关系", "middle", "l", INK, "700"))
    save("fig15-IB-FEP-RL.svg", svg(w, h, "\n".join(b)))


# ---------------------------------------------------------------- fig 18.1
def fig18():
    w, h = 760, 300
    b = [f'<text x="20" y="26" class="t">身份的三种改变（示意）</text>']
    labels = [("盆内移动", "日常学习：你仍是你", BLUE), ("吸引子移动", "深刻学习：重心改变，结构连续", GOLD), ("拓扑改变", "创伤／改宗：连续性断裂", RED)]
    for i, (name, desc, col) in enumerate(labels):
        cx = 130 + i * 250
        cy = 150
        # 势能双谷
        pts = []
        for j in range(0, 61):
            t = j / 60
            x = cx - 80 + t * 160
            depth = [0.28, 0.30, 0.55][i]
            shift = [0.5, 0.62, 0.80][i]
            e = 0.6 - depth * math.exp(-((t - shift) ** 2) / 0.02)
            pts.append((x, 110 + (1 - e) * 60))
        b.append(polyline(pts, col, 2.2))
        b.append(f'<circle cx="{cx-80+[0.5,0.62,0.80][i]*160:.0f}" cy="{110+(1-(0.6-[0.28,0.30,0.55][i]))*60:.0f}" r="6" fill="{col}"/>')
        b.append(txt(cx, 52, name, "middle", "l", col, "700"))
        b.append(txt(cx, 220, desc, "middle", "l", GREY))
    save("fig18-identity-attractor.svg", svg(w, h, "\n".join(b)))


if __name__ == "__main__":
    fig01(); fig02(); fig04(); fig05(); fig06(); fig07(); fig08(); fig09()
    fig10(); fig11(); fig12(); fig13(); fig14(); fig15(); fig18()
    print("done")
