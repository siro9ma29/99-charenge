import math, sys
# 裏ボス 第1形態 ククドラ（9つ首の竜）v2 — しろさんの参考画像をもとに 描き直し
#   全身で 立つ赤い竜。首9本（まん中だけ正面、左右4本ずつ 横顔で外を向く）、
#   クリーム色の おなかの いた・炎・岩の足場・右へ のびる しっぽ・つばさ
#   ひたいの 宝石に 1〜9（左から。数字は いつも まっすぐ）
L = '#2b2b3a'
K = 'class="kdk"'
RED, RED_D, RED_L = '#d9343c', '#9a1c2c', '#ff7a5a'
CR, CR_D = '#f6e8c8', '#d8c196'
HORN = '#f1e2c0'

def f1(v): return f'{v:.1f}'
def SC(d): return f'<path d="{d}" fill="url(#kd_sc)"/>'
def poly(pts): return 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + ' Z'

def cub(p, t):
    a, b, c, d = p; u = 1 - t
    return (u**3*a[0] + 3*u*u*t*b[0] + 3*u*t*t*c[0] + t**3*d[0],
            u**3*a[1] + 3*u*u*t*b[1] + 3*u*t*t*c[1] + t**3*d[1])

def tube(p, w0, w1, band=(-.2, .45), plates=True, n=16, fill=RED, spikes=0, band0=None, open0=False):
    # ベジェに そった 太い管（首・しっぽ）。band は おなかの帯（法線方向の はば。-0.5〜0.5）
    P, N, W = [], [], []
    for i in range(n + 1):
        t = i / n
        x, y = cub(p, t); x2, y2 = cub(p, min(1, t + .01)); x0, y0 = cub(p, max(0, t - .01))
        dx, dy = x2 - x0, y2 - y0; l = math.hypot(dx, dy) or 1
        P.append((x, y)); N.append((-dy / l, dx / l)); W.append(w0 + (w1 - w0) * t)
    side = lambda k: [(P[i][0] + N[i][0] * W[i] * k, P[i][1] + N[i][1] * W[i] * k) for i in range(n + 1)]
    def ab(i):  # i番目の 帯の はば（band0 → band へ なめらかに）
        if not band0: return band
        u = min(1, i / (n * .75)); u = u * u * (3 - 2 * u)
        return (band0[0] + (band[0] - band0[0]) * u, band0[1] + (band[1] - band0[1]) * u)
    bside = lambda j: [(P[i][0] + N[i][0] * W[i] * ab(i)[j], P[i][1] + N[i][1] * W[i] * ab(i)[j]) for i in range(n + 1)]
    s = ''
    if spikes:  # せなかの トゲ（band の 反対がわ）
        sg = -1 if (band[0] + band[1]) > 0 else 1
        for j in range(spikes):
            i = int((j + 2.8) / (spikes + 2.6) * n)
            bx, by = P[i]; nx, ny = N[i]; w = W[i]
            tx, ty = cub(p, min(1, i / n + .03))
            s += (f'<path d="M{f1(bx + nx*w*.5*sg)} {f1(by + ny*w*.5*sg)} L{f1(tx + nx*w*1.05*sg)} {f1(ty + ny*w*1.05*sg)} '
                  f'L{f1(bx + nx*w*.5*sg + (tx-bx)*1.6)} {f1(by + ny*w*.5*sg + (ty-by)*1.6)} Z" fill="{RED_D}" {K} stroke-width="2.6"/>')
    outline = side(.5) + side(-.5)[::-1]
    s += f'<path d="{poly(outline)}" fill="{fill}"/>' + SC(poly(outline))
    a, b = band
    s += f'<path d="{poly(bside(1) + bside(0)[::-1])}" fill="{CR}"/>'
    if plates:
        pl = []
        for i in range(1, n):
            x, y = P[i]; nx, ny = N[i]; w = W[i]; ai, bi = ab(i)
            pl.append(f'M{x + nx*w*ai:.0f} {y + ny*w*ai:.0f}L{x + nx*w*bi:.0f} {y + ny*w*bi:.0f}')
        s += f'<path d="{"".join(pl)}" stroke="{CR_D}" stroke-width="2.2" stroke-linecap="round"/>'
    s += f'<path d="{"M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in bside(1))}" fill="none" stroke="{L}" stroke-width="2" opacity=".55"/>'
    hl = side(-.33 if (a + b) > 0 else .33)
    s += f'<path d="{"M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in hl[(int(n*.8) if band0 else 2):-6])}" fill="none" stroke="{RED_L}" stroke-width="3" stroke-linecap="round" opacity=".6"/>'
    if open0:  # 根もとは 体に つながるので 線を引かない
        s += f'<path d="{"M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in side(.5) + side(-.5)[::-1])}" fill="none" {K} stroke-width="3.4"/>'
    else:
        s += f'<path d="{poly(outline)}" fill="none" {K} stroke-width="3.4"/>'
    return s

