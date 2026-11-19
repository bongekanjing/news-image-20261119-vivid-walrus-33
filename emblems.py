"""Thirteen flat emblems, one drawing grammar for the whole page.

Every emblem fills its own box: a tinted ground, three or four flat shapes in
near-neighbour tones, one accent, and thin dark outlines. No photograph, no
gradient, no text except the short reversed tag the layout passes in. They are
mnemonics and diagrams, not reportage.

All coordinates are fractions of the emblem box, so the same function works at
lead size and at card size.
"""
import math

from art import Art

INK = (26, 23, 20)
WHITE = (250, 248, 243)


def _mix(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _dark(col, k=0.55):
    return tuple(int(c * k) for c in col)


def _pale(col, k=0.86):
    return _mix(col, WHITE, k)


# ---------------------------------------------------------------- emblems ----

def gulf(a, tag=None):
    """A Gulf chart: land, water, a chokepoint, drone arcs, bursts."""
    a.box(_pale((176, 126, 26), 0.80))
    water = (150, 183, 196)
    a.rect(0, 0.34, 1, 0.66, water)
    land = _pale((176, 126, 26), 0.42)
    a.poly([(0, 0.34), (0.20, 0.28), (0.40, 0.36), (0.44, 0.52), (0.30, 0.58), (0, 0.54)], land)
    a.poly([(1, 0.10), (0.72, 0.16), (0.60, 0.32), (0.66, 0.48), (0.80, 0.44), (1, 0.52)], land)
    a.poly([(0.46, 0.70), (0.66, 0.62), (0.74, 0.74), (0.62, 0.86), (0.48, 0.84)], land)
    # chokepoint
    a.line([(0.50, 0.30), (0.56, 0.56)], _dark((176, 126, 26), 0.5), 1.4)
    # drone arcs and interceptions, all launched from the eastern landfall
    for x1, y1 in [(0.22, 0.40), (0.28, 0.54), (0.20, 0.26)]:
        a.line([(0.60, 0.32), ((0.60 + x1) / 2, min(0.32, y1) - 0.10), (x1, y1)],
               (163, 34, 34), 1.2)
    for x, y in [(0.22, 0.40), (0.28, 0.54), (0.20, 0.26)]:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7)]:
            a.line([(x, y), (x + dx * 0.035, y + dy * 0.035)], (163, 34, 34), 0.9)
    # ship
    a.poly([(0.62, 0.74), (0.72, 0.74), (0.70, 0.80), (0.64, 0.80)], _dark(water, 0.45))


def _star(a, cx, cy, r, col, pts=5):
    """A five-pointed star, drawn as a polygon, in box fractions."""
    seq = []
    for i in range(pts * 2):
        ang = -math.pi / 2 + i * math.pi / pts
        rr = r if i % 2 == 0 else r * 0.382
        seq.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    a.poly(seq, col)


def _star(a, cx, cy, r, col, pts=5):
    """A five-pointed star, drawn as a polygon, in box fractions."""
    seq = []
    for i in range(pts * 2):
        ang = -math.pi / 2 + i * math.pi / pts
        rr = r if i % 2 == 0 else r * 0.382
        seq.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    a.poly(seq, col)


def _star(a, cx, cy, r, col, pts=5):
    """A five-pointed star, drawn as a polygon, in box fractions."""
    seq = []
    for i in range(pts * 2):
        ang = -math.pi / 2 + i * math.pi / pts
        rr = r if i % 2 == 0 else r * 0.382
        seq.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    a.poly(seq, col)


