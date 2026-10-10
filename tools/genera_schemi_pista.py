#!/usr/bin/env python3
"""Genera gli schemi SVG della pista e dei circuiti di traffico.

Uso
---
    python3 tools/genera_schemi_pista.py

Riscrive tutti i file in static/images/pista/schema-*.svg. L'output e
deterministico: rigenerare senza toccare lo script produce file identici.

Per modificare il disegno si cambiano le costanti qui sotto (distanze in metri)
o le singole funzioni draft*, non i path dell'SVG a mano.

Nota sui colori
---------------
Ogni elemento porta il colore due volte: come attributo di presentazione (tema
chiaro) e via CSS con var(). Nei browser vince il CSS, quindi inlinando l'SVG
nella pagina eredita le variabili del tema e il dark mode; altrove (librsvg,
thumbnailer, convertitori, che non supportano var()) resta l'attributo e il
disegno non sparisce. Attenzione: i token locali non devono avere lo stesso
nome di quelli del sito, altrimenti --x: var(--x, fallback) e un ciclo e il
valore viene scartato.

Sistema di riferimento
----------------------
Mappa orientata a nord: x verso est, y verso sud (coordinate schermo).
QFU 14 = 140 gradi, quindi la pista corre da NW (testata 14) a SE (testata 32).

Frame locale, dentro il gruppo ruotato:
  x locale = lungo la pista, verso la testata 32 (sud-est)
  y locale = perpendicolare, verso SUD-OVEST (il lato dei circuiti)
rotate(50) manda x locale sulla direzione 140.

Circuiti: 14 destro e 32 sinistro cadono entrambi a sud-ovest, quindi
condividono lo stesso corridoio percorso nei due sensi.
"""
import math
from pathlib import Path

HDG = 140.0
ROT = HDG - 90.0
C, S = math.cos(math.radians(ROT)), math.sin(math.radians(ROT))

RWY_M, RWY_U = 860.0, 230.0
U = RWY_U / RWY_M                      # unita SVG per metro

L = RWY_U / 2                          # semi-lunghezza pista
HW = 60.0 * U / 2                      # semi-larghezza (60 m)
W = 700.0 * U                          # sottovento, scostamento dall'asse
E = L + 600.0 * U                      # semi-lunghezza del circuito
YMOT = 1050.0 * U                      # autostrada

CASTLE = (-L, W)                       # sul sottovento, all'altezza della 14
SOCK = (46.0, -46.0)                   # manica a vento, lato est

OUT = Path(__file__).resolve().parent.parent / "static" / "images" / "pista"

COL = {"ink": "#1a1a1a", "mut": "#5a6470", "fnt": "#a0aab4", "gold": "#9a6f2a",
       "dim": "#c4a060", "surf": "#edeae4", "elev": "#e4e0d8", "base": "#f5f3ef"}

# Colori anche come attributi di presentazione: il CSS con var() li sovrascrive
# nei browser, ma dove var() non e supportato (librsvg, thumbnailer, convertitori)
# restano questi e il disegno resta leggibile.
FALLBACK = {
    "rwy": ("elev", "ink"),    "axis": (None, "surf"),   "thrBar": (None, "ink"),
    "circ": (None, "gold"),    "c14": (None, "gold"),    "c32": (None, "mut"),
    "band": ("gold", None),    "arr": ("gold", None),    "a14": ("gold", None),
    "a32": ("mut", None),      "sockC": ("gold", None),  "road": (None, "mut"),
    "roadM": (None, "base"),   "rule": (None, "gold"),   "pict": (None, "ink"),
    "pictF": ("base", "ink"),  "legbox": ("surf", "fnt"),
    "lbl": ("mut", None),      "lblS": ("fnt", None),    "thr": ("ink", None),
    "big": ("ink", None),      "sub": ("mut", None),
}