def flame(x, y, h, w, rot=0, cls='fl', delay=0):
    d = (f'M0 0 C{-w} {-h*.2} {-w*.9} {-h*.62} {-w*.2} {-h*.78} C{-w*.4} {-h*.55} {-w*.05} {-h*.5} 0 {-h*.62} '
         f'C{w*.1} {-h*.82} {w*.3} {-h*.9} {w*.15} {-h} C{w*.9} {-h*.72} {w} {-h*.3} 0 0 Z')
    inner = f'M0 {-h*.06} C{-w*.5} {-h*.2} {-w*.4} {-h*.5} 0 {-h*.62} C{w*.3} {-h*.44} {w*.5} {-h*.2} 0 {-h*.06} Z'
    return (f'<g transform="translate({f1(x)} {f1(y)}) rotate({rot})"><g class="{cls}" style="animation-delay:-{delay:.2f}s">'
            f'<path d="{d}" fill="url(#kd_fl)"/><path d="{inner}" fill="#fff3a8" opacity=".9"/></g></g>')

# ---- 横顔の 頭（ローカル：0,0 が 首の つけね。+x が 鼻先）----
def side_head():
    # シャープな横顔：長い鼻先・角ばった まゆの いた・細い つり目・するどい下あご
    s = ''
    # 角（うしろ上へ。2本）
    s += (f'<path d="M-8 -16 C-24 -26 -36 -38 -44 -60 C-26 -48 -12 -40 2 -30 Z" fill="{HORN}" {K} stroke-width="2.8"/>'
          f'<path d="M6 -24 C-2 -40 -4 -54 2 -72 C14 -56 20 -42 24 -28 Z" fill="{HORN}" {K} stroke-width="2.8"/>'
          f'<path d="M-22 -32 l6 -3 M-32 -44 l6 -2 M2 -40 l8 0 M1 -54 l7 0" stroke="#c9ad78" stroke-width="2.2" stroke-linecap="round"/>')
    # エラの トゲ（3本、うしろへ）
    s += f'<path d="M-6 -4 L-40 -14 L-20 0 L-44 6 L-20 10 L-36 22 L-2 16 Z" fill="{RED_D}" {K} stroke-width="2.6"/>'
    # 下あご（開いた口。とがった あご先）
    s += (f'<path d="M4 10 L36 18 L70 22 L76 20 L72 28 L40 30 L10 24 Z" fill="{RED}" {K} stroke-width="3"/>'
          f'<path d="M12 24 L40 28 L70 26" fill="none" stroke="{CR}" stroke-width="4" stroke-linecap="round"/>')
    s += f'<path d="M14 6 L40 14 L72 18 L80 6 L46 4 L22 2 Z" fill="#5a0f22"/>'
    s += f'<path d="M26 10 L50 14 L64 15" fill="none" stroke="#ff8a8a" stroke-width="3.6" stroke-linecap="round" opacity=".8"/>'
    s += ''.join(f'<path d="M{x} {y} l3 -7 l3 7 Z" fill="#fff" {K} stroke-width="1.5"/>' for x, y in ((30, 18), (44, 20), (58, 22)))
    # 頭（頭頂〜まゆの いた〜長い鼻先〜上あご を 1つの りんかく）
    s += (f'<path d="M-14 6 C-18 -8 -12 -20 2 -24 L24 -30 L36 -22 L54 -18 L78 -12 L88 -6 L84 2 L72 4 '
          f'L46 4 L26 4 C16 6 10 10 6 14 C-4 16 -12 12 -14 6 Z" fill="url(#kd_h)" {K} stroke-width="3.2"/>')
    # 鼻すじの トゲ・鼻のあな
    s += f'<path d="M58 -17 L64 -25 L66 -15 Z M70 -13 L76 -20 L78 -10 Z" fill="{RED_D}" {K} stroke-width="2"/>'
    s += f'<path d="M80 -4 l4 -2" stroke="{L}" stroke-width="2.6" stroke-linecap="round"/>'
    # 上の歯・きば
    s += ''.join(f'<path d="M{x} 4 l3 8 l3 -8 Z" fill="#fff" {K} stroke-width="1.5"/>' for x in (34, 48, 60))
    s += f'<path d="M70 3 l3 14 l4 -13 Z" fill="#fff" {K} stroke-width="1.8"/>'
    # ほおの すじ（シャープな かげ）
    s += f'<path d="M2 2 L18 -4 L30 -2" fill="none" stroke="{RED_D}" stroke-width="2.4" stroke-linecap="round"/>'
    s += f'<path d="M30 -6 L60 -8" fill="none" stroke="{RED_D}" stroke-width="2" stroke-linecap="round" opacity=".7"/>'
    # まゆの いた（角ばった ほね）＋ 細い つり目
    s += f'<path d="M12 -16 L36 -24 L46 -18 L30 -14 Z" fill="{RED_D}" {K} stroke-width="2.4"/>'
    s += (f'<path d="M20 -12 L44 -18 C42 -12 36 -8 28 -8 C24 -8 21 -10 20 -12 Z" fill="url(#kd_e)" {K} stroke-width="2.2"/>'
          f'<path d="M33 -15 C34 -12 34 -10 33 -8" stroke="{L}" stroke-width="2.6" stroke-linecap="round"/>')
    return s

