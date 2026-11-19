import sys
# かざんの ぬし しんの すがた（背中に 火山が 5つ生えた 岩と ようがんの 竜・左向きの 横すがた）
# 5の段の ひみつの かず＝背中の 火山 5つ（ふん火口と ほのお 5つ）。ほかのパーツは5にしない
#   角2本・頭のうしろのトゲ3本・つめ3本ずつ・しっぽのトゲ4本・きば4本
L = '#2b2b3a'
def hl(d, w=2.4, op=.7): return f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'
def lava(d, w=3, cls='glow'):
    return (f'<path d="{d}" fill="none" stroke="#ff7a2a" stroke-width="{w+5}" stroke-linecap="round" stroke-linejoin="round" opacity=".5" filter="url(#soft)" class="{cls}"/>'
            f'<path d="{d}" fill="none" stroke="#ffb03a" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" class="{cls}"/>')
def shape(d, fill, w=3.2): return f'<path d="{d}" fill="{fill}" stroke="{L}" stroke-width="{w}" stroke-linejoin="round"/>'
def claws(pts, ln=18, w=5):
    # pts: (x, y, 向き) 向き 1=下へ、まがりは 左（前）へ
    s = ''
    for x, y in pts:
        s += f'<path d="M{x-w} {y} Q{x-w-2} {y+ln*.7} {x-w-6} {y+ln} Q{x+2} {y+ln*.6} {x+w} {y} Z" fill="#f2e6c8" stroke="{L}" stroke-width="2.2" stroke-linejoin="round"/>'
    return s

# ---- 背中の 火山 5つ（背びれのように ならぶ。まん中が いちばん高い）----
# (底の中心x, 底y, 火口x, 火口y, おくれ)
# 最後の数＝高さの わりあい（まん中3本は 2/3）
volc = [(372, 224, 394, 164, 'd3', 1), (346, 196, 372, 72, 'd2', 2/3), (310, 180, 332, 30, 'd0', 2/3),
        (270, 168, 284, 42, 'd1', 2/3), (232, 150, 240, 84, 'd2', 1)]
def make_volcs(top):
    # 背中から 生えるように：すそを 広げて 体に なじませ、下に いくほど 体の色に とけこむ
    def ty(x):
        for (x1, y1), (x2, y2) in zip(top, top[1:]):
            if x1 <= x <= x2: return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
        return top[-1][1] if x > top[-1][0] else top[0][1]
    out = ''
    for i, (bx, _, cx, cy, dl, k) in enumerate(volc):
        yb = ty(bx)
        cy = round(yb - (yb - cy) * k); cx = round(bx + (cx - bx) * k)
        lx, rx = max(bx - 46, 212), min(bx + 42, 376)
        lf = (lx, ty(lx) + 10); rf = (rx, ty(rx) + 10)
        ml = (cx - 11 + (bx - 22 - (cx - 11)) * .72, cy + (yb - cy) * .72)
        mr = (cx + 11 + (bx + 20 - (cx + 11)) * .72, cy + (yb - cy) * .72)
        y2 = max(lf[1], rf[1], yb + 10)
        out += (f'<defs><linearGradient id="vg{i}" gradientUnits="userSpaceOnUse" x1="0" y1="{cy}" x2="0" y2="{y2:.0f}">'
                f'<stop offset="0" stop-color="#7a6560"/><stop offset=".55" stop-color="#5a3e3a"/>'
                f'<stop offset=".86" stop-color="#6a3630" stop-opacity=".9"/><stop offset="1" stop-color="#6a3630" stop-opacity="0"/></linearGradient>'
                f'<linearGradient id="vs{i}" gradientUnits="userSpaceOnUse" x1="0" y1="{cy}" x2="0" y2="{y2:.0f}">'
                f'<stop offset="0" stop-color="{L}"/><stop offset=".7" stop-color="{L}"/><stop offset=".9" stop-color="{L}" stop-opacity="0"/></linearGradient></defs>')
        side = (f'M{lf[0]:.0f} {lf[1]:.0f} Q{bx-20} {yb-6:.0f} {ml[0]:.0f} {ml[1]:.0f} L{cx-11} {cy} L{cx+11} {cy} '
                f'L{mr[0]:.0f} {mr[1]:.0f} Q{bx+18} {yb-6:.0f} {rf[0]:.0f} {rf[1]:.0f}')
        out += f'<path d="{side} L{rf[0]:.0f} {y2+20:.0f} L{lf[0]:.0f} {y2+20:.0f} Z" fill="url(#vg{i})"/>'
        out += f'<path d="{side}" fill="none" stroke="url(#vs{i})" stroke-width="3.2" stroke-linejoin="round"/>'
        out += hl(f'M{cx-8} {cy+8} L{(cx+ml[0])/2:.0f} {(cy+ml[1])/2:.0f}', 2.6, .25)
        out += lava(f'M{cx-4} {cy+3} L{cx-8} {cy+(yb-cy)*.35:.0f} L{cx-2} {cy+(yb-cy)*.6:.0f} L{cx-10+(bx-cx)*.9:.0f} {yb+10:.0f} '
                    f'M{cx+6} {cy+3} L{cx+9} {cy+(yb-cy)*.3:.0f}', 3, f'glow {dl}')
        out += f'<ellipse cx="{cx}" cy="{cy}" rx="13" ry="4.5" fill="#ff7a2a" stroke="{L}" stroke-width="2.4"/>'
        out += (f'<g class="flick {dl}"><path d="M{cx-11} {cy-1} C{cx-16} {cy-22} {cx-4} {cy-28} {cx} {cy-46} '
                f'C{cx+6} {cy-28} {cx+16} {cy-22} {cx+11} {cy-1} Z" fill="url(#fl5)" stroke="{L}" stroke-width="2.4" stroke-linejoin="round"/>'
                f'<path d="M{cx-4} {cy-2} C{cx-6} {cy-12} {cx} {cy-16} {cx} {cy-24} C{cx+3} {cy-16} {cx+6} {cy-12} {cx+4} {cy-2} Z" fill="#fff6c0"/></g>')
        out += f'<g class="smoke {dl}"><circle cx="{cx+6}" cy="{cy-40}" r="10" fill="#5a4a4a" opacity=".45" filter="url(#soft)"/></g>'
        out += ''.join(f'<g class="rise {dl}"><circle cx="{cx+dx}" cy="{cy-24}" r="{r}" fill="#ffb02e"/></g>' for dx, r in ((-12, 2.6), (11, 2)))
    return out