def summit(a, tag=None):
    """A summit photo-op: China, Russia and the United States over a mic table.

    Flags rather than faces: a national flag is exact and legible at any size,
    which is what this picture has to survive at 300 pixels across.
    """
    ground = (32, 84, 114)
    RED = (198, 40, 40)
    a.box(_pale(ground, 0.84))
    # briefing-room wall: a pale field with a low dado
    a.rect(0.0, 0.0, 1.0, 0.665, _pale(ground, 0.72))
    a.rect(0.0, 0.665, 1.0, 0.335, _dark(ground, 0.60))

    wf = 0.250
    hf = wf * ((a.w / a.h) if a.h else 1.0) * (2.0 / 3.0)
    xs = [0.078, 0.375, 0.672]
    top = 0.235
    # poles: from above the flag down to the table top, then stop
    for fx in xs:
        a.line([(fx + wf * 0.5, top - 0.040), (fx + wf * 0.5, 0.772)],
               _dark(ground, 0.42), 1.7)

    # left: China
    fx = xs[0]
    a.rect(fx, top, wf, hf, RED)
    _star(a, fx + wf * 0.17, top + hf * 0.28, hf * 0.150, (252, 214, 60))
    for sx, sy in [(0.325, 0.085), (0.395, 0.195), (0.395, 0.355), (0.325, 0.465)]:
        _star(a, fx + wf * sx, top + hf * sy, hf * 0.052, (252, 214, 60))

    # centre: Russia
    fx = xs[1]
    a.rect(fx, top, wf, hf / 3.0, (246, 244, 240))
    a.rect(fx, top + hf / 3.0, wf, hf / 3.0, (44, 74, 148))
    a.rect(fx, top + 2 * hf / 3.0, wf, hf / 3.0, (192, 44, 44))

    # right: United States
    fx = xs[2]
    for i in range(13):
        a.rect(fx, top + i * hf / 13.0, wf, hf / 13.0,
               (198, 42, 46) if i % 2 == 0 else (246, 244, 240))
    a.rect(fx, top, wf * 0.42, hf * (7.0 / 13.0), (38, 56, 118))
    for row in range(9):
        ncol = 6 if row % 2 == 0 else 5
        for col in range(ncol):
            sx = fx + wf * (0.045 + col * (0.036 if ncol == 6 else 0.041)
                            + (0.0 if ncol == 6 else 0.018))
            sy = top + hf * (0.045 + row * 0.0525)
            _star(a, sx, sy, hf * 0.019, (246, 244, 240))

    # the table: a top surface in perspective, a lit front edge, then the apron
    a.poly([(0.0, 0.762), (1.0, 0.762), (1.0, 0.800), (0.0, 0.800)], _pale(ground, 0.55))
    a.poly([(0.0, 0.800), (1.0, 0.800), (1.0, 0.816), (0.0, 0.816)], _pale(ground, 0.74))
    a.poly([(0.0, 0.816), (1.0, 0.816), (1.0, 0.935), (0.0, 0.935)], _dark(ground, 0.58))
    a.poly([(0.0, 0.935), (1.0, 0.935), (1.0, 1.0), (0.0, 1.0)], _dark(ground, 0.44))

    # four larger microphones, standing on the table top, with bases
    for mx, lean in [(0.395, -0.030), (0.470, -0.010), (0.545, 0.010), (0.620, 0.030)]:
        a.rect(mx - 0.030, 0.788, 0.060, 0.013, _dark(ground, 0.30))
        a.line([(mx, 0.790), (mx + lean, 0.720)], _dark(ground, 0.22), 1.4)
        a.circle(mx + lean, 0.712, 0.019, _dark(ground, 0.14))
        a.circle(mx + lean - 0.005, 0.707, 0.007, _pale(ground, 0.60))
    # nameplates on the top surface
    a.rect(0.245, 0.770, 0.075, 0.026, (246, 244, 240))
    a.rect(0.690, 0.770, 0.075, 0.026, (246, 244, 240))


def strike(a, tag=None):
    """A night skyline under fire, a crescent moon."""
    sky = _mix((40, 38, 52), (36, 92, 122), 0.20)
    a.box(sky)
    a.circle(0.80, 0.22, 0.075, _pale((196, 186, 150), 0.55))
    a.circle(0.845, 0.20, 0.070, sky)
    # skyline
    blocks = [(0.02, 0.52, 0.10, 0.48), (0.13, 0.42, 0.09, 0.58), (0.23, 0.58, 0.12, 0.42),
              (0.36, 0.46, 0.08, 0.54), (0.45, 0.60, 0.13, 0.40), (0.59, 0.40, 0.09, 0.60),
              (0.69, 0.56, 0.10, 0.44), (0.80, 0.48, 0.08, 0.52), (0.89, 0.60, 0.11, 0.40)]
    for x, y, w, h in blocks:
        a.rect(x, y, w, h, _mix(sky, INK, 0.55))
    # bursts
    for cx, cy, r in [(0.30, 0.34, 0.055), (0.66, 0.28, 0.045)]:
        a.circle(cx, cy, r, (206, 92, 44))
        a.circle(cx, cy, r * 0.5, (240, 186, 96))
    # drone trails
    for x0, y0 in [(0.10, 0.14), (0.46, 0.10)]:
        a.line([(x0, y0), (0.30, 0.30)], (200, 120, 60), 0.9)