GEM_LOCAL = (5, -15)

def gem(x, y, n, r=9):
    return (f'<path d="M{f1(x)} {f1(y-r)} L{f1(x+r*.8)} {f1(y)} L{f1(x)} {f1(y+r)} L{f1(x-r*.8)} {f1(y)} Z" fill="url(#kd_g)" {K} stroke-width="2.2"/>'
            f'<text x="{f1(x)}" y="{f1(y+4.2)}" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="{r*1.25:.0f}" fill="{L}">{n}</text>')

def head_at(x, y, m, sc, rot, n):
    # m=1 右むき、m=-1 左むき。数字は 鏡にしない
    gx, gy = GEM_LOCAL
    a = math.radians(rot)
    rx, ry = gx*math.cos(a) - gy*math.sin(a), gx*math.sin(a) + gy*math.cos(a)
    wx, wy = x + rx*sc*m, y + ry*sc
    flames = (flame(x + (-4*m)*sc, y - 40*sc, 56*sc, 20*sc, -14*m, delay=n*.3)
              + flame(x + (-30*m)*sc, y - 26*sc, 40*sc, 14*sc, -44*m, delay=n*.3 + .5))
    return (flames + f'<g transform="translate({f1(x)} {f1(y)}) scale({m*sc:.2f} {sc:.2f}) rotate({rot})">{side_head()}</g>'
            + gem(wx, wy, n, 9*sc))