# ---- 岩の ゴツゴツ（りんかくを かくばらせ、中を 岩の板で うめる。すきまは ようがん）----
# 生成には shapely が必要（pip install shapely）。できあがった SVG は ふつうの パスだけ
import random
from shapely.geometry import Polygon, MultiPoint, Point
from shapely import voronoi_polygons
def pts2d(pts): return 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + ' Z'
ROCK = ['#7a4038', '#6a3630', '#74403a', '#5e302c']
ROCKD = ['#4e2622', '#44201e', '#4a2622', '#3e1c1a']
def rough(pts, rnd, amp=5):
    # 辺の まん中を 外へ おし出して ゴツゴツさせる
    P = Polygon(pts); cx, cy = P.centroid.x, P.centroid.y; out = []
    for i, (x1, y1) in enumerate(pts):
        x2, y2 = pts[(i + 1) % len(pts)]; out.append((x1, y1))
        ln = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** .5
        if ln > 18:
            nx, ny = (y2 - y1) / ln, -(x2 - x1) / ln
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            if (mx + nx - cx) ** 2 + (my + ny - cy) ** 2 < (mx - cx) ** 2 + (my - cy) ** 2: nx, ny = -nx, -ny
            a = rnd.uniform(.5, 1) * amp
            out.append((mx + nx * a + rnd.uniform(-3, 3), my + ny * a))
    return out
