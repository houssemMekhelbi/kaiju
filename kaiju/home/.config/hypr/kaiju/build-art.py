#!/usr/bin/env python3
"""Generate the Kaiju art: everything that is an image rather than CSS.

  ~/.config/hypr/kaiju/wallpaper.svg, wallpaper.png   1920x1080: a long back with dorsal plates
        surfacing, lit from behind by the magma, over broken ground slabs with magma in the seams
  ~/.config/hypr/kaiju/lock-field.png                 440x52 terraced plane with the ash to stone frame
  ~/.config/hypr/kaiju/lock-plates.png                three lit plates under the lock saying
  ~/.config/waybar/kaiju/{l,c,r}-{start,end}.png       ends of the three bar plates, 36px high: the
        12/6 terrace (top-left of the left plate, bottom-right of the right plate) and 8px sawtooth teeth
        where the plates face each other
  ~/.config/waybar/kaiju/ws-*.png                      18x18 workspace plates (triangles), five states
  ~/.config/gtk-3.0/kaiju/crumb-chevron.png            Thunar path separator
  ~/.config/gtk-3.0/kaiju/frame.png, frame-focus.png   9-slice terraced frames (menus, tooltips)
  ~/.config/swaync/kaiju/frame-{low,normal,critical}.png  9-slice terraced notification cards

Deterministic; edit and re-run (needs rsvg-convert):  python3 build-art.py
"""

import math
import random
import subprocess
from pathlib import Path

CONF = Path.home() / ".config"
HYPR = CONF / "hypr/kaiju"
BAR = CONF / "waybar/kaiju"
GTK = CONF / "gtk-3.0/kaiju"
NOTI = CONF / "swaync/kaiju"

GROUND, SLAG, RAISED, HAIR, OCHRE = "#0C0B0A", "#161311", "#221C18", "#3A2E26", "#A89070"
MAGMA, EMBER, SPINE, BLAZE = "#FF8A3D", "#9E3B14", "#5FB8FF", "#FF3B3B"
EDGE_HI, EDGE_LO = "#CFC6B4", "#5A4E44"    # accent choice E: edges are ash to stone, the light behind is Magma
BAR_FILL = "rgba(22,19,17,0.78)"
W, H = 1920, 1080


def render(svg, out, w=None, h=None):
    src = out.with_suffix(".svg")
    src.write_text(svg)
    cmd = ["rsvg-convert", "-o", str(out)]
    if w:
        cmd += ["-w", str(w), "-h", str(h)]
    subprocess.run(cmd + [str(src)], check=True)
    if out.name != "wallpaper.png":
        src.unlink()


def path(pts, close=True):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")