def A(*classes, halo=False, fb=None):
    """class=... piu i colori di fallback. fb=(fill,stroke) li sovrascrive,
    necessario quando una bozza ridefinisce la classe nel suo CSS."""
    out = f'class="{" ".join(classes)}"'
    for c in classes:
        if c in FALLBACK:
            fill, stroke = fb if fb else FALLBACK[c]
            out += f' fill="{COL[fill]}"' if fill else ' fill="none"'
            if stroke:
                out += f' stroke="{COL[stroke]}"'
            break
    if halo:
        out = out.replace('class="', 'class="halo ', 1)
        out += (f' stroke="{COL["base"]}" stroke-width="6" '
                f'stroke-linejoin="round" paint-order="stroke"')
    return out


def loc(x, y, k=1.0, cx=0.0, cy=0.0):
    return (cx + k * (C * x - S * y), cy + k * (S * x + C * y))


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def palette(extra=""):
    return f"""
    .dia {{
      --ink: var(--text-primary,#1a1a1a); --mut: var(--text-muted,#5a6470);
      --fnt: var(--text-faint,#a0aab4);   --acc: var(--gold,#9a6f2a);
      --dim: var(--gold-dim,#c4a060);     --surf: var(--bg-surface,#edeae4);
      --elev: var(--bg-elevated,#e4e0d8); --base: var(--bg-base,#f5f3ef);
    }}
    @media (prefers-color-scheme: dark) {{
      .dia {{
        --ink: var(--text-primary,#e8e4dc); --mut: var(--text-muted,#8a9ba8);
        --fnt: var(--text-faint,#4a5662);   --acc: var(--gold,#c8a96e);
        --dim: var(--gold-dim,#8a6f3a);     --surf: var(--bg-surface,#111820);
        --elev: var(--bg-elevated,#161e2a); --base: var(--bg-base,#0d1117);
      }}
    }}
    .dia text {{ font-family:'Barlow Condensed','Arial Narrow',Arial,sans-serif; }}
    .halo {{ stroke: var(--base); stroke-width:6px; stroke-linejoin:round;
             paint-order:stroke; }}
    .lbl  {{ font-size:17px; font-weight:500; letter-spacing:.14em;
             text-transform:uppercase; fill: var(--mut); }}
    .lblS {{ font-size:13px; font-weight:400; letter-spacing:.16em;
             text-transform:uppercase; fill: var(--fnt); }}
    .thr  {{ font-size:36px; font-weight:700; letter-spacing:.04em;
             fill: var(--ink); }}
    .rwy    {{ fill: var(--elev); stroke: var(--ink); stroke-width:1.6; }}
    .thrBar {{ stroke: var(--ink); stroke-width:3; }}
    .axis   {{ stroke: var(--surf); stroke-width:1.4; stroke-dasharray:9 9; }}
    .road   {{ stroke: var(--mut); fill:none; stroke-width:3; }}
    .roadM  {{ stroke: var(--base); stroke-width:1.2; fill:none; }}
    .pict   {{ fill:none; stroke: var(--ink); stroke-width:1.8;
               stroke-linejoin:round; }}
    .pictF  {{ fill: var(--base); stroke: var(--ink); stroke-width:1.8;
               stroke-linejoin:round; }}
    .sockC  {{ fill: var(--acc); stroke:none; }}
    {extra}
    """


def castle(x, y, w=30.0, h=19.0, m=6.0):
    x0 = x - w / 2
    s, g = w / 5, w / 5
    return (f"M{f(x0)},{f(y)} L{f(x0)},{f(y-h-m)} L{f(x0+s)},{f(y-h-m)} "
            f"L{f(x0+s)},{f(y-h)} L{f(x0+s+g)},{f(y-h)} "
            f"L{f(x0+s+g)},{f(y-h-m)} L{f(x0+2*s+g)},{f(y-h-m)} "
            f"L{f(x0+2*s+g)},{f(y-h)} L{f(x0+2*s+2*g)},{f(y-h)} "
            f"L{f(x0+2*s+2*g)},{f(y-h-m)} L{f(x0+w)},{f(y-h-m)} "
            f"L{f(x0+w)},{f(y)} Z")