def front_head(x, y, sc):
    s = ''
    for m in (1, -1):
        s += (f'<path d="M{12*m} -26 C{26*m} -42 {40*m} -50 {44*m} -80 C{56*m} -52 {46*m} -28 {28*m} -14 Z" fill="{HORN}" {K} stroke-width="3"/>'
              f'<path d="M{26*m} -36 l{6*m} 2 M{36*m} -50 l{6*m} 1 M{42*m} -64 l{6*m} 0" stroke="#c9ad78" stroke-width="2.2" stroke-linecap="round"/>'
              # エラ（するどい トゲ3本）
              f'<path d="M{26*m} -14 L{58*m} -26 L{40*m} -8 L{62*m} 0 L{38*m} 6 L{54*m} 20 L{24*m} 12 Z" fill="{RED_D}" {K} stroke-width="2.8"/>')
    # とさか（3本）
    s += (f'<path d="M-14 -30 L-12 -54 L-4 -36 L0 -66 L4 -36 L12 -54 L14 -30 Z" fill="{RED}" {K} stroke-width="2.8"/>'
          f'<path d="M-2 -38 L0 -58 L2 -38 Z" fill="{RED_L}"/>')
    # 下あご（V字）
    s += (f'<path d="M-18 14 L-10 44 L0 54 L10 44 L18 14 Z" fill="{RED}" {K} stroke-width="3"/>'
          f'<path d="M-13 16 L-7 38 L0 44 L7 38 L13 16 Z" fill="#5a0f22"/>'
          f'<path d="M-7 32 L0 38 L7 32 L0 41 Z" fill="#ff8a8a" opacity=".85"/>'
          f'<path d="M-8 46 L0 52 L8 46" fill="none" stroke="{CR}" stroke-width="3.6" stroke-linecap="round"/>')
    # 頭（角ばった 逆三角形）
    s += (f'<path d="M0 -36 L18 -32 L30 -20 L32 -6 L22 8 L14 22 L6 30 L-6 30 L-14 22 L-22 8 L-32 -6 L-30 -20 L-18 -32 Z" '
          f'fill="url(#kd_h)" {K} stroke-width="3.4"/>')
    # 鼻すじ・ほおの かげ
    s += (f'<path d="M-6 6 L0 2 L6 6 L4 24 L-4 24 Z" fill="{RED_L}" opacity=".45"/>'
          f'<path d="M-6 20 l3 -2 M3 18 l3 2" stroke="{L}" stroke-width="2.4" stroke-linecap="round"/>'
          f'<path d="M-26 -2 L-16 10 M26 -2 L16 10" stroke="{RED_D}" stroke-width="2.6" stroke-linecap="round"/>'
          f'<path d="M-12 22 L-8 36 L-5 24 Z M5 24 L8 36 L12 22 Z" fill="#fff" {K} stroke-width="2"/>')
    for m in (1, -1):
        # まゆの いた ＋ 細い つり目
        s += (f'<path d="M{4*m} -10 L{28*m} -22 L{32*m} -14 L{12*m} -6 Z" fill="{RED_D}" {K} stroke-width="2.4"/>'
              f'<path d="M{7*m} -5 L{27*m} -13 C{27*m} -6 {21*m} -1 {13*m} -1 C{9*m} -1 {7*m} -3 {7*m} -5 Z" fill="url(#kd_e)" {K} stroke-width="2.4"/>'
              f'<path d="M{17*m} -9 C{18*m} -6 {18*m} -3 {17*m} -1" stroke="{L}" stroke-width="3" stroke-linecap="round" fill="none"/>')
    fl = flame(x, y - 44*sc, 46*sc, 18*sc, 0, delay=.2) + flame(x - 30*sc, y - 32*sc, 30*sc, 12*sc, -30, delay=.9) + flame(x + 30*sc, y - 32*sc, 30*sc, 12*sc, 30, delay=1.4)
    return fl + f'<g transform="translate({x} {y}) scale({sc})">{s}</g>' + gem(x, y - 24*sc, 5, 10*sc)

