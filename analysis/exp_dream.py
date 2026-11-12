# -*- coding: utf-8 -*-
"""exp_dream.py ——《遗忘的边界》第 12 章：对账 vs 重组（可复算）。

协议见 analysis/PREREG_exp_dream.md（写于本脚本运行之前，永不改写）。
输出：data/exp_dream.json

替身世界：40 个二值事实，真值以每会话概率 h 翻转；每会话触碰 8 个，
观察带噪（错误率 p），写一条笔记；每 k 会话整合一次；查询按"最新笔记优先"作答。
四个臂：A 累积 / B 重组（不核对）/ C 对账（按 q 抽查，仅对可验证的 ρ 部分有效）。
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

F, S, M = 40, 60, 8          # 事实数、会话数、每会话触碰数
H = 0.12                     # 真值翻转的每会话风险率（平均寿命 L = 1/H ≈ 8.3）
P = 0.15                     # 观察错误率
SEEDS = list(range(20261101, 20261121))
QUERIES = 8                  # 每会话末抽取作答的事实数


# ------------------------------------------------------------------ 世界
def world(seed, rho):
    """返回 truth[s,f] 与可验证集合 V（|V| = round(rho*F)）。"""
    rng = np.random.default_rng(seed)
    truth = np.zeros((S, F), dtype=np.int8)
    truth[0] = rng.integers(0, 2, F)
    for s in range(1, S):
        flip = rng.random(F) < H
        truth[s] = np.where(flip, 1 - truth[s - 1], truth[s - 1])
    nv = int(round(rho * F))
    V = set(rng.choice(F, size=nv, replace=False).tolist())
    return truth, V, rng


# ------------------------------------------------------------------ 记忆
class Store:
    """笔记 = [fact, val, sess, conf, ins]。"""

    def __init__(self):
        self.notes = []
        self.counter = 0

    def write(self, fact, val, sess):
        self.counter += 1
        self.notes.append([fact, val, sess, 1.0, self.counter])

    def answer(self, fact):
        best = None
        for n in self.notes:
            if n[0] != fact:
                continue
            if best is None or (n[2], n[4]) > (best[2], best[4]):
                best = n
        return None if best is None else (best[1], best[3])

    def consolidate(self, sess, mode, q, V, truth_s, rng):
        """mode: 'merge'（不核对）或 'audit'（按 q 抽查，仅 V 内有效）。"""
        groups = {}
        for n in self.notes:
            groups.setdefault(n[0], []).append(n)
        for fact, g in groups.items():
            votes1 = sum(1 for n in g if n[1] == 1)
            votes0 = len(g) - votes1
            val = 1 if votes1 > votes0 else (0 if votes0 > votes1 else g[-1][1])
            conf = abs(votes1 - votes0) / len(g)
            latest = max(n[2] for n in g)
            if mode == "audit" and rng.random() < q:
                if fact in V:                      # 日志里有可核对的记录
                    val, conf = int(truth_s[fact]), 1.0
                # 覆盖之外：白花的算力，什么也不改
            self.counter += 1
            keep = [fact, val, latest, conf, self.counter]
            self.notes = [n for n in self.notes if n[0] != fact]
            self.notes.append(keep)


# ------------------------------------------------------------------ 一次运行
def run(seed, mode="none", q=1.0, k=4, rho=1.0):
    truth, V, rng = world(seed, rho)
    st = Store()
    o = {"hit": 0, "n": 0, "conf_hit": 0, "conf_n": 0, "store": []}
    for s in range(S):
        touched = rng.choice(F, size=M, replace=False)
        for f in touched:
            seen = truth[s][f] if rng.random() > P else 1 - truth[s][f]
            st.write(int(f), int(seen), s)
        if mode != "none" and k <= S and (s + 1) % k == 0:
            st.consolidate(s, mode, q, V, truth[s], rng)
        for f in rng.choice(F, size=QUERIES, replace=False):
            a = st.answer(int(f))
            ok = (a is not None and a[0] == truth[s][f])
            o["n"] += 1
            o["hit"] += int(ok)
            if a is not None and a[1] >= 0.6:
                o["conf_n"] += 1
                o["conf_hit"] += int(ok)
        o["store"].append(len(st.notes))
    out = {
        "accuracy": o["hit"] / o["n"],
        "confident_wrong": (1 - o["conf_hit"] / o["conf_n"]) if o["conf_n"] else 0.0,
        "confident_share": o["conf_n"] / o["n"],
        "store": float(np.mean(o["store"])),
    }
    return out


def agg(rows, key):
    v = np.array([r[key] for r in rows], dtype=float)
    boots = [np.mean(np.random.default_rng(1000 + i).choice(v, size=len(v), replace=True))
             for i in range(2000)]
    return {"mean": round(float(v.mean()), 4),
            "lo": round(float(np.percentile(boots, 2.5)), 4),
            "hi": round(float(np.percentile(boots, 97.5)), 4)}


def sweep(fn):
    rows = [fn(s) for s in SEEDS]
    return {k: agg(rows, k) for k in ("accuracy", "confident_wrong", "confident_share", "store")}


out = {"seed_first": SEEDS[0], "seeds": len(SEEDS),
       "params": {"F": F, "S": S, "M": M, "h": H, "L": round(1 / H, 2), "p": P, "q_per_session": QUERIES}}

print("== 主对照（k=4, rho=1）")
main = {
    "A_none": sweep(lambda s: run(s, "none")),
    "B_merge": sweep(lambda s: run(s, "merge", 0, 4, 1.0)),
    "C_audit": sweep(lambda s: run(s, "audit", 1.0, 4, 1.0)),
    "D_audit_rho1_k1": sweep(lambda s: run(s, "audit", 1.0, 1, 1.0)),
}
for k, v in main.items():
    print(f"  {k:18s} acc={v['accuracy']['mean']:.3f} "
          f"[{v['accuracy']['lo']:.3f},{v['accuracy']['hi']:.3f}] "
          f"conf_wrong={v['confident_wrong']['mean']:.3f} store={v['store']['mean']:.1f}")
out["main"] = main

print("== 审计率扫描（k=4）")
qs = [round(0.1 * i, 1) for i in range(11)]
qsweep = {}
for rho in (0.2, 0.5, 1.0):
    qsweep[str(rho)] = {str(q): sweep(lambda s, q=q: run(s, "audit", q, 4, rho)) for q in qs}
    line = "  rho=%.1f " % rho + " ".join(
        "%.2f:%.3f" % (q, qsweep[str(rho)][str(q)]["accuracy"]["mean"]) for q in qs)
    print(line)
out["q_sweep"] = qsweep

print("== 整合周期扫描（rho=1, q=1）")
ks = [1, 2, 4, 8, 16, 32]
ksweep = {str(k): sweep(lambda s, k=k: run(s, "audit", 1.0, k, 1.0)) for k in ks}
for k in ks:
    v = ksweep[str(k)]
    print(f"  k={k:3d} acc={v['accuracy']['mean']:.3f} store={v['store']['mean']:.1f} "
          f"conf_wrong={v['confident_wrong']['mean']:.3f}")
out["k_sweep"] = ksweep

print("== 可验证性扫描（k=4, q=1；预注册只覆盖 0.2/0.5/1.0，本扫描为事后追加）")
rhos = [round(0.1 * i, 1) for i in range(1, 11)]
rho_post = {str(r): sweep(lambda s, r=r: run(s, "audit", 1.0, 4, r)) for r in rhos}
for r in rhos:
    v = rho_post[str(r)]
    print(f"  rho={r:.1f} acc={v['accuracy']['mean']:.3f} [+{v['accuracy']['mean']-main['A_none']['accuracy']['mean']:.3f}]")
sl = np.polyfit([r for r in rhos], [rho_post[str(r)]["accuracy"]["mean"] for r in rhos], 1)
out["rho_sweep_posthoc"] = {"sweep": rho_post, "slope": round(float(sl[0]), 4),
                            "intercept": round(float(sl[1]), 4), "note": "事后追加，不属预注册"}
print("  线性拟合：gain ≈ %.3f * rho %+.3f" % (sl[0], sl[1]))

# ---------------------------------------------------------------- 裁决
a = main["A_none"]["accuracy"]["mean"]
b = main["B_merge"]["accuracy"]["mean"]
c = main["C_audit"]["accuracy"]["mean"]
f1 = (c >= a + 0.05) and (c >= b + 0.05)
# F2：是否存在 q，使 C 不优于 A，且存在更大 q 使 C 优于 A
ser = [qsweep["1.0"][str(q)]["accuracy"]["mean"] for q in qs]
cross = None
for i in range(1, len(qs)):
    if ser[i] > a and all(ser[j] <= a + 1e-9 for j in range(i)) and ser[0] <= a:
        cross = qs[i]
f2 = cross is not None
# F3：k 扫描在 k≫L 一侧是否下降
kacc = {k: ksweep[str(k)]["accuracy"]["mean"] for k in ks}
argmax = max(kacc, key=lambda k: kacc[k])
f3 = kacc[32] < kacc[argmax] - 0.02
# F4：合并是否制造自信的错误
f4 = main["B_merge"]["confident_wrong"]["mean"] > main["A_none"]["confident_wrong"]["mean"]
out["adjudication"] = {
    "F1_audit_beats": dict(pass_=bool(f1), A=a, B=b, C=c),
    "F2_threshold": dict(pass_=bool(f2), q_star=cross, series=[round(x, 4) for x in ser], A=a),
    "F3_cadence": dict(pass_=bool(f3), argmax_k=argmax, by_k={str(k): round(v, 4) for k, v in kacc.items()}, L=round(1 / H, 2)),
    "F4_confident_wrong": dict(pass_=bool(f4),
                               A=main["A_none"]["confident_wrong"]["mean"],
                               B=main["B_merge"]["confident_wrong"]["mean"]),
}
print("== 裁决")
for k, v in out["adjudication"].items():
    print("  ", k, "→", "触发（主张被削弱）" if v["pass_"] is False else "未触发（主张站住）", v)

with open(os.path.join(DATA, "exp_dream.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("wrote data/exp_dream.json")
