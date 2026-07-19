#!/usr/bin/env python3
"""Generate the hacker-style SVG asset set for the KiwiGaze GitHub profile.

Every asset is emitted in a dark and a light variant from one set of design
tokens. Pure stdlib; deterministic output.
"""

import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"
ADV = 0.6  # monospace advance as a fraction of font-size

DARK = {
    "bg": "#0b0f0d", "panel": "#0f1512", "panel2": "#131b17",
    "border": "#1e2c25", "fg": "#cfe3d8", "dim": "#5f7a6d",
    "green": "#00e69a", "green_soft": "#7ee2b8", "amber": "#f5b957",
    "cyan": "#62d0ff", "magenta": "#ff7ac2", "scan_op": "0.16",
    "chip": "#131b17", "eye": "#0b0f0d",
}
LIGHT = {
    "bg": "#f7f5ee", "panel": "#fffdf6", "panel2": "#f0ecdf",
    "border": "#ddd6c2", "fg": "#26382e", "dim": "#8a9787",
    "green": "#0a7d4f", "green_soft": "#3a9b72", "amber": "#a86d0a",
    "cyan": "#0e6f9e", "magenta": "#a8487d", "scan_op": "0.045",
    "chip": "#f0ecdf", "eye": "#fffdf6",
}

LANG_COLORS = {
    "TypeScript": "#3178c6", "Python": "#3572A5", "Go": "#00ADD8",
    "Swift": "#F05138", "React": "#61dafb", "Vue": "#41b883",
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cw(size: float) -> float:
    return size * ADV


STYLE = """
  <style>
    text { font-family: %s; }
    .a { opacity: 0; animation: ap 0.01s steps(1) forwards; }
    @keyframes ap { to { opacity: 1; } }
    .cur { animation: bl 1.1s steps(1) infinite; }
    @keyframes bl { 50%% { opacity: 0; } }
    @media (prefers-reduced-motion: reduce) {
      .a { animation: none; opacity: 1; }
      .cur { animation: none; }
    }
  </style>
""" % MONO


def svg_open(w: int, h: int, p: dict, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">\n'
        f"{STYLE}"
        f'  <defs>\n'
        f'    <pattern id="scan" width="2" height="3" patternUnits="userSpaceOnUse">\n'
        f'      <rect y="2" width="2" height="1" fill="#000000" opacity="{p["scan_op"]}"/>\n'
        f'    </pattern>\n'
        f'    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">\n'
        f'      <feDropShadow dx="0" dy="0" stdDeviation="2.4" flood-color="{p["green"]}" flood-opacity="0.5"/>\n'
        f'    </filter>\n'
        f'  </defs>\n'
    )


def panel(x, y, w, h, p, rx=12, fill=None):
    return (
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill or p["panel"]}" stroke="{p["border"]}" stroke-width="1.5"/>\n'
    )


def txt(x, y, size, fill, content, weight="normal", anchor="start",
        cls=None, delay=None, glow=False, spacing=None):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    c = f' class="{cls}"' if cls else ""
    d = f' style="animation-delay:{delay}s"' if delay is not None else ""
    g = ' filter="url(#glow)"' if glow else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    wt = f' font-weight="{weight}"' if weight != "normal" else ""
    return (
        f'  <text x="{x}" y="{y}" font-size="{size}"{wt} fill="{fill}"{a}{c}{d}{g}{ls}>'
        f"{content}</text>\n"
    )


def typed(x, y, size, fill, s, t0, dt, weight="normal"):
    """Per-character typing animation; returns (svg, finish_time, end_x)."""
    out = f'  <text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}">\n'
    for i, ch in enumerate(s):
        d = t0 + i * dt
        out += (
            f'    <tspan x="{x + i * cw(size):.1f}" class="a" '
            f'style="animation-delay:{d:.2f}s">{esc(ch)}</tspan>\n'
        )
    out += "  </text>\n"
    return out, t0 + len(s) * dt, x + len(s) * cw(size)


def corner_brackets(x, y, w, h, p, arm=14, pad=0):
    c = p["green"]
    o = []
    for cx, cy, dx, dy in [
        (x + pad, y + pad, 1, 1), (x + w - pad, y + pad, -1, 1),
        (x + pad, y + h - pad, 1, -1), (x + w - pad, y + h - pad, -1, -1),
    ]:
        o.append(
            f'  <path d="M {cx} {cy + dy * arm} L {cx} {cy} L {cx + dx * arm} {cy}" '
            f'fill="none" stroke="{c}" stroke-width="2" opacity="0.9"/>\n'
        )
    return "".join(o)