def rock(pts, seed, cell=40, dark=False, holes=(), w=3.2, amp=5):
    rnd = random.Random(seed)
    if amp: pts = rough(pts, rnd, amp)
    poly = Polygon(pts)
    x0, y0, x1, y1 = poly.bounds
    seeds = []
    y = y0
    while y < y1 + cell:
        x = x0 + (cell / 2 if int((y - y0) / cell) % 2 else 0)
        while x < x1 + cell:
            seeds.append((x + rnd.uniform(-.3, .3) * cell, y + rnd.uniform(-.3, .3) * cell)); x += cell
        y += cell * .87
    inner = poly.buffer(-3.5, join_style='mitre')
    for h in holes: inner = inner.difference(h)
    cells = voronoi_polygons(MultiPoint(seeds), extend_to=poly.buffer(cell))
    base = '#e0601e' if not dark else '#a8401a'
    out = f'<path d="{pts2d(pts)}" fill="{base}"/>'
    pal = ROCKD if dark else ROCK
    for c in cells.geoms:
        g = c.intersection(inner).buffer(-1.3, join_style='mitre')
        for p in (getattr(g, 'geoms', None) or [g]):
            if p.is_empty or p.area < 20 or p.geom_type != 'Polygon': continue
            co = list(p.exterior.coords)[:-1]
            out += f'<path d="{pts2d(co)}" fill="{rnd.choice(pal)}" stroke="{L}" stroke-width="1.4" stroke-linejoin="round" stroke-opacity=".6"/>'
            # 板の 上がわに 光
            top = sorted(co, key=lambda q: q[1])[:2]
            if rnd.random() < .6:
                out += f'<path d="M{top[0][0]:.0f} {top[0][1]+2:.0f} L{top[1][0]:.0f} {top[1][1]+2:.0f}" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity=".22"/>'
    out += f'<path d="{pts2d(pts)}" fill="none" stroke="{L}" stroke-width="{w}" stroke-linejoin="round"/>'
    return out

# ---- しっぽ（右へ のびる。トゲ4本）----
# つけねを 太く → 地面まで 下ろし、右はしで ゆるやかに 巻き上げる（トゲ4本）
tail_p = [(338, 290), (362, 324), (388, 354), (418, 376), (446, 386), (466, 380), (476, 362), (478, 338),
          (472, 316), (464, 330), (460, 350), (446, 356), (424, 344), (406, 322), (396, 294), (390, 262),
          (384, 232), (378, 208)]
tail_sp = ''.join(shape(f'M{x1} {y1} L{tx} {ty} L{x2} {y2} Z', 'url(#vk5)', 2.4)
                  for x1, y1, x2, y2, tx, ty in [(390, 254, 394, 278, 414, 258), (398, 296, 406, 318, 426, 298),
                                                 (414, 334, 428, 346, 440, 322), (442, 354, 456, 356, 458, 334)])
stretch = lambda x: x + 30 * max(0, (x - 390) / 88)
tail_p = [(stretch(x), y) for x, y in tail_p]
tail_sp = ''.join(shape(f'M{stretch(x1):.0f} {y1} L{stretch(tx):.0f} {ty} L{stretch(x2):.0f} {y2} Z', 'url(#vk5)', 2.4)
                  for x1, y1, x2, y2, tx, ty in [(390, 254, 394, 278, 414, 258), (398, 296, 406, 318, 426, 298),
                                                 (414, 334, 428, 346, 440, 322), (442, 354, 456, 356, 458, 334)])
tail = tail_sp + rock(tail_p, 5, 30, amp=4)

# ---- 体（胴）----
body_p = [(206, 104), (230, 124), (252, 144), (282, 152), (316, 160), (346, 174), (372, 196), (384, 224),
          (376, 248), (356, 264), (330, 272), (300, 272), (270, 268), (248, 266), (222, 262), (196, 250),
          (176, 232), (164, 210), (160, 186), (162, 160), (176, 128)]
volcs = make_volcs(body_p[:8])
# 胸の 筋肉（大きな 岩の板 2まい）
pecs = (shape('M178 186 L206 170 L234 184 L240 222 L222 246 L194 240 L174 220 Z', 'url(#pc5)', 2.6)
        + shape('M206 250 L228 228 L252 236 L262 262 L240 266 L214 262 Z', 'url(#pc5)', 2.4)
        + hl('M184 192 L206 178 L228 188', 2.4, .35) + hl('M214 246 L228 234 L248 240', 2, .3))
# おく側の うで・脚（こい色）
leg_p = [(306, 262), (336, 252), (364, 258), (382, 276), (384, 302), (366, 322), (338, 336), (354, 354),
         (368, 374), (362, 392), (354, 404), (292, 404), (294, 394), (310, 390), (326, 388), (334, 378),
         (318, 364), (298, 352), (284, 332), (286, 298)]
# うで：ひじを 曲げて 前に つき出し、つめを 広げて かまえる（えものを おそう 直前）
arm_p = [(214, 222), (238, 240), (236, 270), (214, 292), (190, 298), (166, 286), (146, 268), (128, 256),
         (118, 240), (126, 226), (146, 230), (166, 246), (184, 252), (194, 236)]
def claw_at(x, y, ang, ln=22, w=5):
    return (f'<g transform="translate({x} {y}) rotate({ang})"><path d="M{w} 0 Q{w+3} {ln*.7:.0f} {w+9} {ln} Q-2 {ln*.6:.0f} {-w} 0 Z" '
            f'fill="#f2e6c8" stroke="{L}" stroke-width="2.2" stroke-linejoin="round"/></g>')