# ---- 9本の首 ----
# (番号, 首のつけね, 頭の位置, 向き m, 頭の かたむき, 大きさ, 首の太さ)
BS, BO = 1.3, (240, 416)
D = 18   # 腰を落とす量（体の中の座標）
def T(x, y): return (round(BO[0] + (x - BO[0]) * BS, 1), round(BO[1] + (y + D - BO[1]) * BS, 1))
BODY_TF = f'translate({BO[0]} {BO[1]}) scale({BS}) translate({-BO[0]} {-BO[1]})'
RIGHT = [(6, T(256, 206), (318, 20), 1, -34, .98, 31),
         (7, T(268, 212), (392, 74), 1, -16, .94, 29),
         (8, T(278, 222), (426, 148), 1, -2, .9, 27),
         (9, T(286, 234), (424, 222), 1, 10, .86, 26)]
HEADS = RIGHT + [(10 - n, (480 - b[0], b[1]), (480 - h[0], h[1]), -1, r, sc, w) for n, b, h, m, r, sc, w in RIGHT]

def neck_head(n, base, hp, m, rot, sc, w):
    a = math.radians(rot)
    fx, fy = math.cos(a) * m, math.sin(a)        # 鼻先の むき
    p = [base, (base[0] + (hp[0]-base[0])*.15, base[1] - 36), (hp[0] - fx*44*sc, hp[1] - fy*44*sc + 8), (hp[0] - fx*4, hp[1] + 4)]
    band = (-.1, .46) if m == 1 else (-.46, .1)   # おなかの帯は 下がわ（内がわ）
    delay = (n * .41) % 2.6
    return (f'<g class="nk" style="transform-origin:{base[0]}px {base[1]}px;animation-delay:-{delay:.2f}s">'
            + tube(p, w, w*.82, band=band) + head_at(hp[0], hp[1], m, sc, rot, n) + '</g>')

order = sorted(HEADS, key=lambda h: -abs(h[0] - 5))
necks = ''.join(neck_head(*h) for h in order)
center = ('<g class="nk" style="transform-origin:240px 190px;animation-delay:-1.1s">'
          + tube([(240, 210), (237, 160), (243, 116), (240, 76)], 46, 40, band=(-.34, .34))
          + front_head(240, 46, 1.42) + '</g>')

# ---- つばさ（体の うしろ）----
def wing(m):
    s = (f'<path d="M206 214 C170 160 120 110 40 96 C60 112 66 126 64 140 C80 140 92 148 96 160 C110 160 122 168 128 180 '
         f'C144 182 156 196 160 214 Z" fill="url(#kd_w)" {K} stroke-width="3.2"/>'
         + SC('M206 214 C170 160 120 110 40 96 C60 112 66 126 64 140 C80 140 92 148 96 160 C110 160 122 168 128 180 C144 182 156 196 160 214 Z') +
         f'<path d="M206 214 C170 160 120 110 40 96 M180 190 C150 170 100 146 64 140 M168 200 C150 186 120 170 96 160 M164 208 C150 196 140 186 128 180" '
         f'fill="none" stroke="{RED}" stroke-width="4" stroke-linecap="round"/>')
    return s if m == 1 else f'<g transform="translate(480 0) scale(-1 1)">{s}</g>'
wings = f'<g class="wgL">{wing(1)}</g><g class="wgR">{wing(-1)}</g>'

# ---- しっぽ（右へ のびて 上へ まく）----
TP = [(244, 318), (276, 404), (372, 418), (410, 360)]
tail = tube(TP, 48, 9, band=(-.48, .06), band0=(-.44, .44), spikes=6, open0=True)
tail += f'<path d="M412 362 L418 340 L424 360 Z M412 362 L394 354 L402 372 Z" fill="{RED_D}" {K} stroke-width="2.4"/>'