def titlebar(w, p, title):
    out = f'  <path d="M 1 37 H {w - 1}" stroke="{p["border"]}" stroke-width="1"/>\n'
    for i, col in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        out += f'  <circle cx="{26 + i * 20}" cy="19" r="5.5" fill="{col}"/>\n'
    out += txt(w / 2, 23, 12, p["dim"], esc(title), anchor="middle")
    return out


# ---------------------------------------------------------------- boot.svg
def gen_boot(p):
    W, H = 860, 216
    s = svg_open(W, H, p, "terminal intro: whoami — qi yijiazhen, kiwigaze")
    s += panel(0.75, 0.75, W - 1.5, H - 1.5, p)
    s += titlebar(W, p, "kiwigaze@hk — zsh")
    X, FS = 22, 13.5
    LH = 22
    y = 66

    def prompt(y_, cls=None, delay=None):
        seg = ""
        c = f' class="{cls}"' if cls else ""
        d = f' style="animation-delay:{delay}s"' if delay is not None else ""
        seg += f'  <text x="{X}" y="{y_}" font-size="{FS}"{c}{d}>'
        seg += f'<tspan fill="{p["green"]}" font-weight="bold">kiwigaze@hk</tspan>'
        seg += f'<tspan fill="{p["dim"]}">:</tspan>'
        seg += f'<tspan fill="{p["cyan"]}">~</tspan>'
        seg += f'<tspan fill="{p["dim"]}">$ </tspan>'
        seg += "</text>\n"
        return seg, X + 15 * cw(FS)

    # line 1: prompt + typed whoami
    seg, px = prompt(y)
    s += seg
    t_seg, t_end, _ = typed(px, y, FS, p["fg"], "whoami", 0.4, 0.09)
    s += t_seg
    # output
    y += LH
    name_line = (
        f'<tspan fill="{p["green"]}" font-weight="bold">qi yijiazhen</tspan>'
        f'<tspan fill="{p["dim"]}"> · </tspan>'
        f'<tspan fill="{p["amber"]}">@kiwigaze</tspan>'
    )
    s += (
        f'  <text x="{X}" y="{y}" font-size="15" class="a" '
        f'style="animation-delay:{t_end + 0.25:.2f}s" filter="url(#glow)">{name_line}</text>\n'
    )
    y += LH
    s += txt(X, y, FS, p["fg"],
             esc("full-stack engineer / ai-tooling hacker — hong kong"),
             cls="a", delay=round(t_end + 0.45, 2))

    # line 2: prompt + typed ls ~/now
    y += LH + 4
    seg, px = prompt(y, cls="a", delay=round(t_end + 0.9, 2))
    s += seg
    t_seg, t2_end, _ = typed(px, y, FS, p["fg"], "ls ~/now", t_end + 1.05, 0.09)
    s += t_seg
    y += LH
    dirs = ["simplifying/", "glm-for-copilot/", "velata/", "multica-prs/", "arxiv-chat/"]
    dx = X
    dseg = f'  <text x="{X}" y="{y}" font-size="{FS}" class="a" style="animation-delay:{t2_end + 0.25:.2f}s">'
    for d_ in dirs:
        dseg += f'<tspan x="{dx:.1f}" fill="{p["cyan"]}" font-weight="bold">{esc(d_)}</tspan>'
        dx += (len(d_) + 3) * cw(FS)
    dseg += "</text>\n"
    s += dseg

    # line 3: fresh prompt + blinking cursor
    y += LH + 4
    seg, px = prompt(y, cls="a", delay=round(t2_end + 0.6, 2))
    s += seg
    s += (
        f'  <g class="a" style="animation-delay:{t2_end + 0.6:.2f}s">'
        f'<rect x="{px:.1f}" y="{y - 12}" width="8.5" height="15" fill="{p["green"]}" class="cur"/></g>\n'
    )

    s += f'  <rect x="1" y="38" width="{W - 2}" height="{H - 39}" fill="url(#scan)" rx="0"/>\n'
    s += "</svg>\n"
    return s


# ------------------------------------------------------------- sysinfo.svg
KIWI = [
    "..................",
    "........######....",
    "......##########..",
    ".....###########B.",
    "....############.B",
    "...#############.B",
    "...#############..",
    "....###########...",
    ".....#########....",
    "......###..###....",
    "......LL....LL....",
    "..................",
]