def paw(dx, dy, fill, ln, w):
    c = claw_at(112 + dx, 228 + dy, 112, ln, w) + claw_at(106 + dx, 242 + dy, 86, ln, w) + claw_at(110 + dx, 256 + dy, 58, ln, w)
    return c + shape(f'M{130+dx} {222+dy} L{114+dx} {222+dy} L{102+dx} {236+dy} L{104+dx} {254+dy} L{120+dx} {262+dy} L{134+dx} {254+dy} Z', fill, 2.8)
sh = lambda P, dx, dy: [(x + dx, y + dy) for x, y in P]
far_leg = rock(sh(leg_p, -42, 0), 11, 32, dark=True, w=3) + claws([(254, 400), (266, 400), (280, 400)], 12, 5)
far_arm = rock(sh(arm_p, -30, -30), 12, 30, dark=True, w=3) + paw(-30, -30, '#4a2420', 26, 5)
near_leg = rock(leg_p, 13, 32) + claws([(298, 400), (312, 400), (326, 400)], 14, 6)
near_arm = rock(arm_p, 14, 30) + paw(0, 0, '#6a3630', 32, 6)
body = rock(body_p, 7, 46, w=3.4, amp=7)

# ---- 頭（左向き。後頭部は うしろへ するどく とがる。口を開けて ほのおを はく）----
cx_, cy_ = 124, 86
head_p = [(22, 76), (36, 66), (70, 64), (90, 70), (104, 62), (130, 56), (156, 60), (180, 70), (206, 80), (268, 104),
          (214, 120), (234, 146), (210, 152), (190, 160), (160, 162), (126, 166), (90, 164), (58, 158), (42, 150), (118, 118), (30, 86)]
head_holes = [Point(cx_, cy_ + 2).buffer(24), Polygon([(20, 70), (60, 70), (58, 100), (20, 92)])]
mouth = ('<path d="M32 88 L118 118 L46 148 Q64 118 32 88 Z" fill="#5a1018"/>'
         '<path d="M60 104 L108 119 L64 134 Z" fill="#ffb02e" opacity=".9" class="glow"/>')
teeth = (f'<path d="M44 91 L46 108 L56 95 Z M76 103 L78 119 L88 107 Z" fill="#fff" stroke="{L}" stroke-width="2" stroke-linejoin="round"/>'
         f'<path d="M60 146 L62 130 L72 142 Z M88 133 L92 118 L100 129 Z" fill="#fff" stroke="{L}" stroke-width="2" stroke-linejoin="round"/>')
# ほのおは 口の おくから 出て、口の 開いた ところを おおう
breath = (f'<g class="flickL"><path d="M106 118 C82 104 56 90 26 84 C28 96 10 100 -4 102 C8 112 4 126 -6 134 C10 138 22 146 28 156 C54 144 82 132 106 122 Z" '
          f'fill="url(#fb5)" stroke="{L}" stroke-width="2.4" stroke-linejoin="round" opacity=".95"/>'
          f'<path d="M100 119 C80 112 60 106 36 104 C40 114 28 118 18 120 C30 126 34 132 34 138 C60 130 80 124 100 121 Z" fill="#fff6c0"/></g>')
horn_far = shape('M170 70 C178 52 180 36 172 16 C190 30 198 54 190 84 Z', 'url(#hn5d)', 2.8)
horn = shape('M160 70 C184 62 202 50 210 28 C220 50 212 76 190 94 Z', 'url(#hn5)', 3) + hl('M172 68 C190 60 202 50 206 40', 2.2, .8)
crest = ''.join(shape(f'M{x1} {y1} L{tx} {ty} L{x2} {y2} Z', 'url(#vk5)', 2.6)
                for x1, y1, x2, y2, tx, ty in [(222, 130, 230, 144, 256, 140), (226, 146, 210, 152, 240, 170), (190, 158, 170, 162, 196, 184)])