def ipo(a, tag=None):
    """A rising bar chart and a ticker line."""
    a.box(_pale((46, 74, 126), 0.84))
    base = 0.86
    heights = [0.22, 0.34, 0.30, 0.46, 0.58, 0.74]
    for i, hh in enumerate(heights):
        x = 0.10 + i * 0.135
        a.rect(x, base - hh, 0.085, hh, _mix((46, 74, 126), WHITE, 0.15 + i * 0.09))
    a.line([(0.08, base), (0.92, base)], _dark((46, 74, 126), 0.5), 1.2)
    # trend line
    pts = [(0.145 + i * 0.135, base - h - 0.06) for i, h in enumerate(heights)]
    a.line(pts, (163, 34, 34), 1.5)


def fed(a, tag=None):
    """A central-bank portico and a rate arrow."""
    a.box(_pale((92, 88, 84), 0.86))
    a.poly([(0.5, 0.10), (0.94, 0.32), (0.06, 0.32)], _mix((92, 88, 84), WHITE, 0.25))
    for i in range(6):
        x = 0.10 + i * 0.155
        a.rect(x, 0.34, 0.075, 0.40, _mix((92, 88, 84), WHITE, 0.35))
    a.rect(0.06, 0.76, 0.88, 0.055, _mix((92, 88, 84), WHITE, 0.18))
    a.line([(0.62, 0.72), (0.86, 0.50)], (163, 34, 34), 1.5)
    a.poly([(0.86, 0.44), (0.90, 0.58), (0.77, 0.56)], (163, 34, 34))


def space(a, tag=None):
    """A star field, the Sun, a probe, and Earth as a speck."""
    a.box((18, 22, 40))
    stars = [(0.08, 0.20), (0.17, 0.62), (0.24, 0.14), (0.33, 0.78), (0.41, 0.26),
             (0.49, 0.58), (0.57, 0.12), (0.63, 0.84), (0.72, 0.34), (0.79, 0.68),
             (0.86, 0.18), (0.93, 0.52), (0.12, 0.86), (0.90, 0.90), (0.55, 0.42)]
    for x, y in stars:
        a.circle(x, y, 0.008, (206, 210, 226))
    a.circle(0.06, 0.44, 0.075, (222, 176, 84))
    # probe
    a.rect(0.46, 0.42, 0.05, 0.10, (198, 200, 210))
    a.rect(0.40, 0.44, 0.06, 0.05, (150, 156, 176))
    a.rect(0.51, 0.44, 0.06, 0.05, (150, 156, 176))
    a.line([(0.485, 0.42), (0.485, 0.32)], (198, 200, 210), 0.8)
    # distance line to Earth
    a.line([(0.14, 0.44), (0.85, 0.44)], (120, 140, 190), 0.7)
    a.circle(0.87, 0.44, 0.028, (120, 168, 210))


def caracas(a, tag=None):
    """Two flags and a handshake."""
    a.box(_pale((46, 74, 126), 0.80))
    for fx, cols in [(0.16, [(196, 168, 40), (36, 62, 120), (176, 40, 34)]),
                     (0.68, [(196, 168, 40), (36, 62, 120), (176, 40, 34)])]:
        for i, c in enumerate(cols):
            a.rect(fx, 0.14 + i * 0.075, 0.16, 0.075, c)
        a.line([(fx, 0.14), (fx, 0.62)], _dark((46, 74, 126), 0.55), 1.2)
    a.line([(0.36, 0.60), (0.64, 0.60)], _dark((46, 74, 126), 0.45), 1.8)
    a.circle(0.50, 0.60, 0.045, _dark((46, 74, 126), 0.35))