def windsock(x, y, sc=1.0):
    h, ln = 32 * sc, 26 * sc
    return (f'<line {A("pict")} x1="{f(x)}" y1="{f(y)}" x2="{f(x)}" '
            f'y2="{f(y-h)}"/>'
            f'<path {A("sockC")} d="M{f(x+2)},{f(y-h)} '
            f'L{f(x+ln)},{f(y-h+5*sc)} L{f(x+ln)},{f(y-h+12*sc)} '
            f'L{f(x+2)},{f(y-h+14*sc)} Z"/>'
            f'<circle {A("pictF")} cx="{f(x)}" cy="{f(y)}" r="{f(2.8*sc)}"/>')


def racetrack(w, e=E, r=70.0):
    """Circuito: gamba sopravvento/finale sull'asse pista, sottovento a y=w."""
    return (f"M{f(-e+r)},0 H{f(e-r)} A{f(r)},{f(r)} 0 0 1 {f(e)},{f(r)} "
            f"V{f(w-r)} A{f(r)},{f(r)} 0 0 1 {f(e-r)},{f(w)} H{f(-e+r)} "
            f"A{f(r)},{f(r)} 0 0 1 {f(-e)},{f(w-r)} V{f(r)} "
            f"A{f(r)},{f(r)} 0 0 1 {f(-e+r)},0 Z")


def arrow(x, y, dx, dy, size=12.0, cls="arr"):
    n = math.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    px, py = -dy, dx
    return (f'<path {A(cls)} d="M{f(x+dx*size)},{f(y+dy*size)} '
            f'L{f(x-dx*size*.5+px*size*.64)},{f(y-dy*size*.5+py*size*.64)} '
            f'L{f(x-dx*size*.5-px*size*.64)},{f(y-dy*size*.5-py*size*.64)} Z"/>')


def north(x, y):
    return (f'<line {A("pict")} x1="{f(x)}" y1="{f(y)}" x2="{f(x)}" '
            f'y2="{f(y-32)}"/>'
            f'<path {A("sockC")} d="M{f(x)},{f(y-46)} L{f(x-7)},{f(y-28)} '
            f'L{f(x)},{f(y-33)} L{f(x+7)},{f(y-28)} Z"/>'
            f'<text {A("lbl", halo=True)} x="{f(x)}" y="{f(y+19)}" '
            f'text-anchor="middle">N</text>')


def scalebar(x, y, m=500, k=1.0):
    w = m * U * k
    return (f'<line {A("pict")} stroke-width="1.4" x1="{f(x)}" y1="{f(y)}" '
            f'x2="{f(x+w)}" y2="{f(y)}"/>'
            f'<line {A("pict")} stroke-width="1.4" x1="{f(x)}" y1="{f(y-5)}" '
            f'x2="{f(x)}" y2="{f(y+5)}"/>'
            f'<line {A("pict")} stroke-width="1.4" x1="{f(x+w)}" y1="{f(y-5)}" '
            f'x2="{f(x+w)}" y2="{f(y+5)}"/>'
            f'<text {A("lblS", halo=True)} x="{f(x+w/2)}" y="{f(y-11)}" '
            f'text-anchor="middle">{m} m</text>')


def runway(solid=False):
    """solid=True: pista piena (bozza banner), altrimenti riquadro chiaro."""
    rwy_fb = ("ink", None) if solid else None
    axis_fb = (None, "base") if solid else None
    out = [f'<rect {A("rwy", fb=rwy_fb)} x="{f(-L)}" y="{f(-HW)}" '
           f'width="{f(2*L)}" height="{f(2*HW)}" rx="1"/>']
    if not solid:
        for sx in (-1, 1):
            out.append(f'<line {A("thrBar")} x1="{f(sx*(L-4))}" '
                       f'y1="{f(-HW+1.5)}" x2="{f(sx*(L-4))}" '
                       f'y2="{f(HW-1.5)}"/>')
    out.append(f'<line {A("axis", fb=axis_fb)} x1="{f(-L+14)}" y1="0" '
               f'x2="{f(L-14)}" y2="0"/>')
    return "".join(out)