# ---- wallpaper -------------------------------------------------------------------
def wallpaper():
    random.seed(3)
    plates, seams = [], []
    # ground: three broken slabs, each edge an irregular terrace (long runs, small risers up and down)
    def slab_edge(y_l, y_r, seed):
        rnd = random.Random(seed)
        x, y, pts = -20.0, float(y_l), [(-20.0, float(y_l))]
        while x < W + 20:
            run = rnd.uniform(120, 420)
            x = min(x + run, W + 20)
            pts.append((x, y))
            target = y_l + (y_r - y_l) * (x / W)
            y2 = target + rnd.choice([-1, 1]) * rnd.choice([6, 12, 12, 18])
            if x < W + 20:
                pts.append((x, y2)); y = y2
        return pts
    for k, (y_l, y_r, fill) in enumerate([(905, 850, "#100E0C"), (965, 930, "#141210"), (1030, 1000, "#181513")]):
        edge = slab_edge(y_l, y_r, 20 + k)
        plates.append(f'<path d="{path(edge + [(W + 20, H + 20), (-20, H + 20)])}" fill="{fill}"/>')
        seams.append(path(edge, close=False))
    seam_glow = "".join(f'<path d="{d}" fill="none" stroke="{MAGMA}" stroke-width="6" opacity="0.40" filter="url(#heat)"/>' for d in seams)
    seam_line = "".join(f'<path d="{d}" fill="none" stroke="url(#seam)" stroke-width="1.3"/>' for d in seams)

    # the back: one long hump; the dorsal plates stand in it, all leaning the same way
    def hump(t):
        x = 760 + t * 1240
        y = 905 - 400 * math.sin(min(1.0, t * 1.05) * math.pi * 0.56) ** 0.9
        return x, y
    ridge = []
    n = 11
    for i in range(n):
        t = 0.10 + 0.74 * i / (n - 1)
        x, y = hump(t)
        size = 46 + 210 * math.sin(math.pi * (i + 0.6) / (n + 0.2)) ** 1.5
        ridge.append((x, y + 14, size, 14))
    def plate_poly(x, y, s, lean):
        a = math.radians(lean)
        b = s * 0.50
        # a dorsal plate: steep leading edge, notched trailing edge
        pts = [(-b * 0.50, 0), (-b * 0.30, -s * 0.50), (-b * 0.02, -s), (b * 0.20, -s * 0.70), (b * 0.12, -s * 0.62),
               (b * 0.40, -s * 0.34), (b * 0.32, -s * 0.28), (b * 0.56, 0)]
        return [(x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)) for px, py in pts]
    fmt = lambda pts: " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    glow = "".join(f'<polygon points="{fmt(plate_poly(x, y, s * 1.05, l))}" fill="{MAGMA}"/>' for x, y, s, l in ridge)
    body = ""
    for x, y, s, l in ridge:
        pts = plate_poly(x, y, s, l)
        body += f'<polygon points="{fmt(pts)}" fill="#0A0908"/>'
        body += f'<polyline points="{fmt(pts[:3])}" fill="none" stroke="url(#edge)" stroke-width="1.5"/>'
    back = [hump(t / 60) for t in range(61)]
    back_d = path([(back[0][0], H + 40)] + back + [(W + 40, back[-1][1]), (W + 40, H + 40)])
    rim_d = path(back, close=False)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
    <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A0908"/><stop offset="0.7" stop-color="#0F0D0B"/><stop offset="1" stop-color="#1A120D"/></linearGradient>
    <linearGradient id="seam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{EMBER}" stop-opacity="0.35"/><stop offset="0.55" stop-color="{MAGMA}"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0.6"/></linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{EDGE_HI}"/><stop offset="0.5" stop-color="{EDGE_LO}"/><stop offset="1" stop-color="{EDGE_LO}" stop-opacity="0.25"/></linearGradient>
    <radialGradient id="charge" gradientUnits="userSpaceOnUse" cx="1380" cy="560" r="680"><stop offset="0" stop-color="{MAGMA}" stop-opacity="0.30"/><stop offset="0.5" stop-color="{EMBER}" stop-opacity="0.12"/><stop offset="1" stop-color="{EMBER}" stop-opacity="0"/></radialGradient>
    <radialGradient id="warm" gradientUnits="userSpaceOnUse" cx="700" cy="1150" r="900"><stop offset="0" stop-color="{MAGMA}" stop-opacity="0.20"/><stop offset="1" stop-color="{MAGMA}" stop-opacity="0"/></radialGradient>
    <filter id="heat" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="9"/></filter>
    <filter id="cold" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="26"/></filter>
    <filter id="smoke" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.003 0.008" numOctaves="4" seed="12"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 0.54  0 0 0 0 0.24  0 0 0 0.8 -0.34"/></filter>
    <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 0.9  0 0 0 0 0.8  0 0 0 0.09 0"/></filter>
    </defs>
    <rect width="{W}" height="{H}" fill="url(#sky)"/>
    <rect width="{W}" height="{H}" filter="url(#smoke)" opacity="0.16"/>
    <path d="M0,{H} L{W * 0.47:.0f},0" stroke="{MAGMA}" stroke-opacity="0.05" stroke-width="1"/>
    <path d="M{W},{H * 0.2:.0f} L{W * 0.3:.0f},{H}" stroke="{MAGMA}" stroke-opacity="0.05" stroke-width="1"/>
    <rect width="{W}" height="{H}" fill="url(#charge)"/>
    <g filter="url(#cold)" opacity="0.75">{glow}</g>
    {body}
    <path d="{back_d}" fill="#0A0908"/>
    <path d="{rim_d}" fill="none" stroke="{EDGE_LO}" stroke-opacity="0.8" stroke-width="1.2"/>
    {plates[0]}{plates[1]}{plates[2]}
    <rect width="{W}" height="{H}" fill="url(#warm)"/>
    {seam_glow}{seam_line}
    <rect width="{W}" height="{H}" filter="url(#grain)"/>
    </svg>'''
    render(svg, HYPR / "wallpaper.png", W, H)


# ---- terraced planes ---------------------------------------------------------------
def terrace_pts(w, h, a=12, b=6, tl=True, br=True):
    pts = [(0, a), (b, a), (b, b), (a, b), (a, 0)] if tl else [(0, 0)]
    pts += [(w, 0)]
    pts += [(w, h - a), (w - b, h - a), (w - b, h - b), (w - a, h - b), (w - a, h)] if br else [(w, h)]
    return pts + [(0, h)]


def inset(pts, w, h, d=0.5):
    """pull the outline half a pixel in so a 1px stroke lands on whole pixels"""
    return [(min(max(x, d), w - d), min(max(y, d), h - d)) for x, y in pts]


GRAD = (f'<linearGradient id="fr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{EDGE_HI}"/>'
        f'<stop offset="0.45" stop-color="{EDGE_LO}"/><stop offset="1" stop-color="{EDGE_LO}" stop-opacity="0.3"/></linearGradient>')


def plane_svg(w, h, fill, stroke="url(#fr)", a=12, b=6, tl=True, br=True):
    d = path(inset(terrace_pts(w, h, a, b, tl, br), w, h))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{GRAD}</defs>'
            f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="1"/></svg>')


# ---- bar plates ------------------------------------------------------------------------
def bar_caps():
    h = 36
    top, bottom = f'stroke="{EDGE_HI}" stroke-opacity="0.55"', f'stroke="{EDGE_LO}"'

    def terrace_cap(flip):
        # 12px wide: the two-step cut, top-left; flipped twice it is the bottom-right one
        tr = ' transform="translate(12 36) scale(-1 -1)"' if flip else ""
        fill = path([(0.5, 12), (6, 12), (6, 6), (12, 6), (12, 0), (12, h), (0.5, h)])
        line = path([(0.5, h - 0.5), (0.5, 12.5), (6.5, 12.5), (6.5, 6.5), (12, 6.5)], close=False)
        top_l = path([(12, 0.5), (12.5, 0.5)], close=False)
        a, b = (bottom, top) if flip else (top, bottom)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="12" height="{h}" viewBox="0 0 12 {h}"><g{tr}>'
                # the glow continues into the cut: CSS box-shadow stops at the box, so the cut would read as a dark notch
                f'<path d="M0,0 H12 V{h} H0 Z {fill}" fill-rule="evenodd" fill="{MAGMA}" opacity="0.15"/>'
                f'<path d="{fill}" fill="{BAR_FILL}"/><path d="{line}" fill="none" {a} stroke-width="1"/>'
                f'<path d="M0,{h - 0.5} H12" fill="none" {b} stroke-width="1"/></g></svg>')

    def teeth_cap(right):
        # 8px wide sawtooth: points at 1/8, 3/8, 5/8, 7/8 of the height
        zig = [(0, 0)] + [((8 if k % 2 else 0), h * k / 8) for k in range(1, 8)] + [(0, h)]
        tr = "" if right else ' transform="translate(8 0) scale(-1 1)"'
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="8" height="{h}" viewBox="0 0 8 {h}"><g{tr}>'
                f'<path d="M0,0 H8 V{h} H0 Z {path(zig)}" fill-rule="evenodd" fill="{MAGMA}" opacity="0.15"/>'
                f'<path d="{path(zig)}" fill="{BAR_FILL}"/>'
                f'<path d="{path(zig, close=False)}" fill="none" stroke="{EDGE_LO}" stroke-width="1"/></g></svg>')

    render(terrace_cap(False), BAR / "l-start.png")
    render(teeth_cap(True), BAR / "l-end.png")
    render(teeth_cap(False), BAR / "c-start.png")
    render(teeth_cap(True), BAR / "c-end.png")
    render(teeth_cap(False), BAR / "r-start.png")
    render(terrace_cap(True), BAR / "r-end.png")


def workspace_plates():
    tri = "9,2.5 15.5,15 2.5,15"
    shapes = {
        "empty": f'<polygon points="{tri}" fill="none" stroke="{MAGMA}" stroke-opacity="0.45" stroke-width="1.2"/>',
        "occupied": f'<polygon points="{tri}" fill="{EMBER}"/>',
        "active": f'<polygon points="{tri}" fill="{MAGMA}" opacity="0.5"/>',
        "focused": f'<polygon points="{tri}" fill="{MAGMA}"/><line x1="9" y1="6.5" x2="9" y2="14.5" stroke="{GROUND}" stroke-width="1.4"/>',
        "urgent": f'<polygon points="{tri}" fill="{BLAZE}"/>',
    }
    for name, body in shapes.items():
        render(f'<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18">{body}</svg>', BAR / f"ws-{name}.png")


# ---- lock ----------------------------------------------------------------------------------
def lock_art():
    render(plane_svg(440, 52, "rgba(22,19,17,0.80)"), HYPR / "lock-field.png", 880, 104)
    plates = "".join(f'<polygon points="{x},{60 - s} {x + s * 0.5},60 {x - s * 0.5},60" fill="{GROUND}" stroke="{EDGE_HI}" stroke-opacity="0.8" stroke-width="1.2"/>'
                     for x, s in ((34, 30), (70, 42), (106, 30)))
    glow = "".join(f'<polygon points="{x},{60 - s} {x + s * 0.5},60 {x - s * 0.5},60" fill="{MAGMA}"/>' for x, s in ((34, 30), (70, 42), (106, 30)))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="140" height="80" viewBox="0 0 140 80"><defs><filter id="g" x="-40%" y="-60%" width="180%" height="220%">'
           f'<feGaussianBlur stdDeviation="7"/></filter></defs><g filter="url(#g)" opacity="0.8">{glow}</g>{plates}</svg>')
    render(svg, HYPR / "lock-plates.png", 280, 160)


# ---- GTK and notification frames (9-slice: 16px corners) --------------------------------------
def frames():
    render(f'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="18" viewBox="0 0 10 18">'
           f'<polyline points="3,5 7,9 3,13" fill="none" stroke="{EMBER}" stroke-width="1.4"/></svg>', GTK / "crumb-chevron.png")
    render(plane_svg(48, 48, SLAG, f"{EDGE_HI}30"), GTK / "frame.png")
    render(plane_svg(48, 48, SLAG), GTK / "frame-focus.png")
    render(plane_svg(48, 48, "rgba(22,19,17,0.98)", f"{EDGE_HI}1F"), NOTI / "frame-low.png")
    render(plane_svg(48, 48, "rgba(22,19,17,0.98)", f"{EDGE_HI}30"), NOTI / "frame-normal.png")
    render(plane_svg(48, 48, "rgba(22,19,17,0.98)"), NOTI / "frame-critical.png")


if __name__ == "__main__":
    for d in (HYPR, BAR, GTK, NOTI):
        d.mkdir(parents=True, exist_ok=True)
    wallpaper()
    bar_caps()
    workspace_plates()
    lock_art()
    frames()
    print("Kaiju art written")