def cop(a, tag=None):
    """A globe, two stacks, and a draft with a crossed line."""
    a.box(_pale((32, 112, 96), 0.84))
    a.circle(0.28, 0.48, 0.185, (108, 168, 150))
    a.arc(0.28, 0.48, 0.185, 0, 360, _dark((32, 112, 96), 0.55), 0.9)
    a.arc(0.28, 0.48, 0.09, 0, 360, _dark((32, 112, 96), 0.4), 0.8)
    a.line([(0.10, 0.48), (0.46, 0.48)], _dark((32, 112, 96), 0.4), 0.8)
    # stacks
    for x in (0.62, 0.76):
        a.rect(x, 0.44, 0.055, 0.40, _dark((32, 112, 96), 0.45))
        a.poly([(x - 0.02, 0.44), (x + 0.075, 0.44), (x + 0.045, 0.34), (x + 0.012, 0.34)],
               _dark((32, 112, 96), 0.5))
    a.circle(0.66, 0.24, 0.035, (188, 196, 198))
    a.circle(0.79, 0.20, 0.028, (188, 196, 198))
    # document
    a.rect(0.86, 0.52, 0.11, 0.30, WHITE)
    a.line([(0.878, 0.60), (0.955, 0.60)], (163, 34, 34), 0.9)
    a.line([(0.878, 0.66), (0.955, 0.66)], (163, 34, 34), 0.9)


def border(a, tag=None):
    """A border post, a barrier, and two columns of troops."""
    a.box(_pale((176, 126, 26), 0.78))
    a.rect(0, 0.90, 1, 0.10, _mix((176, 126, 26), INK, 0.45))
    # border line
    a.line([(0.50, 0.06), (0.50, 0.90)], (163, 34, 34), 1.4)
    # barrier
    for y in (0.30, 0.40):
        a.rect(0.44, y, 0.12, 0.045, (206, 202, 192))
    a.line([(0.44, 0.16), (0.44, 0.52)], _mix((176, 126, 26), INK, 0.5), 1.6)
    # troops
    for side, x0 in [(-1, 0.30), (1, 0.60)]:
        for i in range(3):
            cx = x0 + i * 0.055
            a.circle(cx, 0.56, 0.030, _mix((176, 126, 26), INK, 0.62))
            a.rect(cx - 0.020, 0.60, 0.040, 0.16, _mix((176, 126, 26), INK, 0.55))
    a.rect(0.66, 0.34, 0.30, 0.10, _mix((176, 126, 26), INK, 0.30))
    a.rect(0.72, 0.44, 0.18, 0.08, _mix((176, 126, 26), INK, 0.22))


def gavel(a, tag=None):
    """A gavel over a page: a court's order."""
    a.box(_pale((116, 92, 40), 0.82))
    a.rect(0.14, 0.20, 0.44, 0.62, WHITE)
    for i in range(5):
        a.line([(0.19, 0.30 + i * 0.095), (0.53, 0.30 + i * 0.095)],
               (176, 170, 160) if i else (163, 34, 34), 0.7)
    # gavel
    a.poly([(0.52, 0.62), (0.86, 0.28), (0.92, 0.36), (0.58, 0.70)], _mix((116, 92, 40), INK, 0.58))
    a.poly([(0.82, 0.22), (0.94, 0.30), (0.90, 0.42), (0.78, 0.34)], _mix((116, 92, 40), INK, 0.7))
    a.rect(0.44, 0.82, 0.34, 0.045, _mix((116, 92, 40), INK, 0.65))


def chart(a, tag=None):
    """A fiscal chart: balance bars and a target line."""
    a.box(_pale((52, 78, 128), 0.84))
    base = 0.72
    vals = [0.16, 0.26, 0.20, 0.34, 0.30, 0.42, 0.50]
    for i, v in enumerate(vals):
        x = 0.10 + i * 0.115
        a.rect(x, base - v, 0.070, v, _mix((52, 78, 128), WHITE, 0.20 + i * 0.06))
    a.line([(0.08, base), (0.92, base)], _dark((52, 78, 128), 0.45), 1.1)
    a.line([(0.08, 0.30), (0.92, 0.30)], (163, 34, 34), 1.1)
    a.circle(0.88, 0.30, 0.022, (163, 34, 34))