eye = (f'<ellipse cx="{cx_}" cy="{cy_+2}" rx="22" ry="15" fill="#ffcf3a" opacity=".7" filter="url(#soft)" class="glow"/>'
       f'<clipPath id="e5"><path d="M{cx_-24} {cy_+2} L{cx_+24} {cy_-14} L{cx_+24} {cy_+24} L{cx_-24} {cy_+24} Z"/></clipPath>'
       f'<g clip-path="url(#e5)"><ellipse cx="{cx_}" cy="{cy_}" rx="16" ry="13" fill="#ffd84a" stroke="{L}" stroke-width="2.4"/>'
       f'<ellipse cx="{cx_-4}" cy="{cy_+2}" rx="3.6" ry="9" fill="#3a1410"/>'
       f'<circle cx="{cx_-8}" cy="{cy_-1}" r="3.2" fill="#fff"/><circle cx="{cx_+5}" cy="{cy_+7}" r="1.6" fill="#fff"/></g>'
       f'<path d="M{cx_-20} {cy_+1} L{cx_+20} {cy_-12}" stroke="{L}" stroke-width="3.8" stroke-linecap="round"/>')


# ---- 体を 流れる ようがん（光る すじの 上を、明るい つぶが 流れていく）----
def flow(d, w=4, dl=''):
    w *= 1.6
    k = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
    return (f'<path d="{d}" {k} stroke="#ff8a2a" stroke-width="{w+8:.1f}" opacity=".75" filter="url(#soft)" class="glow2 {dl}"/>'
            f'<path d="{d}" {k} stroke="#ff9a2a" stroke-width="{w:.1f}"/>'
            f'<path d="{d}" {k} stroke="#ffd24a" stroke-width="{w*.62:.1f}" class="glow2 {dl}"/>'
            f'<path d="{d}" {k} stroke="#fffbe0" stroke-width="{w*.3:.1f}" stroke-dasharray="10 12" class="flow {dl}"/>')
body_flow = (flow('M232 150 C226 172 236 190 228 212 C222 230 230 246 222 262', 6, 'd1')
             + flow('M230 196 C244 204 250 216 262 226', 3.6, 'd2')
             + flow('M302 160 C292 184 304 200 296 222 C290 240 300 256 292 270', 6)
             + flow('M298 206 C316 212 324 226 340 232', 3.6, 'd3')
             + flow('M368 196 C360 214 370 230 362 250 C358 262 362 268 356 276', 5.4, 'd2')
             + flow('M364 226 C350 236 342 248 334 262', 3.4, 'd1')
             + flow('M198 118 C186 140 196 156 186 178', 3, 'd3'))
head_flow = (flow('M146 60 C160 76 148 92 162 108 C176 122 196 128 216 140', 3.2, 'd2')
             + flow('M162 108 C150 120 156 132 146 146', 2.2, 'd1')
             + flow('M60 66 C76 76 90 70 102 80', 2.2, 'd3')
             + flow('M140 156 C160 156 174 154 190 150', 2.8))
head = f'''{horn_far}{crest}
{rock(head_p, 3, 36, w=3.4, amp=0)}
{head_flow}
<path d="M30 72 Q36 68 40 74 Q34 78 30 72 Z" fill="{L}"/>
<g class="puff"><circle cx="34" cy="62" r="5" fill="#9a8c88" opacity=".55"/></g>
{mouth}{breath}{teeth}{eye}{horn}
'''
leg_flow = flow('M334 262 C320 284 332 300 318 322 C310 336 322 346 334 358', 4.6, 'd2')
arm_flow = flow('M222 232 C212 250 222 262 206 282', 4, 'd1')
tail_flow = flow('M384 236 C392 270 400 300 418 326 C436 350 462 370 490 366 C500 362 504 350 500 336', 4.8, 'd3')

# ---- 地面の ようがん ----
ground = (lava('M10 404 C40 396 70 410 110 400 M380 404 C410 398 440 408 474 398', 2.6, 'glow d2'))
embers = ''.join(f'<g class="rise {d}"><circle cx="{x}" cy="{y}" r="{r}" fill="#ff9a3a"/></g>'
                 for x, y, r, d in [(40, 380, 3, ''), (450, 330, 2.5, 'd1'), (24, 300, 2.5, 'd2'), (110, 260, 2, 'd3'),
                                    (200, 410, 2.5, 'd1'), (290, 410, 2, 'd3'), (70, 40, 2, 'd2'), (160, 20, 2.5, '')])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 480 444" width="480" height="444">
