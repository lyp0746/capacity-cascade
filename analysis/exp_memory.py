# -*- coding: utf-8 -*-
"""exp_memory.py ——《遗忘的边界》新增数值实验（可复算）。

实验一：Hopfield 网络的容量（Hebbian 规则）。
        经典结果：随机模式数 P 与神经元数 N 之比 α=P/N 超过约 0.138 时，检索失败。
实验二：双时间尺度学习。环境每隔 T 步切换目标；比较“单一学习率”与“快+慢两个学习率”。
输出：data/exp_memory.json
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)
rng = np.random.default_rng(20261016)
out = {"seed": 20261016}


# ---------------------------------------------------------------- 实验一
def hopfield(N, P, trials=20, sweeps=20):
    """返回平均重叠 |m|（对 P 个模式、trials 次取平均）。"""
    ov = []
    for _ in range(trials):
        xi = rng.choice([-1.0, 1.0], size=(P, N))
        W = (xi.T @ xi) / N
        np.fill_diagonal(W, 0.0)
        for p in range(P):
            s = xi[p].copy()
            for _ in range(sweeps):
                s = np.sign(W @ s)
                s[s == 0] = 1.0
            ov.append(abs(float(s @ xi[p])) / N)
    return float(np.mean(ov))


N = 300
alphas = [round(0.02 * i, 2) for i in range(1, 15)]
hop = []
for a in alphas:
    P = max(1, int(round(a * N)))
    m = hopfield(N, P)
    hop.append(dict(alpha=round(P / N, 4), P=P, overlap=round(m, 4)))
    print("alpha=%.3f P=%3d overlap=%.3f" % (P / N, P, m))
out["hopfield"] = dict(N=N, trials=20, sweeps=20, curve=hop, alpha_c_theory=0.138)

# ---------------------------------------------------------------- 实验二
def tracking(period, etas, steps=40000, noise=0.5, m=0.6, amp=0.4):
    """环境 = 稳定成分 m + 快变成分（每 period 步翻转）+ 噪声。

    etas = (eta_slow, eta_fast)。若 eta_slow=0，则是单时间尺度学习器。
    返回最后 1/3 步数上的均方误差。
    """
    ws, wf = 0.0, 0.0
    se, n = 0.0, 0
    for t in range(steps):
        base = amp * (1.0 if (t // period) % 2 == 0 else -1.0)
        lvl = 0.6 if t < steps // 2 else 0.2          # 慢漂移：目标水平在中期改变
        target = lvl + base + rng.normal(0, noise)
        pred = ws + wf
        e = target - pred
        ws += etas[0] * e
        wf += etas[1] * e
        if t > steps * 2 // 3:
            se += e * e
            n += 1
    return float(se / n)


periods = [200, 500, 1000, 2000, 5000, 10000]
grid_single = [(0.001,), (0.005,), (0.01,), (0.02,), (0.05,)]
single_best, single_by_eta = [], {}
for T in periods:
    best = None
    for (eta,) in grid_single:
        v = tracking(T, (0.0, eta))
        single_by_eta.setdefault(eta, []).append(round(v, 3))
        best = v if best is None else min(best, v)
    single_best.append(round(best, 4))
dual = [round(min(tracking(T, (0.001, eta)) for eta in (0.02, 0.05, 0.1)), 4) for T in periods]
for T, a, b in zip(periods, single_best, dual):
    print("period=%5d best_single=%.3f dual=%.3f" % (T, a, b))
out["tracking"] = dict(periods=periods, single_best=single_best, dual=dual,
                       single_grid={str(k): v for k, v in single_by_eta.items()},
                       params="level 0.6→0.2, amp=0.4, noise=0.5, eta_slow=0.001, eta_fast∈{0.02,0.05,0.1}")

json.dump(out, open(os.path.join(DATA, "exp_memory.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("wrote data/exp_memory.json")