def rally(a, tag=None):
    """A ticker board: an index line climbing across a grid of quotes."""
    a.box(_pale((38, 66, 116), 0.82))
    grid = _mix((38, 66, 116), WHITE, 0.30)
    for i in range(1, 6):
        a.line([(0.0, i / 6.0), (1.0, i / 6.0)], grid, 0.6)
    for i in range(1, 8):
        a.line([(i / 8.0, 0.0), (i / 8.0, 1.0)], grid, 0.6)
    pts = [(0.06, 0.82), (0.20, 0.70), (0.32, 0.76), (0.46, 0.52),
           (0.58, 0.58), (0.72, 0.34), (0.86, 0.40), (0.95, 0.22)]
    a.line(pts, (170, 36, 36), 2.0)
    a.circle(0.95, 0.22, 0.028, (170, 36, 36))
    a.circle(0.06, 0.82, 0.020, WHITE)


def ledger(a, tag=None):
    """A vote tally: a wide block of ayes against a sliver of nays. 69 to 2."""
    a.box(_pale((60, 84, 60), 0.80))
    # the floor of the chamber: a wide green slab, then a narrow bar
    a.rect(0.055, 0.20, 0.66, 0.52, (72, 118, 72))
    a.rect(0.775, 0.20, 0.062, 0.52, (150, 44, 44))
    # seat rows scored across each block
    for i in range(5):
        y = 0.26 + i * 0.092
        a.rect(0.085, y, 0.60, 0.020, _mix((72, 118, 72), WHITE, 0.34))
        if i < 2:
            a.rect(0.780, y, 0.052, 0.020, _mix((150, 44, 44), WHITE, 0.30))
    # a heavy baseline and the result tick
    a.rect(0.055, 0.760, 0.782, 0.030, _dark((60, 84, 60), 0.42))
    a.rect(0.055, 0.128, 0.66, 0.026, (150, 44, 44))


def cyclone(a, tag=None):
    """A storm spiral over a coast."""
    sea = _mix((150, 183, 196), (32, 112, 96), 0.18)
    a.box(sea)
    a.rect(0, 0.72, 1, 0.28, _pale((116, 92, 40), 0.45))
    for r, w in [(0.30, 2.0), (0.22, 1.8), (0.14, 1.6), (0.07, 1.4)]:
        a.arc(0.44, 0.44, r, r * 900 % 360, r * 900 % 360 + 250, WHITE, w)
    a.circle(0.44, 0.44, 0.028, WHITE)
    for cx, cy in [(0.76, 0.24), (0.86, 0.40)]:
        a.circle(cx, cy, 0.030, (163, 34, 34))


def ballot(a, tag=None):
    """Seat tally: a grid of squares, a broken run of one colour."""
    a.box(_pale((46, 74, 126), 0.86))
    cols, rows = 10, 5
    for r in range(rows):
        for c in range(cols):
            x = 0.10 + c * 0.082
            y = 0.14 + r * 0.115
            dem = (c + r * cols) < 28
            a.rect(x, y, 0.052, 0.078, _mix((46, 74, 126), WHITE, 0.45) if dem else (188, 132, 132))
    a.rect(0.10, 0.72, 0.052, 0.078, _mix((46, 74, 126), WHITE, 0.45))
    a.rect(0.17, 0.72, 0.052, 0.078, (163, 34, 34))


def network(a, tag=None):
    """Server racks and a severed link."""
    a.box(_pale((92, 88, 84), 0.84))
    for i in range(3):
        y = 0.16 + i * 0.24
        a.rect(0.10, y, 0.34, 0.18, _mix((92, 88, 84), INK, 0.30))
        for j in range(3):
            a.circle(0.14 + j * 0.038, y + 0.045, 0.010, (150, 196, 150) if j < 2 else (200, 120, 100))
    # severed cable
    a.line([(0.46, 0.44), (0.62, 0.44)], (163, 34, 34), 1.6)
    a.line([(0.68, 0.38), (0.72, 0.50)], (163, 34, 34), 1.6)
    a.line([(0.72, 0.38), (0.68, 0.50)], (163, 34, 34), 1.6)
    a.circle(0.84, 0.44, 0.055, _mix((92, 88, 84), INK, 0.45))
    a.arc(0.84, 0.44, 0.085, 200, 340, (163, 34, 34), 1.0)