<title>かざんの ぬし しんの すがた</title>
<style>
  .breathe{{transform-origin:280px 400px;animation:br 3s ease-in-out infinite}}
  @keyframes br{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.012,1.022)}}}}
  .sway{{transform-origin:180px 168px;animation:sw 4s ease-in-out infinite}}
  @keyframes sw{{0%,100%{{transform:rotate(-1.5deg)}}50%{{transform:rotate(1.5deg)}}}}
  .wag{{transform-origin:376px 240px;animation:wg 3.4s ease-in-out infinite}}
  @keyframes wg{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-1.2deg)}}}}
  .glow{{animation:gl 2.4s ease-in-out infinite}}
  @keyframes gl{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
  .d1{{animation-delay:.6s}}.d2{{animation-delay:1.2s}}.d3{{animation-delay:1.8s}}
  .flick{{transform-box:fill-box;transform-origin:50% 100%;animation:fk .5s ease-in-out infinite alternate}}
  @keyframes fk{{from{{transform:scale(1,1)}}to{{transform:scale(.88,1.14)}}}}
  .flickL{{transform-box:fill-box;transform-origin:100% 50%;animation:fkL .45s ease-in-out infinite alternate}}
  @keyframes fkL{{from{{transform:scale(1,1)}}to{{transform:scale(1.12,.9)}}}}
  .glow2{{animation:g2 2s ease-in-out infinite}}
  @keyframes g2{{0%,100%{{opacity:.8}}50%{{opacity:1}}}}
  .flow{{animation:fw 1.6s linear infinite}}
  @keyframes fw{{to{{stroke-dashoffset:-40}}}}
  .rise{{animation:rs 3.6s linear infinite}}
  @keyframes rs{{0%{{transform:translateY(0);opacity:0}}15%{{opacity:1}}100%{{transform:translateY(-110px);opacity:0}}}}
  .smoke{{animation:sm 4s ease-out infinite}}
  @keyframes sm{{0%{{transform:translate(0,10px) scale(.5);opacity:0}}25%{{opacity:.7}}100%{{transform:translate(24px,-40px) scale(1.8);opacity:0}}}}
  .puff{{animation:pf 2.6s ease-out infinite}}
  @keyframes pf{{0%{{transform:translate(0,0) scale(.6);opacity:0}}20%{{opacity:.8}}100%{{transform:translate(-10px,-36px) scale(1.6);opacity:0}}}}
</style>
<defs>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
  <radialGradient id="bg" cx="50%" cy="55%" r="55%"><stop offset="0" stop-color="#ffb08a"/><stop offset=".6" stop-color="#ffb08a" stop-opacity=".5"/><stop offset="1" stop-color="#ffb08a" stop-opacity="0"/></radialGradient>
  <linearGradient id="bd5" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a3e34"/><stop offset="1" stop-color="#4e2420"/></linearGradient>
  <linearGradient id="dk5" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5e2a26"/><stop offset="1" stop-color="#361816"/></linearGradient>
  <linearGradient id="pc5" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9a5446"/><stop offset="1" stop-color="#6a3630"/></linearGradient>
  <linearGradient id="vk5" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7a6560"/><stop offset="1" stop-color="#3e2e2c"/></linearGradient>
  <linearGradient id="hn5" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#e8dcc0"/><stop offset="1" stop-color="#b8a27a"/></linearGradient>
  <linearGradient id="hn5d" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#b8a684"/><stop offset="1" stop-color="#8a7656"/></linearGradient>
  <linearGradient id="fl5" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ff6a2a"/><stop offset=".6" stop-color="#ffb02e"/><stop offset="1" stop-color="#ffe36b"/></linearGradient>
  <linearGradient id="fb5" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#ffe36b"/><stop offset=".5" stop-color="#ffb02e"/><stop offset="1" stop-color="#ff5a2a"/></linearGradient>
</defs>
<ellipse cx="240" cy="230" rx="238" ry="205" fill="url(#bg)"/>
<ellipse cx="256" cy="404" rx="200" ry="12" fill="{L}" opacity=".2"/>
{ground}
<g transform="translate(-28 0)">
<g class="breathe">
<g transform="translate(0 18)"><g class="wag">{tail}{tail_flow}</g>{far_arm}</g>
{far_leg}
<g transform="translate(0 18)">{body}{pecs}{body_flow}{volcs}</g>
{near_leg}<g>{leg_flow}</g>
<g transform="translate(0 18)">{near_arm}{arm_flow}</g>
</g>
<g class="sway"><g transform="translate(-6 8) translate(200 130) scale(.8) translate(-200 -130)">{head}</g></g>
</g>
{embers}
</svg>'''
open(sys.argv[1] if len(sys.argv) > 1 else '5_kazan_shin.svg', 'w').write(svg)