# ---- 体 ----
TORSO = 'M172 212 C150 240 156 296 184 330 C204 352 222 362 240 362 C258 362 276 352 296 330 C324 296 330 240 308 212 C286 196 194 196 172 212 Z'
torso = (f'<path d="{TORSO}" fill="url(#kd_b)"/>' + SC(TORSO) + f'<path d="{TORSO}" fill="none" {K} stroke-width="3.6"/>'
         f'<path d="M184 226 C176 250 178 282 192 304" fill="none" stroke="{RED_L}" stroke-width="5" stroke-linecap="round" opacity=".55"/>')
# むねの筋肉（左右2まい）。おなかと同じ クリーム色の いた＋だんの すじ
belly = ''
for m in (1, -1):
    pec = ('M238 214 C224 206 202 206 188 214 C180 226 182 242 192 252 C206 260 226 258 238 250 Z')
    lines = ('M192 226 C206 222 224 222 236 226 M190 240 C204 238 222 238 236 240')
    g = (f'<path d="{pec}" fill="{CR}" {K} stroke-width="2.8"/>'
         f'<path d="{lines}" fill="none" stroke="{CR_D}" stroke-width="2.4" stroke-linecap="round"/>'
         f'<path d="M196 216 C206 212 222 212 232 216" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".6"/>')
    belly += g if m == 1 else f'<g transform="translate(480 0) scale(-1 1)">{g}</g>'
# 腹筋（左右2列 × 4だん）
for y, hw in ((258, 30), (276, 28), (294, 25), (312, 21)):
    for m in (1, -1):
        x0, x1 = 240 + 2*m, 240 + hw*m
        belly += (f'<path d="M{x0} {y} L{x1} {y-2} L{x1 - 2*m} {y+15} L{x0} {y+16} Z" fill="{CR}" {K} stroke-width="2.4"/>'
                  f'<path d="M{x0 + 4*m} {y+13} L{x1 - 4*m} {y+12}" stroke="{CR_D}" stroke-width="2.2" stroke-linecap="round"/>')
# かたの よろい（トゲ）
for m in (1, -1):
    sh = (f'<path d="M168 214 C176 196 198 192 214 202 C206 214 190 222 172 226 Z" fill="{RED}" {K} stroke-width="3"/>'
          f'<path d="M184 202 L178 180 L196 198 Z" fill="{RED_D}" {K} stroke-width="2.6"/>')
    torso += sh if m == 1 else f'<g transform="translate(480 0) scale(-1 1)">{sh}</g>'

def part(d, fill, w=3.2):
    return f'<path d="{d}" fill="{fill}"/>' + SC(d) + f'<path d="{d}" fill="none" {K} stroke-width="{w}"/>'

def arm(m):
    s = (part('M180 222 C150 226 124 242 110 264 L132 282 C142 266 160 254 186 250 Z', 'url(#kd_b)')
         + part('M110 264 C96 280 90 296 92 308 L118 308 C120 296 126 288 132 282 Z', RED) +
         f'<path d="M112 270 L100 300" stroke="{CR}" stroke-width="6" stroke-linecap="round"/>'
         f'<path d="M80 306 C82 292 120 290 126 304 C130 316 118 324 102 324 C88 324 78 318 80 306 Z" fill="{RED}" {K} stroke-width="3"/>'
         + ''.join(f'<path d="M{x} {y} C{x+dx*.3} {y+10} {x+dx*.8} {y+16} {x+dx} {y+22} C{x+dx*.2+5} {y+16} {x+6} {y+10} {x+7} {y} Z" fill="{HORN}" {K} stroke-width="2.2"/>'
                   for x, y, dx in ((80, 312, -12), (92, 318, -6), (106, 320, 0), (118, 316, 8))))
    return s if m == 1 else f'<g transform="translate(480 0) scale(-1 1)">{s}</g>'