def settler(a, tag=None):
    """Houses behind a barrier wall."""
    a.box(_pale((176, 126, 26), 0.80))
    a.rect(0, 0.82, 1, 0.18, _mix((176, 126, 26), INK, 0.40))
    for x, w in [(0.10, 0.20), (0.36, 0.20), (0.62, 0.24)]:
        a.rect(x, 0.40, w, 0.40, _mix((176, 126, 26), INK, 0.28))
        a.poly([(x - 0.02, 0.40), (x + w + 0.02, 0.40), (x + w / 2, 0.22)],
               _mix((176, 126, 26), INK, 0.45))
        for j in range(2):
            a.rect(x + 0.03 + j * 0.09, 0.52, 0.05, 0.07, (222, 214, 198))
    # wall
    a.rect(0, 0.74, 1, 0.10, _mix((176, 126, 26), INK, 0.62))
    for i in range(9):
        a.line([(0.05 + i * 0.11, 0.74), (0.05 + i * 0.11, 0.84)], PAPER_GREY, 0.6)


def flags(a, tag=None):
    """Two flags on poles and a handshake under them."""
    a.box(_pale((36, 92, 122), 0.80))
    for fx, bands in [(0.14, [(196, 40, 52), (250, 248, 243), (40, 62, 130)]),
                      (0.66, [(40, 62, 130), (250, 248, 243), (196, 40, 52)])]:
        a.line([(fx, 0.14), (fx, 0.66)], _dark((36, 92, 122), 0.58), 1.3)
        for i, c in enumerate(bands):
            a.rect(fx, 0.16 + i * 0.10, 0.20, 0.10, c)
    a.circle(0.50, 0.70, 0.055, _dark((36, 92, 122), 0.45))
    a.poly([(0.44, 0.70), (0.50, 0.62), (0.56, 0.70), (0.50, 0.78)], _dark((36, 92, 122), 0.30))
    a.line([(0.34, 0.78), (0.66, 0.78)], _dark((36, 92, 122), 0.5), 1.4)


def ocean(a, tag=None):
    """A reef ring and a protected-zone boundary."""
    a.box((150, 197, 200))
    a.rect(0, 0.60, 1, 0.40, (108, 168, 178))
    # sanctuary boundary
    a.arc(0.50, 0.56, 0.34, 0, 360, (250, 248, 243), 1.2)
    # reef
    a.poly([(0.30, 0.68), (0.42, 0.56), (0.56, 0.60), (0.64, 0.72), (0.46, 0.78)],
           (86, 148, 120))
    a.circle(0.44, 0.64, 0.030, (188, 214, 176))
    # fish
    a.poly([(0.70, 0.40), (0.78, 0.36), (0.78, 0.44)], (60, 104, 116))
    a.poly([(0.66, 0.40), (0.72, 0.36), (0.72, 0.44)], (60, 104, 116))
    # guardian ring
    a.arc(0.50, 0.56, 0.40, 200, 340, (32, 112, 96), 1.0)


PAPER_GREY = (170, 162, 150)
WHITE = WHITE  # re-exported for builders

EMBLEMS = {
    "gulf": gulf, "summit": summit, "strike": strike, "ipo": ipo, "fed": fed,
    "space": space, "caracas": caracas, "cop": cop, "border": border,
    "gavel": gavel, "chart": chart, "cyclone": cyclone, "ballot": ballot,
    "network": network, "settler": settler, "flags": flags, "ocean": ocean,
    "rally": rally, "ledger": ledger,
}


def draw(page, name, x, y, w, h, accent, tag=None):
    fn = EMBLEMS.get(name)
    if fn is None:
        page.rect(x, y, w, h, _pale(accent, 0.86))
        return
    a = Art(page, x, y, w, h, accent)
    fn(a, tag)
    if tag:
        a.chip(tag)