SYS_FIELDS = [
    ("host",   [("Hong Kong · UTC+8", "fg")]),
    ("os",     [("macOS / darwin", "fg"), (" · deploys on ubuntu", "dim")]),
    ("uptime", [("shipping since 2021", "fg")]),
    ("role",   [("full-stack engineer · ai tooling", "fg")]),
    ("now",    [("founder-mode @ ", "fg"), ("simplifying", "green"), (" (pre-launch)", "dim")]),
    ("edu",    [("HKUST MSc — incoming", "fg")]),
    ("oss",    [("multica-ai/multica", "green"), (" — 4 PRs merged · 41k+ ★", "fg")]),
    ("langs",  [("typescript · python · go · swift", "fg")]),
    ("web",    [("qiyijiazhen.com", "cyan")]),
]


def gen_sysinfo(p):
    W, H = 860, 296
    s = svg_open(W, H, p, "system card: kiwigaze at hong kong — role, focus, oss, stack")
    s += panel(0.75, 0.75, W - 1.5, H - 1.5, p)
    s += corner_brackets(14, 14, W - 28, H - 28, p)

    # pixel kiwi, 11px cells
    cell = 11
    gx, gy = 36, (H - len(KIWI) * cell) // 2
    for ry, row in enumerate(KIWI):
        for rx, ch in enumerate(row):
            if ch == ".":
                continue
            if ch == "#":
                fill = p["green"] if (rx * 7 + ry * 13) % 5 < 3 else p["green_soft"]
            elif ch == "B":
                fill = p["amber"]
            elif ch == "L":
                fill = p["amber"]
            s += (
                f'  <rect x="{gx + rx * cell}" y="{gy + ry * cell}" '
                f'width="{cell - 1}" height="{cell - 1}" fill="{fill}"/>\n'
            )
    # eye
    s += (
        f'  <rect x="{gx + 14 * cell + 2}" y="{gy + 2 * cell + 2}" '
        f'width="{cell - 5}" height="{cell - 5}" fill="{p["eye"]}"/>\n'
    )
    s += txt(gx + 9 * cell, gy + len(KIWI) * cell + 16, 11.5, p["dim"],
             "kiwi.gaze(1)", anchor="middle")

    # info block
    ix, iy = 280, 52
    s += txt(ix, iy, 16, p["green"], "kiwigaze", weight="bold", glow=True)
    s += txt(ix + 8 * cw(16), iy, 16, p["dim"], "@hongkong")
    s += txt(ix, iy + 16, 12, p["dim"], esc("-" * 30))
    fy = iy + 40
    for label, parts in SYS_FIELDS:
        line = f'<tspan fill="{p["amber"]}">{label}</tspan>'
        line += f'<tspan x="{ix + 9 * cw(13)}">'
        line = f'  <text x="{ix}" y="{fy}" font-size="13">{line}'
        for text_, color in parts:
            line += f'<tspan fill="{p[color]}">{esc(text_)}</tspan>'
        line += "</tspan></text>\n"
        s += line
        fy += 22

    # neofetch palette dots
    fy += 4
    for i, col in enumerate(["green", "green_soft", "amber", "cyan", "magenta", "fg", "dim", "border"]):
        s += (
            f'  <rect x="{ix + i * 26}" y="{fy - 10}" width="20" height="12" '
            f'rx="2" fill="{p[col]}"/>\n'
        )
    s += f'  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" fill="url(#scan)" rx="12"/>\n'
    s += "</svg>\n"
    return s


# ---------------------------------------------------------------- cards
CARDS = [
    {
        "slug": "glm-for-copilot",
        "title": "~/glm-for-copilot",
        "tag": "[SHIPPED]", "tagc": "amber",
        "desc": ["GLM-5.2 + full GLM lineup inside GitHub Copilot",
                 "Chat — BYOK VS Code extension · agent + tools"],
        "langs": ["TypeScript"],
        "note": "vsix releases · byok",
    },
    {
        "slug": "multica",
        "title": "multica-ai/multica",
        "tag": "[OSS·MERGED]", "tagc": "green",
        "desc": ["Open-source managed agents platform — built its",
                 "slash-command skills palette (React + Go daemon)"],
        "langs": ["Go", "React"],
        "note": "4 PRs merged · 41k+ ★",
    },
    {
        "slug": "velata",
        "title": "~/velata",
        "tag": "[ACTIVE]", "tagc": "cyan",
        "desc": ["macOS floating scratchpad that rewrites messy",
                 "dictated text into clean, paste-ready copy"],
        "langs": ["TypeScript"],
        "note": "in active development",
    },
    {
        "slug": "arxiv-chat",
        "title": "~/arXiv-chat",
        "tag": "[RESEARCH]", "tagc": "magenta",
        "desc": ["Local-first agentic RAG assistant for arXiv CS.AI",
                 "papers — retrieval, tools & citations on-device"],
        "langs": ["Python"],
        "note": "local-first rag",
    },
    {
        "slug": "codex-status-bar",
        "title": "~/codex-status-bar",
        "tag": "[SHIPPED]", "tagc": "amber",
        "desc": ["Tiny macOS menu-bar app showing the Codex CLI's",
                 "live status — thinking / running / awaiting"],
        "langs": ["Swift"],
        "note": "native menu-bar",
    },
    {
        "slug": "omnisearches",
        "title": "~/OmniSearches",
        "tag": "[SHIPPED]", "tagc": "amber",
        "desc": ["Free, open-source AI search engine — answers with",
                 "live web grounding, cited sources & image search"],
        "langs": ["TypeScript"],
        "note": "ai search",
    },
]


