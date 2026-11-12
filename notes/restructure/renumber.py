# -*- coding: utf-8 -*-
"""renumber.py —— 在第四部分插入新第 12 章，把旧 ch12—ch25 顺移为 ch13—ch26。

只动“编号引用”，不动正文内容。规则：
  章号 n∈[12,25] → n+1
  节／图／表／式／定义／断言／警告／锚点 id 的章号部分同样 +1
  范围引用（第 10—13 章）两端分别按同一规则映射
  第 N 部分 不动

用法：python notes/restructure/renumber.py [--apply]
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(HERE, "source")
APPLY = "--apply" in sys.argv


def shift(n):
    n = int(n)
    return n + 1 if 12 <= n <= 25 else n


def num(n):
    return str(shift(n))


# 先长后短：范围、带标签的编号、再单项
RULES = [
    # 第 10—13 章
    (re.compile(r"第(\s*)(\d{1,2})(—|–)(\d{1,2})(\s*)章"),
     lambda m: "第%s%s%s%s%s章" % (m.group(1), num(m.group(2)), m.group(3), num(m.group(4)), m.group(5))),
    # 第 13 章 / <h2>第13章
    (re.compile(r"第(\s*)(\d{1,2})(\s*)章"),
     lambda m: "第%s%s%s章" % (m.group(1), num(m.group(2)), m.group(3))),
    # 第 13.4 节
    (re.compile(r"第(\s*)(\d{1,2})\.(\d{1,2})([a-z]?)(\s*)节"),
     lambda m: "第%s%s.%s%s%s节" % (m.group(1), num(m.group(2)), m.group(3), m.group(4), m.group(5))),
    # 图 13.1 / 表 13.2 / 图 13.1a
    (re.compile(r"([图表])(\s*)(\d{1,2})\.(\d{1,2})([a-z]?)"),
     lambda m: "%s%s%s.%s%s" % (m.group(1), m.group(2), num(m.group(3)), m.group(4), m.group(5))),
    # 式(13.1)
    (re.compile(r"式\((\d{1,2})\.(\d{1,2})([a-z]?)\)"),
     lambda m: "式(%s.%s%s)" % (num(m.group(1)), m.group(2), m.group(3))),
    # 定义 13.1 / 断言 13.2 / 警告 13.5.1 / 深思 13.1 / 假设 13.3
    (re.compile(r"(定义|断言|警告|深思|假设|命题)(\s*)(\d{1,2})\.(\d{1,2})(\.\d{1,2})?"),
     lambda m: "%s%s%s.%s%s" % (m.group(1), m.group(2), num(m.group(3)), m.group(4), m.group(5) or "")),
    # 锚点 id：sec13-4
    (re.compile(r"sec(\d{1,2})-(\d{1,2})"),
     lambda m: "sec%s-%s" % (num(m.group(1)), m.group(2))),
    # 公式编号 <span class="num">(13.1)</span>
    (re.compile(r'(class="num">\()(\d{1,2})\.(\d{1,2})([a-z]?)'),
     lambda m: "%s%s.%s%s" % (m.group(1), num(m.group(2)), m.group(3), m.group(4))),
    # (13.1) 出现在正文括号里
    (re.compile(r"（(\d{1,2})\.(\d{1,2})）"),
     lambda m: "（%s.%s）" % (num(m.group(1)), m.group(2))),
]


def transform(text):
    for pat, fn in RULES:
        text = pat.sub(fn, text)
    return text


def main():
    # 1) 文件改名：降序，避免碰撞
    for n in range(25, 11, -1):
        old = os.path.join(SRC, "ch%02d.html" % n)
        new = os.path.join(SRC, "ch%02d.html" % (n + 1))
        if os.path.exists(old):
            if APPLY:
                os.rename(old, new)
            print("rename ch%02d -> ch%02d" % (n, n + 1))

    # 2) 全部源文件与 parts.json 的引用顺移
    targets = [os.path.join(SRC, f) for f in sorted(os.listdir(SRC)) if f.endswith(".html")]
    targets.append(os.path.join(SRC, "parts.json"))
    for p in targets:
        t0 = open(p, encoding="utf-8").read()
        t1 = transform(t0)
        if t0 != t1:
            n = sum(1 for a, b in zip(t0.splitlines(), t1.splitlines()) if a != b)
            print("%-30s %3d 行变更" % (os.path.basename(p), n))
            if APPLY:
                open(p, "w", encoding="utf-8").write(t1)


if __name__ == "__main__":
    main()