def leg(m):
    # もも：胴体の わきから そのまま はり出す。線は 外がわの りんかくだけ（胴体との 境目には 引かない）
    TH = 'M166 314 C140 322 112 338 100 360 C92 376 104 390 128 388 L168 370 C186 362 208 366 224 378 L232 320 Z'
    TH_LINE = 'M166 314 C140 322 112 338 100 360 C92 376 104 390 128 388 L168 370 C186 362 208 366 224 378'
    s = (f'<path d="{TH}" fill="url(#kd_t)"/>' + SC(TH) + f'<path d="{TH_LINE}" fill="none" {K} stroke-width="3.4"/>'
         # こしの 筋肉の すじ（やわらかい かげ）
         f'<path d="M172 330 C190 342 208 348 224 350" fill="none" stroke="{RED_D}" stroke-width="3" stroke-linecap="round" opacity=".55"/>' +
         f'<path d="M116 350 C132 338 156 332 180 330" fill="none" stroke="{RED_L}" stroke-width="4" stroke-linecap="round" opacity=".6"/>'
         + part('M102 366 L96 392 C96 398 102 402 112 402 L146 402 L142 378 Z', RED) +
         f'<path d="M84 406 C84 394 136 390 154 398 C162 406 152 412 136 412 L90 412 C84 412 84 408 84 406 Z" fill="{RED}" {K} stroke-width="3"/>'
         + ''.join(f'<path d="M{x} 406 C{x-4} 411 {x-8} 414 {x-14} 416 C{x-2} 418 {x+6} 414 {x+8} 408 Z" fill="{HORN}" {K} stroke-width="2.2"/>'
                   for x in (94, 114, 134, 152)))
    return s if m == 1 else f'<g transform="translate(480 0) scale(-1 1)">{s}</g>'

# ---- 岩の 足場 ----
rocks = ''.join(f'<path d="{d}" fill="{c}" {K} stroke-width="2.8"/>' for d, c in (
    ('M60 420 L72 392 L118 386 L132 404 L128 420 Z', '#6d6a74'),
    ('M150 420 L166 404 L214 408 L222 420 Z', '#85818c'),
    ('M258 420 L268 404 L320 400 L334 420 Z', '#85818c'),
    ('M350 420 L346 396 L392 380 L420 396 L424 420 Z', '#6d6a74'),
    ('M28 420 L36 404 L60 406 L62 420 Z', '#85818c'),
    ('M424 420 L432 398 L462 402 L470 420 Z', '#85818c')))
rocks += ''.join(f'<path d="{d}" fill="none" stroke="{L}" stroke-width="1.8" opacity=".45"/>' for d in
                 ('M84 396 L96 412', 'M370 392 L384 410', 'M286 406 L298 418'))

# ---- 炎（体の まわり）----
back_flames = (flame(36, 416, 120, 38, -14, 'fl2', .1) + flame(448, 416, 112, 36, 18, 'fl2', .9)
               + flame(96, 402, 96, 30, -8, 'fl2', 1.6) + flame(388, 404, 100, 32, 10, 'fl2', 2.2)
               + flame(10, 320, 90, 26, -28, 'fl2', .5) + flame(474, 240, 80, 24, 26, 'fl2', 1.3))
front_flames = flame(226, 420, 46, 18, -6, 'fl', .3) + flame(250, 420, 40, 16, 8, 'fl', 1.1)
embers = ''.join(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="#ffb14a" class="ember" style="animation-delay:-{d}s" transform="rotate(30 {x} {y})"/>'
                 for x, y, s, d in ((54, 330, 6, 0), (430, 330, 5, 1.1), (160, 380, 4, 2), (330, 370, 5, .6), (20, 200, 4, 1.6), (462, 120, 4, 2.4), (120, 200, 3, .9)))

bg = '<ellipse cx="240" cy="230" rx="300" ry="250" fill="url(#kd_bg)"/>'