def gen_card(p, card):
    W, H = 420, 132
    s = svg_open(W, H, p, f'project {card["title"]}: {card["desc"][0]}')
    s += panel(0.75, 0.75, W - 1.5, H - 1.5, p, rx=10)
    s += corner_brackets(8, 8, W - 16, H - 16, p, arm=10)
    s += txt(24, 36, 14.5, p["green"], esc("▸ ") + esc(card["title"]), weight="bold")
    s += txt(W - 22, 35, 11, p[card["tagc"]], esc(card["tag"]), anchor="end", weight="bold")
    s += txt(24, 62, 12, p["fg"], esc(card["desc"][0]))
    s += txt(24, 79, 12, p["fg"], esc(card["desc"][1]))
    s += (
        f'  <path d="M 24 95 H {W - 24}" stroke="{p["border"]}" '
        f'stroke-width="1" stroke-dasharray="3 4"/>\n'
    )
    lx = 24
    for lang in card["langs"]:
        s += f'  <circle cx="{lx + 4}" cy="{111}" r="4.2" fill="{LANG_COLORS[lang]}"/>\n'
        s += txt(lx + 13, 115, 11.5, p["dim"], esc(lang))
        lx += 13 + len(lang) * cw(11.5) + 16
    s += txt(W - 22, 115, 11, p["amber"], esc(card["note"]), anchor="end")
    s += "</svg>\n"
    return s


# ---------------------------------------------------------------- skills
SKILL_ROWS = [
    ("languages", ["TypeScript", "Python", "Go", "Swift"], False),
    ("backend", ["Node.js", "Express", "FastAPI", "PostgreSQL", "Redis", "REST APIs"], False),
    ("frontend", ["React", "Next.js", "Vue", "Electron"], False),
    ("ai / agents", ["LLM tool-calling", "RAG pipelines", "MCP", "agent workflows"], True),
    ("platform", ["Docker", "GitHub Actions", "macOS apps", "CI release pipelines"], False),
]


def gen_skills(p):
    W, H = 860, 250
    s = svg_open(W, H, p, "stack: languages, backend, frontend, ai agents, platform")
    s += panel(0.75, 0.75, W - 1.5, H - 1.5, p)
    s += txt(24, 38, 14, p["dim"], "$")
    s += txt(24 + 2 * cw(14), 38, 14, p["green"],
             "stack --list --grouped", weight="bold")
    y = 76
    for label, chips, hot in SKILL_ROWS:
        s += txt(150, y + 4, 12.5, p["amber"], esc(label), anchor="end")
        x = 172
        for chip in chips:
            wpx = len(chip) * cw(12) + 20
            stroke = p["green"] if hot else p["border"]
            s += (
                f'  <rect x="{x:.1f}" y="{y - 12}" width="{wpx:.1f}" height="23" rx="6" '
                f'fill="{p["chip"]}" stroke="{stroke}" stroke-width="1.2"/>\n'
            )
            s += txt(x + 10, y + 4, 12, p["fg"], esc(chip))
            x += wpx + 9
        y += 36
    s += "</svg>\n"
    return s


def write(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(content)
    print(f"{name:32s} {len(content):>7,d} bytes")


def main():
    global STYLE
    os.makedirs(OUT, exist_ok=True)
    if os.environ.get("STATIC_DEBUG"):
        STYLE = STYLE.replace("opacity: 0;", "opacity: 1;")
    for suffix, pal in [("dark", DARK), ("light", LIGHT)]:
        write(f"boot-{suffix}.svg", gen_boot(pal))
        write(f"sysinfo-{suffix}.svg", gen_sysinfo(pal))
        write(f"skills-{suffix}.svg", gen_skills(pal))
        for card in CARDS:
            write(f'card-{card["slug"]}-{suffix}.svg', gen_card(pal, card))


if __name__ == "__main__":
    main()