def motorway(width=3.0, mid=True):
    out = []
    for off in (-width * 1.1, width * 1.1):
        out.append(f'<line {A("road")} stroke-width="{f(width)}" x1="-900" '
                   f'y1="{f(YMOT+off)}" x2="900" y2="{f(YMOT+off)}"/>')
    if mid:
        out.append(f'<line {A("roadM")} x1="-900" y1="{f(YMOT)}" x2="900" '
                   f'y2="{f(YMOT)}"/>')
    return "".join(out)


def head(w, h, title, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" class="dia" role="img" '
            f'aria-labelledby="t d">\n<title id="t">{title}</title>\n'
            f'<desc id="d">{DESC}</desc>\n<style>{palette(css)}</style>\n')


DESC = ("Schema dell'aviosuperficie visto dall'alto su mappa orientata a nord. "
        "La pista 14/32 corre da nord-ovest a sud-est. I circuiti di traffico "
        "si sviluppano entrambi a sud-ovest della pista: destro per la 14, "
        "sinistro per la 32, quindi lo stesso corridoio percorso nei due sensi. "
        "Sul sottovento, all'altezza della testata 14, si trova un castello; "
        "piu a sud-ovest corre l'autostrada. La manica a vento e a est "
        "della pista.")


def group(k, cx, cy, body):
    return (f'<g transform="translate({f(cx)},{f(cy)}) rotate({f(ROT)}) '
            f'scale({f(k)})">{body}</g>\n')


def landmarks(k, cx, cy, sock_scale=1.0, sub=True):
    cas = loc(*CASTLE, k, cx, cy)
    sck = loc(*SOCK, k, cx, cy)
    o = [f'<path {A("pictF")} d="{castle(cas[0], cas[1] + 13)}"/>',
         f'<text {A("lbl", halo=True)} x="{f(cas[0])}" y="{f(cas[1]+36)}" '
         f'text-anchor="middle">Castello</text>',
         windsock(sck[0], sck[1], sock_scale)]
    if sub:
        o.append(f'<text {A("lbl", halo=True)} x="{f(sck[0]+34)}" '
                 f'y="{f(sck[1]-8)}">Manica a vento</text>')
    return "".join(o)


def thresholds(k, cx, cy, sub14="", sub32=""):
    a = loc(-L - 40, -74, k, cx, cy)
    b = loc(L + 40, -74, k, cx, cy)
    o = []
    for (x, y), n, s in ((a, "14", sub14), (b, "32", sub32)):
        o.append(f'<text {A("thr", halo=True)} x="{f(x)}" y="{f(y)}" '
                 f'text-anchor="middle">{n}</text>')
        if s:
            o.append(f'<text {A("lblS", halo=True)} x="{f(x)}" y="{f(y+19)}" '
                     f'text-anchor="middle">{s}</text>')
    return "".join(o)


# ──────────────────────────────────────────────────────────── bozza 1
def draft1():
    k, cx, cy = 1.0, 500.0, 325.0
    css = """
    .circ { fill:none; stroke: var(--acc); stroke-width:2.4;
            stroke-dasharray:15 9; }
    .arr  { fill: var(--acc); stroke:none; }
    """
    g = [f'<path {A("circ")} d="{racetrack(W)}"/>',
         arrow(-20, W, -1, 0), arrow(150, W, 1, 0),
         motorway(),
         runway(),
         f'<text {A("lblS", halo=True)} x="205" y="{f(YMOT-26)}">'
         f'Autostrada</text>',
         f'<text {A("lblS", halo=True)} x="26" y="{f(W+34)}">Sottovento</text>']

    a14 = loc(-20, W - 30, k, cx, cy)
    a32 = loc(150, W - 30, k, cx, cy)
    o = [thresholds(k, cx, cy),
         landmarks(k, cx, cy),
         f'<text {A("lbl", halo=True)} x="{f(a14[0])}" y="{f(a14[1])}" '
         f'text-anchor="middle">14</text>',
         f'<text {A("lbl", halo=True)} x="{f(a32[0])}" y="{f(a32[1])}" '
         f'text-anchor="middle">32</text>',
         north(928, 96), scalebar(60, 762, 500, k),
         f'<text {A("lblS", halo=True)} x="940" y="724" text-anchor="end">'
         f'Circuiti a sud-ovest</text>',
         f'<text {A("lblS", halo=True)} x="940" y="746" text-anchor="end">'
         f'14 destro · 32 sinistro</text>']

    return (head(1000, 800, "Pista 14/32 e circuito di traffico", css)
            + group(k, cx, cy, "".join(g)) + "".join(o) + "</svg>\n")