style = '''<style>
  .kdk{stroke:#2b2b3a;stroke-linejoin:round;stroke-linecap:round}
  .breathe{transform-origin:240px 410px;animation:br 3.2s ease-in-out infinite}
  @keyframes br{0%,100%{transform:scale(1)}50%{transform:scale(1.008,1.016)}}
  .nk{animation:nk 2.8s ease-in-out infinite}
  @keyframes nk{0%,100%{transform:rotate(-1.8deg)}50%{transform:rotate(1.8deg)}}
  .wgL{transform-origin:206px 214px;animation:wl 3.2s ease-in-out infinite}
  .wgR{transform-origin:274px 214px;animation:wr 3.2s ease-in-out infinite}
  @keyframes wl{0%,100%{transform:rotate(0)}50%{transform:rotate(5deg)}}
  @keyframes wr{0%,100%{transform:rotate(0)}50%{transform:rotate(-5deg)}}
  .fl,.fl2{transform-origin:0 0;animation:fl .9s ease-in-out infinite alternate}
  .fl2{animation-duration:1.3s}
  @keyframes fl{0%{transform:scale(.9,.86) skewX(-4deg)}100%{transform:scale(1.06,1.1) skewX(4deg)}}
  .ember{animation:em 3s ease-in-out infinite}
  @keyframes em{0%,100%{opacity:0;transform:translateY(10px)}50%{opacity:.95;transform:translateY(-14px)}}
</style>'''

defs = f'''<defs>
  <radialGradient id="kd_bg" cx="50%" cy="55%" r="50%"><stop offset="0" stop-color="#ffd6c2"/><stop offset=".6" stop-color="#ffa48a" stop-opacity=".4"/><stop offset="1" stop-color="#ffa48a" stop-opacity="0"/></radialGradient>
  <linearGradient id="kd_h" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{RED_L}"/><stop offset=".45" stop-color="{RED}"/><stop offset="1" stop-color="{RED_D}"/></linearGradient>
  <linearGradient id="kd_b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8463e"/><stop offset="1" stop-color="{RED_D}"/></linearGradient>
  <linearGradient id="kd_t" x1="0" x2="0" gradientUnits="userSpaceOnUse" y1="{198+D}" y2="{362+D}"><stop offset="0" stop-color="#e8463e"/><stop offset="1" stop-color="{RED_D}"/></linearGradient>
  <linearGradient id="kd_w" x1="1" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#b52634"/><stop offset="1" stop-color="#e8503c"/></linearGradient>
  <linearGradient id="kd_fl" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#ffd23a"/><stop offset=".55" stop-color="#ff8a1e"/><stop offset="1" stop-color="#e8402a" stop-opacity=".85"/></linearGradient>
  <pattern id="kd_sc" width="14" height="12" patternUnits="userSpaceOnUse"><path d="M0 12 Q7 4 14 12 M-7 6 Q0 -2 7 6 M7 6 Q14 -2 21 6" fill="none" stroke="#6e0f22" stroke-width="1.5" opacity=".42"/></pattern>
  <radialGradient id="kd_e" cx=".4" cy=".4" r=".7"><stop offset="0" stop-color="#fff8c4"/><stop offset="1" stop-color="#ffc21e"/></radialGradient>
  <linearGradient id="kd_g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6c0"/><stop offset="1" stop-color="#f5b52e"/></linearGradient>
</defs>'''

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 480 444" width="480" height="444" overflow="hidden">\n'
       f'<title>うらボス ククドラ</title>\n{style}\n{defs}\n{bg}\n{back_flames}\n'
       f'<g class="breathe"><g transform="{BODY_TF} translate(0 {D})">{wings}</g>{necks}{center}<g transform="{BODY_TF}"><g transform="translate(0 {D})">{torso}</g>{tail}{leg(1)}{leg(-1)}<g transform="translate(0 {D})">{belly}{arm(1)}{arm(-1)}</g></g></g>\n'
       f'{rocks}{front_flames}{embers}\n</svg>\n')
open(sys.argv[1] if len(sys.argv) > 1 else 'kukudora.svg', 'w').write(svg)