# ──────────────────────────────────────────────────────────── bozza 2
def draft2():
    k, cx, cy = 1.0, 500.0, 325.0
    W14, W32 = W * 0.72, W * 1.22
    css = """
    .c14  { fill:none; stroke: var(--acc); stroke-width:2.8; }
    .c32  { fill:none; stroke: var(--mut); stroke-width:2.2;
            stroke-dasharray:13 8; }
    .a14  { fill: var(--acc); stroke:none; }
    .a32  { fill: var(--mut);  stroke:none; }
    .field{ fill: var(--surf); stroke:none; opacity:.6; }
    .legbox{ fill: var(--surf); stroke: var(--fnt); stroke-width:1; opacity:.92; }
    """
    g = [motorway(),
         f'<path {A("c32")} d="{racetrack(W32, E + 30, 80)}"/>',
         f'<path {A("c14")} d="{racetrack(W14, E, 62)}"/>',
         arrow(-40, W14, -1, 0, 11, "a14"), arrow(140, W14, -1, 0, 11, "a14"),
         arrow(-30, W32, 1, 0, 10, "a32"), arrow(150, W32, 1, 0, 10, "a32"),
         runway(),
         f'<text {A("lblS", halo=True)} x="205" y="{f(YMOT-26)}">'
         f'Autostrada</text>']

    lx, ly = 716, 60
    o = [thresholds(k, cx, cy),
         landmarks(k, cx, cy),
         north(934, 700), scalebar(60, 762, 500, k),
         f'<rect {A("legbox")} x="{lx}" y="{ly}" width="238" height="118" rx="2"/>',
         f'<line {A("c14")} x1="{lx+20}" y1="{ly+36}" x2="{lx+64}" y2="{ly+36}"/>',
         f'<text {A("lbl")} x="{lx+78}" y="{ly+41}">14 · destro</text>',
         f'<line {A("c32")} x1="{lx+20}" y1="{ly+68}" x2="{lx+64}" y2="{ly+68}"/>',
         f'<text {A("lbl")} x="{lx+78}" y="{ly+73}">32 · sinistro</text>',
         f'<text {A("lblS")} x="{lx+20}" y="{ly+100}">Entrambi a sud-ovest</text>']

    return (head(1000, 800, "Pista 14/32: i due circuiti", css)
            + group(k, cx, cy, "".join(g)) + "".join(o) + "</svg>\n")


# ──────────────────────────────────────────────────────────── bozza 3
def draft3():
    k, cx, cy = 0.80, 392.0, 258.0
    css = """
    .band { fill: var(--acc); opacity:.07; stroke:none; }
    .circ { fill:none; stroke: var(--acc); stroke-width:3.6; }
    .arr  { fill: var(--acc); stroke:none; }
    .rwy  { fill: var(--ink); stroke:none; }
    .axis { stroke: var(--base); stroke-width:2; stroke-dasharray:11 10; }
    .road { stroke: var(--mut); fill:none; }
    .big  { font-size:64px; font-weight:700; letter-spacing:.03em;
            fill: var(--ink); text-transform:uppercase; stroke:none; }
    .sub  { font-size:19px; font-weight:400; letter-spacing:.2em;
            fill: var(--mut); text-transform:uppercase; stroke:none; }
    .rule { stroke: var(--acc); stroke-width:2; }
    """
    g = [f'<path {A("band")} opacity=".07" d="{racetrack(W)}"/>',
         motorway(3.4),
         f'<path {A("circ")} d="{racetrack(W)}"/>',
         arrow(-30, W, -1, 0, 15), arrow(150, W, 1, 0, 15),
         runway(solid=True),
         f'<text {A("lblS", halo=True)} x="55" y="{f(YMOT-24)}">'
         f'Autostrada</text>']

    tx = 680
    o = [thresholds(k, cx, cy),
         landmarks(k, cx, cy, 1.1, sub=False),
         north(1332, 100),
         f'<text {A("sub")} x="{tx}" y="238">Aviosuperficie RM24</text>',
         f'<text {A("big")} x="{tx}" y="308">Pista 14 / 32</text>',
         f'<line {A("rule")} x1="{tx}" y1="338" x2="{tx+96}" y2="338"/>',
         f'<text {A("sub")} x="{tx}" y="382">860 m · erba · 551 ft</text>',
         f'<text {A("sub")} x="{tx}" y="414">Circuiti a sud-ovest</text>',
         f'<text {A("sub")} x="{tx}" y="446">14 destro · 32 sinistro</text>',
         scalebar(tx, 516, 500, k)]

    return (head(1400, 640, "Pista 14/32 — schema di apertura", css)
            + group(k, cx, cy, "".join(g)) + "".join(o) + "</svg>\n")


# ─────────────────────────────────────────── bozza 2b: circuito unico
def draft2b():
    """Variante della 2: un solo tracciato tratteggiato percorso nei due sensi.

    Entrambi i circuiti cadono a sud-ovest, quindi condividono il corridoio:
      14 (destro)   sottovento verso NW, base al vertice NW, finale verso la 14
      32 (sinistro) sottovento verso SE, base al vertice SE, finale verso la 32
    Le due basi portano entrambe dal sottovento all'asse pista, cioe verso -y.
    """
    k, cx, cy = 1.0, 500.0, 325.0
    W2 = W * 1.22
    e, r = E + 30, 80.0
    css = """
    .c32 { fill:none; stroke: var(--mut); stroke-width:2.2;
           stroke-dasharray:13 8; }
    .a32 { fill: var(--mut); stroke:none; }
    """
    g = [motorway(),
         f'<path {A("c32")} d="{racetrack(W2, e, r)}"/>',
         # sottovento 32: verso sud-est
         arrow(-30, W2, 1, 0, 10, "a32"), arrow(150, W2, 1, 0, 10, "a32"),
         # sottovento 14: verso nord-ovest, oltre il castello (x = -115)
         arrow(-170, W2, -1, 0, 10, "a32"),
         # basi: dal sottovento verso l'asse pista, a meta del tratto dritto
         arrow(-e, W2 / 2, 0, -1, 10, "a32"),   # base 14 -> finale per la 14
         arrow(e, W2 / 2, 0, -1, 10, "a32"),    # base 32 -> finale per la 32
         runway(),
         f'<text {A("lblS", halo=True)} x="205" y="{f(YMOT-26)}">'
         f'Autostrada</text>']

    o = [thresholds(k, cx, cy),
         landmarks(k, cx, cy),
         north(934, 700), scalebar(60, 762, 500, k)]

    return (head(1000, 800, "Pista 14/32: il circuito nei due sensi", css)
            + group(k, cx, cy, "".join(g)) + "".join(o) + "</svg>\n")


OUT.mkdir(parents=True, exist_ok=True)
for name, fn in (("schema-1-tecnico", draft1),
                 ("schema-2-circuiti", draft2),
                 ("schema-3-banner", draft3),
                 ("schema-2b-circuito-unico", draft2b)):
    p = OUT / f"{name}.svg"
    p.write_text(fn(), encoding="utf-8")
    print(f"{p.name}  {p.stat().st_size} byte")
