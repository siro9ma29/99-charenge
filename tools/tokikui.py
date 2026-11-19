import math, sys
# 裏ボス 第2形態 トキクイ v2 — しろさんの参考画像をもとに 描き直し
#   時計じかけの 機械の竜：せなかに 大きな砂時計、むねに 時計の たて（中で 歯車が回る）、
#   歯車の つばさ2まい、砂時計つきの かま、まわりを うずまく 青い砂と 金の砂
#   文字ばんは 2年で ならう 1〜12 の数字（ローマ数字は つかわない）
#   砂の量は #tk_sandTop / #tk_sandBot の transform（scaleY）で アプリから HP に合わせて動かせる
FRONT = False  # True＝正面がお、False＝横顔（v5）
L = '#2b2b3a'
K = 'class="tkk"'
BR, BR_L, BR_D = '#c49a48', '#efd590', '#86622a'      # 真ちゅう（さばくの 金より くすませる）
SV, SV_L, SV_D = '#b9c6d6', '#eef3f8', '#6c7b91'      # ぎん
CY, BL = '#56e0ff', '#2f7fe0'                          # 光る 水色・青

def P(pts, close=True): return 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + (' Z' if close else '')

def gear(cx, cy, r, n, cls, fill='url(#tk_br)', hub=CY, delay=0):
    pts = []
    for i in range(n * 4):
        a = 2 * math.pi * i / (n * 4)
        rr = r + r * .22 if i % 4 in (1, 2) else r
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    sp = ''.join(f'M{cx:.0f} {cy:.0f} L{cx + r*.78*math.cos(a):.0f} {cy + r*.78*math.sin(a):.0f}'
                 for a in (math.radians(k * 60) for k in range(6)))
    return (f'<g class="{cls}" style="transform-origin:{cx:.0f}px {cy:.0f}px;animation-delay:-{delay}s">'
            f'<path d="{P(pts)}" fill="{fill}" {K} stroke-width="2.6"/>'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.78:.0f}" fill="none" stroke="{BR_D}" stroke-width="2"/>'
            f'<path d="{sp}" stroke="{BR_D}" stroke-width="{max(2, r*.12):.1f}" stroke-linecap="round"/>'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r*.26:.0f}" fill="{hub}" {K} stroke-width="2"/></g>')

# ---- うずまく 砂（いちばん うしろ）----
def arc(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    return f'M{x0:.0f} {y0:.0f} A{r} {r} 0 {1 if (a1 - a0) % 360 > 180 else 0} 1 {x1:.0f} {y1:.0f}'
vortex = '<g class="vx" style="transform-origin:240px 206px">'
for r, a0, a1, w, c, op in ((214, 120, 300, 16, BL, .55), (204, 300, 470, 12, '#7cc8ff', .6), (194, 20, 160, 9, BL, .5),
                            (222, 200, 330, 5, '#d8b866', .8), (186, 160, 280, 6, '#7cc8ff', .55), (210, 340, 420, 4, '#d8b866', .8)):
    vortex += f'<path d="{arc(240, 206, r, a0, a1)}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'
for r, a0, a1, c in ((228, 100, 260, '#d8b866'), (178, 280, 420, '#a8e4ff'), (200, 40, 120, '#d8b866')):
    vortex += f'<path d="{arc(240, 206, r, a0, a1)}" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-dasharray="0.1 10"/>'
vortex += '</g>'

# ---- 歯車の つばさ（左・右）----
def blade(x, y, ang, ln, wd):
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
    pts = [(x + nx*wd*.5, y + ny*wd*.5), (x + ux*ln*.8 + nx*wd*.6, y + uy*ln*.8 + ny*wd*.6), (x + ux*ln, y + uy*ln),
           (x + ux*ln*.7 - nx*wd*.3, y + uy*ln*.7 - ny*wd*.3), (x - nx*wd*.5, y - ny*wd*.5)]
    edge = P([pts[1], pts[2]], False)
    return (f'<path d="{P(pts)}" fill="url(#tk_sv)" {K} stroke-width="2.6"/>'
            f'<path d="{edge}" stroke="{BR_L}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="{P([(x, y), (x + ux*ln*.72, y + uy*ln*.72)], False)}" stroke="{SV_D}" stroke-width="2" opacity=".6"/>')
def wing(cx, cy, angs, lens):
    s = ''.join(blade(cx, cy, a, l, 22) for a, l in zip(angs, lens))
    return s + gear(cx, cy, 34, 10, 'gR') + gear(cx + 30 * (1 if angs[0] > -90 else -1), cy + 34, 16, 8, 'gL', delay=1)
wingL = wing(128, 104, (-200, -165, -140, -118), (110, 120, 104, 84))
wingR = wing(356, 112, (-62, -36, -12, 14), (90, 118, 124, 100))

# ---- せなかの 大きな砂時計 ----
glass = ('M198 4 C198 40 232 54 240 66 C232 78 198 94 198 130 L282 130 C282 94 248 78 240 66 '
         'C248 54 282 40 282 4 Z')
hourglass = (f'<rect x="184" y="-14" width="112" height="20" rx="6" fill="url(#tk_br)" {K} stroke-width="2.8"/>'
             f'<path d="M190 -14 Q240 -26 290 -14" fill="url(#tk_br)" {K} stroke-width="2.6"/>'
             f'<path d="M206 -8 c8 -4 16 4 24 0 c8 -4 12 4 20 0 c8 -4 16 4 24 0" fill="none" stroke="{BR_D}" stroke-width="2" stroke-linecap="round"/>'
             f'<circle cx="240" cy="-4" r="5" fill="{CY}" {K} stroke-width="2"/>'
             + ''.join(f'<rect x="{x}" y="6" width="9" height="126" rx="3" fill="url(#tk_br)" {K} stroke-width="2.4"/>' for x in (186, 285))
             + f'<path d="{glass}" fill="#dff6ff" opacity=".75"/>'
             + f'<clipPath id="tk_clip"><path d="{glass}"/></clipPath><g clip-path="url(#tk_clip)">'
             f'<g id="tk_sandTop" style="transform-origin:240px 66px"><path d="M190 30 Q240 22 290 30 L290 70 L190 70 Z" fill="url(#tk_sand)"/></g>'
             f'<g id="tk_sandBot" style="transform-origin:240px 132px"><path d="M190 132 L190 118 Q216 92 240 90 Q264 92 290 118 L290 132 Z" fill="url(#tk_sand)"/></g>'
             f'<path d="M240 64 L240 96" stroke="#e8feff" stroke-width="4" stroke-dasharray="5 5" class="fall"/>'
             + ''.join(f'<use href="#tk_star" x="{x}" y="{y}" class="tw" style="animation-delay:-{d}s"/>' for x, y, d in ((222, 40, 0), (258, 46, .8), (230, 112, .4), (254, 106, 1.2)))
             + '</g>'
             f'<path d="{glass}" fill="none" {K} stroke-width="3"/>'
             f'<path d="M208 12 C210 34 222 46 232 56" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".8"/>'
             f'<rect x="184" y="126" width="112" height="16" rx="6" fill="url(#tk_br)" {K} stroke-width="2.8"/>')

# ---- しっぽ（右うしろで まく）----
tail = ''
for i in range(9):
    t = i / 8
    x = 300 + 130 * t - 30 * t * t; y = 300 + 40 * math.sin(t * 2.4) - 70 * t * t
    r = 17 - 11 * t
    tail = (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="url(#tk_br)" {K} stroke-width="2.4"/>'
            f'<path d="M{x - r*.6:.0f} {y:.0f} L{x + r*.6:.0f} {y:.0f}" stroke="{CY}" stroke-width="2" stroke-linecap="round"/>') + tail
tail += f'<path d="M398 232 L412 198 L418 236 Z" fill="url(#tk_sv)" {K} stroke-width="2.4"/>'

# ---- あし（金の よろい＋水色の すじ。つめ3本）----
def leg(hip, knee, ank, foot, m):
    s = ''
    for a, b, w in ((hip, knee, 58), (knee, ank, 46)):
        s += (f'<path d="{P([a, b], False)}" stroke="{L}" stroke-width="{w + 6}" stroke-linecap="round"/>'
              f'<path d="{P([a, b], False)}" stroke="url(#tk_brv)" stroke-width="{w}" stroke-linecap="round"/>'
              f'<path d="{P([a, b], False)}" stroke="{CY}" stroke-width="2.6" stroke-linecap="round" opacity=".9" transform="translate({-9*m} 0)"/>')
    # ももの よろい（大きな板）・ひざ当て
    hx, hy = hip; kx, ky = knee
    s += (f'<path d="M{hx-30} {hy-6} L{hx+30} {hy-6} L{(hx+kx)/2+24:.0f} {(hy+ky)/2+6:.0f} L{(hx+kx)/2-24:.0f} {(hy+ky)/2+6:.0f} Z" fill="url(#tk_br)" {K} stroke-width="2.6"/>'
          f'<path d="M{hx-18} {hy+6} L{hx+18} {hy+6}" stroke="{BR_D}" stroke-width="2.4" stroke-linecap="round"/>')
    s += (f'<path d="M{kx-22} {ky-6} C{kx-22} {ky-26} {kx+22} {ky-26} {kx+22} {ky-6} L{kx+14} {ky+16} L{kx-14} {ky+16} Z" fill="url(#tk_sv)" {K} stroke-width="2.6"/>'
          f'<path d="M{kx} {ky-24} L{kx} {ky+12}" stroke="{SV_D}" stroke-width="2" opacity=".6"/><circle cx="{kx}" cy="{ky-4}" r="6" fill="{CY}" {K} stroke-width="1.6"/>')
    fx, fy = foot
    s += f'<g transform="translate({fx} {fy}) scale(1.3) translate({-fx} {-fy})">'
    s += f'<path d="M{fx-26} {fy-2} C{fx-24} {fy-20} {fx+24} {fy-20} {fx+26} {fy-2} Z" fill="url(#tk_br)" {K} stroke-width="2.6"/>'
    s += ''.join(f'<path d="M{fx+dx} {fy-4} C{fx+dx-2} {fy+6} {fx+dx+2*m} {fy+12} {fx+dx+6} {fy+16} C{fx+dx+8} {fy+8} {fx+dx+8} {fy+2} {fx+dx+7} {fy-4} Z" fill="url(#tk_sv)" {K} stroke-width="2"/>'
                 for dx in (-22, -4, 14)) + '</g>'
    return s
legs = leg((218, 284), (180, 326), (188, 366), (192, 380), -1) + leg((286, 284), (328, 322), (322, 366), (326, 380), 1)

# ---- 胴体（時計の たての うしろ）・こし ----
body = (f'<path d="M196 150 L304 150 L318 230 L300 300 L200 300 L182 230 Z" fill="url(#tk_dk)" {K} stroke-width="3"/>'
        f'<path d="M214 286 L286 286 L276 312 L224 312 Z" fill="url(#tk_br)" {K} stroke-width="2.6"/>'
        f'<path d="M232 300 L268 300" stroke="{CY}" stroke-width="3" stroke-linecap="round"/>')

# ---- 首と 頭（ぎんの 機械の竜。左を向く）----
neck = ''
for i in range(5):
    t = i / 4
    x, y = (252, 150 - 46 * t) if FRONT else (248 - 10 * t, 150 - 36 * t)
    neck += (f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{22 - 3*t:.0f}" ry="{15 - 2*t:.0f}" transform="rotate({-90 if FRONT else -70} {x:.0f} {y:.0f})" fill="url(#tk_sv)" {K} stroke-width="2.4"/>'
             f'<path d="M{x-8:.0f} {y+6:.0f} L{x+6:.0f} {y-8:.0f}" stroke="{CY}" stroke-width="2" stroke-linecap="round" opacity=".8"/>')
def head():
    # 彫りの深い 機械の竜（+x が 鼻先）。まゆは なし：まぶたの骨が 頭の りんかくごと はり出し、その下の くぼみで 目が光る
    s = ''
    # とさかの 刃（うしろへ 3まい）
    for (bx, by), (tx, ty) in (((-8, -12), (-58, -26)), ((4, -22), (-40, -62)), ((20, -26), (2, -74))):
        s += (f'<path d="M{bx-10} {by+6} L{tx} {ty} L{bx+10} {by-2} Z" fill="url(#tk_dk)" {K} stroke-width="2.4"/>'
              f'<path d="M{bx} {by+2} L{(bx+tx)/2:.0f} {(by+ty)/2:.0f}" stroke="{CY}" stroke-width="2" stroke-linecap="round" opacity=".8"/>')
    # 下あご（大きく 開く）
    s += (f'<path d="M2 12 L42 22 L78 28 L76 38 L42 38 L6 28 Z" fill="url(#tk_svd)" {K} stroke-width="2.8"/>'
          f'<path d="M12 26 L42 34 L72 34" fill="none" stroke="{SV_D}" stroke-width="2" opacity=".7"/>')
    # 口の中（水色に 光る）
    s += (f'<path d="M12 12 L46 12 L84 6 L78 26 L44 22 L14 16 Z" fill="#14223a"/>'
          f'<path d="M30 16 L60 16 L74 18" fill="none" stroke="{CY}" stroke-width="4" stroke-linecap="round" opacity=".7" class="glow"/>')
    # 下の歯・きば
    s += ''.join(f'<path d="M{x} {y} l3 -7 l3 7 Z" fill="#fff" {K} stroke-width="1.4"/>' for x, y in ((30, 21), (44, 23), (58, 25)))
    s += f'<path d="M68 27 l3 -13 l4 13 Z" fill="#fff" {K} stroke-width="1.6"/>'
    # 頭（りんかく1つ。目の上で まぶたの骨が 前へ はり出す）
    s += (f'<path d="M-16 6 C-18 -10 -6 -22 10 -27 L32 -30 L58 -18 L54 -8 L64 -13 L82 -10 L90 -2 L86 8 L62 10 L42 12 L18 16 C2 18 -12 14 -16 6 Z" '
          f'fill="url(#tk_sv)" {K} stroke-width="3"/>')
    # 上の歯・きば
    s += ''.join(f'<path d="M{x} 11 l3 8 l3 -8 Z" fill="#fff" {K} stroke-width="1.4"/>' for x in (36, 50, 62))
    s += f'<path d="M74 8 l3 14 l4 -15 Z" fill="#fff" {K} stroke-width="1.8"/>'
    # 目の くぼみ（まぶたの骨の かげ）＋ するどく 光る目（鼻先がわが 下がる つり目）
    s += (f'<path d="M12 -20 L56 -14 L52 -2 L22 -2 L12 -10 Z" fill="url(#tk_sock)"/>'
          f'<path d="M16 -16 L50 -6 C46 -2 38 0 30 -1 C24 -3 19 -8 16 -16 Z" fill="{CY}" opacity=".5" class="glow" transform="translate(-2 0) scale(1.08)"/>'
          f'<path d="M19 -15 L48 -6 C44 -3 37 -2 31 -3 C25 -5 21 -9 19 -15 Z" fill="url(#tk_eye)" {K} stroke-width="1.8"/>'
          f'<path d="M31 -9 L33 -3" stroke="#14223a" stroke-width="2.4" stroke-linecap="round"/>')
    # まぶたの骨の 上の ハイライトと、下の ふかい かげの 線
    s += (f'<path d="M8 -24 L32 -27 L54 -17" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/>'
          f'<path d="M14 -19 L56 -14" stroke="{L}" stroke-width="1.6" stroke-linecap="round" opacity=".6"/>')
    # ほお骨・鼻すじ・板の すじ
    s += (f'<path d="M20 4 L50 0 L66 2" fill="none" stroke="{SV_D}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M62 -14 L84 -6" stroke="{SV_D}" stroke-width="2" opacity=".7"/>'
          f'<path d="M6 -26 L0 8 M58 -6 L58 10" fill="none" stroke="{SV_D}" stroke-width="2" opacity=".6"/>'
          f'<path d="M84 -4 l5 -1" stroke="{L}" stroke-width="2.4" stroke-linecap="round"/>')
    # ほおの 青い宝石
    s += f'<path d="M2 -4 L8 -11 L14 -4 L8 3 Z" fill="url(#tk_gem)" {K} stroke-width="1.8"/>'
    return s
def front_head():
    # 正面の 機械の竜。まゆは なし：ひたいの 骨の板が 目の上へ はり出し（下の ふちが V字）、その下の くぼみで 目が光る
    s = ''
    # とさかの 刃（上へ 5まい、おうぎ形）
    for ang, ln, bx in ((-150, 50, -20), (-122, 62, -10), (-90, 72, 0), (-58, 62, 10), (-30, 50, 20)):
        a = math.radians(ang); tx, ty = bx + ln*math.cos(a), -30 + ln*math.sin(a)
        nx, ny = -math.sin(a) * 9, math.cos(a) * 9
        s += (f'<path d="M{bx+nx:.0f} {-30+ny:.0f} L{tx:.0f} {ty:.0f} L{bx-nx:.0f} {-30-ny:.0f} Z" fill="url(#tk_dk)" {K} stroke-width="2.4"/>'
              f'<path d="M{bx} -32 L{(bx+tx)/2:.0f} {(-30+ty)/2:.0f}" stroke="{CY}" stroke-width="2" stroke-linecap="round" opacity=".85"/>')
    # 耳の ひれ（外へ）
    for m in (1, -1):
        s += f'<path d="M{36*m} -18 L{70*m} -34 L{58*m} -16 L{72*m} -6 L{40*m} 2 Z" fill="url(#tk_svd)" {K} stroke-width="2.4"/>'
    # 下あご（開いた口。V字）
    s += (f'<path d="M-26 14 L-14 44 L0 50 L14 44 L26 14 Z" fill="url(#tk_svd)" {K} stroke-width="2.8"/>'
          f'<path d="M-19 16 L-10 36 L0 40 L10 36 L19 16 Z" fill="#14223a"/>'
          f'<path d="M-9 28 L0 32 L9 28" fill="none" stroke="{CY}" stroke-width="4" stroke-linecap="round" opacity=".7" class="glow"/>'
          + ''.join(f'<path d="M{x} {y} l3 -7 l3 7 Z" fill="#fff" {K} stroke-width="1.4"/>' for x, y in ((-15, 30), (-7, 36), (1, 36), (9, 30)))
          + f'<path d="M-12 46 L0 50 L12 46" fill="none" stroke="{SV_D}" stroke-width="2" opacity=".7"/>')
    # 頭（かどばった りんかく1つ）
    s += (f'<path d="M0 -42 L22 -38 L38 -24 L42 -8 L36 4 L28 14 L18 22 L-18 22 L-28 14 L-36 4 L-42 -8 L-38 -24 L-22 -38 Z" '
          f'fill="url(#tk_sv)" {K} stroke-width="3"/>')
    # 目の くぼみ・光る目（外がわが 上がる つり目）
    for m in (1, -1):
        s += (f'<path d="M{4*m} -8 L{38*m} -14 L{36*m} 0 L{14*m} 4 L{4*m} 0 Z" fill="url(#tk_sock)"/>'
              f'<path d="M{7*m} -3 L{34*m} -11 C{32*m} -4 {24*m} 1 {16*m} 1 C{11*m} 1 {8*m} -1 {7*m} -3 Z" fill="{CY}" opacity=".5" class="glow" transform="scale(1.08)"/>'
              f'<path d="M{8*m} -3 L{33*m} -10 C{31*m} -4 {24*m} 0 {16*m} 0 C{12*m} 0 {9*m} -1 {8*m} -3 Z" fill="url(#tk_eye)" {K} stroke-width="1.8"/>'
              f'<path d="M{20*m} -6 L{19*m} 0" stroke="#14223a" stroke-width="2.4" stroke-linecap="round"/>')
    # ひたいの 骨の板（目の上へ はり出す。下の ふちは V字）
    s += (f'<path d="M-42 -10 L-38 -26 L-20 -34 L20 -34 L38 -26 L42 -10 L12 -12 L0 -5 L-12 -12 Z" fill="url(#tk_sv)" {K} stroke-width="2.8"/>'
          f'<path d="M-34 -24 L-18 -30 L18 -30 L34 -24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity=".75"/>'
          f'<path d="M-40 -9 L-12 -11 L0 -4 L12 -11 L40 -9" fill="none" stroke="#2c3448" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/>')
    # 鼻先の 板・鼻の あな・上の キバ
    s += (f'<path d="M-14 6 L14 6 L18 20 L10 24 L-10 24 L-18 20 Z" fill="url(#tk_svd)" {K} stroke-width="2.2"/>'
          f'<path d="M-7 12 l3 2 M7 12 l-3 2" stroke="{L}" stroke-width="2.4" stroke-linecap="round"/>'
          f'<path d="M-15 21 L-11 34 L-7 23 Z M7 23 L11 34 L15 21 Z" fill="#fff" {K} stroke-width="1.8"/>')
    # ほお骨・ほおの 宝石・ひたいの 宝石
    s += (f'<path d="M-36 4 L-22 10 M36 4 L22 10" stroke="{SV_D}" stroke-width="2.2" stroke-linecap="round"/>'
          + ''.join(f'<path d="M{30*m-5} 8 L{30*m} 2 L{30*m+5} 8 L{30*m} 14 Z" fill="url(#tk_gem)" {K} stroke-width="1.6"/>' for m in (1, -1))
          + f'<path d="M0 -40 L7 -32 L0 -24 L-7 -32 Z" fill="url(#tk_gem)" {K} stroke-width="1.8"/>'
          + f'<path d="M-2 -36 l3 -3" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>')
    return s

headg = f'<g class="hd" style="transform-origin:246px 150px"><g transform="translate(238 106) scale(-1.42 1.42) rotate(4)">{head()}</g></g>'
if FRONT:
    headg = f'<g class="hd" style="transform-origin:252px 130px"><g transform="translate(252 72) scale(1.5)">{front_head()}</g></g>'

# ---- うで（筋肉質だけど 細く シャープに）----
def limb(a, b, w0, wm, w1, bul=1, fill='url(#tk_brv)'):
    # a→b の うで。bul がわに 力こぶ（ふくらみ）、反対がわは まっすぐ
    dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy); nx, ny = -dy / l * bul, dx / l * bul
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    A1, B1 = (a[0] + nx*w0/2, a[1] + ny*w0/2), (b[0] + nx*w1/2, b[1] + ny*w1/2)
    A2, B2 = (a[0] - nx*w0/2, a[1] - ny*w0/2), (b[0] - nx*w1/2, b[1] - ny*w1/2)
    M1 = (mx + nx*wm*.75, my + ny*wm*.75); M2 = (mx - nx*(w0+w1)/4, my - ny*(w0+w1)/4)
    d = (f'M{A1[0]:.0f} {A1[1]:.0f} Q{M1[0]:.0f} {M1[1]:.0f} {B1[0]:.0f} {B1[1]:.0f} L{B2[0]:.0f} {B2[1]:.0f} '
         f'Q{M2[0]:.0f} {M2[1]:.0f} {A2[0]:.0f} {A2[1]:.0f} Z')
    mus = f'M{a[0] + dx*.25 + nx*w0*.15:.0f} {a[1] + dy*.25 + ny*w0*.15:.0f} Q{mx + nx*wm*.35:.0f} {my + ny*wm*.35:.0f} {a[0] + dx*.8 + nx*w1*.1:.0f} {a[1] + dy*.8 + ny*w1*.1:.0f}'
    return (f'<path d="{d}" fill="{fill}" {K} stroke-width="2.8"/>'
            f'<path d="{mus}" fill="none" stroke="{BR_D}" stroke-width="2.2" stroke-linecap="round" opacity=".8"/>'
            f'<path d="M{A2[0]*.8 + B2[0]*.2:.0f} {A2[1]*.8 + B2[1]*.2:.0f} L{A2[0]*.2 + B2[0]*.8:.0f} {A2[1]*.2 + B2[1]*.8:.0f}" stroke="{CY}" stroke-width="2.4" stroke-linecap="round" opacity=".9"/>')
def elbow_spike(x, y, tx, ty):
    return (f'<path d="M{x-8} {y-6} L{tx} {ty} L{x+8} {y+6} Z" fill="url(#tk_blade)" {K} stroke-width="2.2"/>'
            f'<circle cx="{x}" cy="{y}" r="8" fill="url(#tk_sv)" {K} stroke-width="2.2"/><circle cx="{x}" cy="{y}" r="3" fill="{CY}"/>')
def claws(pts):
    return ''.join(f'<path d="M{x} {y} C{x+2} {y+12} {x-2} {y+20} {x-8} {y+27} C{x+3} {y+25} {x+10} {y+16} {x+9} {y+1} Z" fill="url(#tk_sv)" {K} stroke-width="2"/>'
                   for x, y in pts)
armR = (limb((346, 196), (380, 238), 24, 30, 17, bul=-1)
        + elbow_spike(380, 238, 408, 222)
        # こて（細く とがった 真ちゅう）
        + f'<path d="M370 240 L392 238 L400 276 L394 290 L376 292 L368 270 Z" fill="url(#tk_br)" {K} stroke-width="2.6"/>'
        + f'<path d="M392 240 L410 262 L398 270 Z" fill="url(#tk_blade)" {K} stroke-width="2"/>'
        + f'<path d="M378 250 L386 284" stroke="{CY}" stroke-width="2.6" stroke-linecap="round"/>'
        + f'<path d="M386 256 l6 -6 l5 7 l-6 7 Z" fill="url(#tk_gem)" {K} stroke-width="1.6"/>'
        + claws(((372, 290), (384, 292), (396, 288))))
# かま（砂時計の いしづき・下へ そる大きな刃・上へ トゲ）
staff = (f'<path d="M30 344 L204 228" stroke="{L}" stroke-width="14" stroke-linecap="round"/>'
         f'<path d="M30 344 L204 228" stroke="url(#tk_sv)" stroke-width="8" stroke-linecap="round"/>'
         f'<path d="M36 340 L198 232" stroke="{CY}" stroke-width="2" stroke-linecap="round" opacity=".7"/>'
         # 大きな刃
         f'<path d="M80 312 C56 326 40 356 40 396 C30 362 34 328 58 306 Z" fill="url(#tk_blade)" {K} stroke-width="2.8"/>'
         f'<path d="M74 316 C58 332 48 354 44 378" fill="none" stroke="{CY}" stroke-width="2.4" stroke-linecap="round"/>'
         # 上の トゲ2本
         f'<path d="M72 316 L52 262 L86 306 Z M94 302 L86 250 L106 294 Z" fill="url(#tk_blade)" {K} stroke-width="2.4"/>'
         f'<rect x="68" y="302" width="36" height="12" rx="4" transform="rotate(-33 86 308)" fill="url(#tk_br)" {K} stroke-width="2.4"/>'
         # いしづきの 小さな 砂時計
         f'<g transform="translate(24 348) rotate(-33) scale(1.25)"><rect x="-18" y="-16" width="8" height="32" rx="3" fill="url(#tk_br)" {K} stroke-width="2.2"/>'
         f'<rect x="10" y="-16" width="8" height="32" rx="3" fill="url(#tk_br)" {K} stroke-width="2.2"/>'
         f'<path d="M-10 -11 C2 -11 -4 0 0 0 C-4 0 2 11 -10 11 L10 11 C-2 11 4 0 0 0 C4 0 -2 -11 10 -11 Z" transform="rotate(90)" fill="#a8e8ff" {K} stroke-width="2"/></g>')
armL = (limb((208, 198), (182, 238), 24, 30, 17, bul=-1)
        + limb((182, 238), (160, 250), 18, 18, 18, bul=1, fill='url(#tk_br)')
        + elbow_spike(182, 238, 196, 270)
        # 手（かまの 柄を にぎる。つめ3本）
        + f'<path d="M146 240 L170 236 L176 252 L164 262 L148 260 Z" fill="url(#tk_sv)" {K} stroke-width="2.4"/>'
        + claws(((148, 256), (158, 260), (168, 258))))

# ---- 大きな 肩よろい（3まい重ね＋トゲ3本＋宝石）----
def pauldron(cx, cy, m, sc):
    # かどばった 肩よろい：外がわ（+x）へ はり出して 下がる 重ね板。上の ふちに トゲ3本
    g = ''
    for bx, by, tx, ty in ((-22, -30, -30, -78), (6, -38, 8, -92), (34, -32, 52, -76)):
        g += (f'<path d="M{bx-12} {by+4} L{tx} {ty} L{bx+12} {by-2} Z" fill="url(#tk_blade)" {K} stroke-width="2.4"/>'
              f'<path d="M{bx} {by} L{(bx+tx)/2:.0f} {(by+ty)/2:.0f}" stroke="{CY}" stroke-width="2" stroke-linecap="round" opacity=".85"/>')
    # 下の 板（2まい）
    g += (f'<path d="M-26 40 L24 44 L70 60 L80 82 L62 80 L22 66 L-20 60 Z" fill="url(#tk_br)" {K} stroke-width="2.6"/>'
          f'<path d="M-34 22 L26 26 L76 40 L88 64 L68 62 L24 48 L-28 44 Z" fill="url(#tk_sv)" {K} stroke-width="2.6"/>'
          f'<path d="M-20 34 L24 37 L74 51" fill="none" stroke="{SV_D}" stroke-width="2" opacity=".6"/>')
    # 上の 大きな 板
    g += (f'<path d="M-44 20 L-38 -20 L-10 -40 L36 -42 L76 -20 L94 18 L96 46 L70 34 L26 26 L-30 28 Z" fill="url(#tk_br)" {K} stroke-width="3.2"/>'
          f'<path d="M-36 -16 L-10 -34 L34 -36 L70 -16" fill="none" stroke="{BR_L}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
          f'<path d="M-36 16 L26 18 L72 28 L90 40" fill="none" stroke="{CY}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="M36 -42 L44 26 M76 -20 L78 30" stroke="{BR_D}" stroke-width="2.2" opacity=".7"/>'
          f'<path d="M4 -16 l13 -14 l13 14 l-13 16 Z" fill="url(#tk_gem)" {K} stroke-width="2.2"/>'
          f'<path d="M11 -17 l6 -7" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/>'
          + ''.join(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{BR_L}" {K} stroke-width="1.4"/>' for x, y in ((-30, 4), (58, -6), (84, 22))))
    return f'<g transform="translate({cx} {cy}) scale({m*sc} {sc})">{g}</g>'
pauldrons = pauldron(352, 188, 1, .7) + pauldron(160, 204, -1, .62)

# ---- むねの 時計の たて（1〜12・中で 歯車が回る・はりが まわる）----
CX, CYY, R = 252, 214, 86
clock = (f'<circle cx="{CX}" cy="{CYY}" r="{R}" fill="url(#tk_br)" {K} stroke-width="3.4"/>'
         f'<circle cx="{CX}" cy="{CYY}" r="{R-8}" fill="none" stroke="{BR_D}" stroke-width="2"/>'
         + ''.join(f'<path d="M{CX + (R-4)*math.cos(math.radians(a)):.0f} {CYY + (R-4)*math.sin(math.radians(a)):.0f} '
                   f'l{8*math.cos(math.radians(a+90)):.1f} {8*math.sin(math.radians(a+90)):.1f}" stroke="{BR_L}" stroke-width="3" stroke-linecap="round"/>'
                   for a in range(0, 360, 20))
         + ''.join(f'<path d="M{x} {y-11} L{x+8} {y} L{x} {y+11} L{x-8} {y} Z" fill="url(#tk_gem)" {K} stroke-width="2"/>'
                   for x, y in ((CX, CYY - R + 2), (CX, CYY + R - 2), (CX - R + 2, CYY), (CX + R - 2, CYY)))
         + f'<circle cx="{CX}" cy="{CYY}" r="{R-16}" fill="url(#tk_face)" {K} stroke-width="2.8"/>')
for k in range(12):
    a = math.radians(k * 30 - 60)
    x, y = CX + (R - 30) * math.cos(a), CYY + (R - 30) * math.sin(a)
    clock += f'<text x="{x:.1f}" y="{y + 5.5:.1f}" text-anchor="middle" font-family="sans-serif" font-weight="900" font-size="15" fill="{L}">{k + 1}</text>'
clock += ''.join(f'<path d="M{CX + (R-17)*math.cos(math.radians(a)):.0f} {CYY + (R-17)*math.sin(math.radians(a)):.0f} L{CX + (R-21)*math.cos(math.radians(a)):.0f} {CYY + (R-21)*math.sin(math.radians(a)):.0f}" stroke="{L}" stroke-width="1.6"/>'
                 for a in range(0, 360, 6) if a % 30)
# 中の まど（歯車が 見える）
clock += (f'<clipPath id="tk_win"><circle cx="{CX}" cy="{CYY}" r="40"/></clipPath>'
          f'<circle cx="{CX}" cy="{CYY}" r="40" fill="#3a4660"/>'
          f'<g clip-path="url(#tk_win)">{gear(CX - 12, CYY - 8, 20, 10, "gR")}{gear(CX + 20, CYY + 14, 15, 8, "gL", delay=.5)}{gear(CX - 10, CYY + 26, 12, 8, "gR", delay=1.3)}</g>'
          f'<circle cx="{CX}" cy="{CYY}" r="40" fill="none" {K} stroke-width="2.6"/>')
# はり（長い はり・短い はり。くるくる まわる＝時を 食う）
clock += (f'<g class="hL" style="transform-origin:{CX}px {CYY}px"><path d="M{CX} {CYY + 8} L{CX - 4} {CYY} L{CX} {CYY - 60} L{CX + 4} {CYY} Z" fill="{CY}" {K} stroke-width="2"/></g>'
          f'<g class="hS" style="transform-origin:{CX}px {CYY}px"><path d="M{CX - 6} {CYY + 6} L{CX - 5} {CYY - 2} L{CX + 34} {CYY - 30} L{CX + 4} {CYY + 4} Z" fill="{CY}" {K} stroke-width="2"/></g>'
          f'<circle cx="{CX}" cy="{CYY}" r="7" fill="url(#tk_br)" {K} stroke-width="2"/>')

# ---- うかぶ 歯車・砂つぶ ----
floats = (gear(36, 60, 12, 8, 'gR', delay=.3) + gear(452, 30, 11, 8, 'gL', delay=.8) + gear(30, 300, 10, 8, 'gL')
          + gear(456, 330, 13, 8, 'gR', delay=1.1) + gear(118, 400, 9, 8, 'gR', delay=.6))
dust = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" class="dust" style="animation-delay:-{d}s"/>'
               for x, y, r, c, d in ((70, 150, 3, CY, 0), (420, 200, 2.6, '#d8b866', .8), (60, 230, 2.2, '#d8b866', 1.5),
                                     (440, 270, 3, CY, 2.1), (150, 30, 2.4, CY, 1.1), (330, 400, 2.4, '#d8b866', .4), (400, 380, 2, CY, 1.8)))

style = '''<style>
  .tkk{stroke:#2b2b3a;stroke-linejoin:round;stroke-linecap:round}
  .breathe{transform-origin:240px 400px;animation:br 3.6s ease-in-out infinite}
  @keyframes br{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
  .vx{animation:vx 14s linear infinite}
  @keyframes vx{to{transform:rotate(-360deg)}}
  .gR{animation:gr 6s linear infinite}.gL{animation:gr 6s linear infinite reverse}
  @keyframes gr{to{transform:rotate(360deg)}}
  .hL{animation:gr 3s linear infinite}.hS{animation:gr 36s linear infinite}
  .fall{animation:fa .6s linear infinite}
  @keyframes fa{to{stroke-dashoffset:-10}}
  .hd{animation:hd 3.6s ease-in-out infinite}
  @keyframes hd{0%,100%{transform:rotate(0)}50%{transform:rotate(3deg)}}
  .glow{animation:gw 2s ease-in-out infinite}
  @keyframes gw{0%,100%{opacity:.25}50%{opacity:.8}}
  .tw{animation:tw 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}
  @keyframes tw{0%,100%{opacity:.2}50%{opacity:1}}
  .dust{animation:du 4s ease-in-out infinite}
  @keyframes du{0%,100%{opacity:0;transform:translateY(10px)}50%{opacity:.9;transform:translateY(-10px)}}
</style>'''

defs = f'''<defs>
  <radialGradient id="tk_bg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#e6f8ff"/><stop offset=".65" stop-color="#bfe6fb" stop-opacity=".45"/><stop offset="1" stop-color="#bfe6fb" stop-opacity="0"/></radialGradient>
  <linearGradient id="tk_br" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BR_L}"/><stop offset=".55" stop-color="{BR}"/><stop offset="1" stop-color="{BR_D}"/></linearGradient>
  <linearGradient id="tk_brv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BR_L}"/><stop offset="1" stop-color="{BR_D}"/></linearGradient>
  <linearGradient id="tk_sv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SV_L}"/><stop offset=".6" stop-color="{SV}"/><stop offset="1" stop-color="{SV_D}"/></linearGradient>
  <linearGradient id="tk_svd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SV}"/><stop offset="1" stop-color="{SV_D}"/></linearGradient>
  <linearGradient id="tk_dk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d8aa0"/><stop offset="1" stop-color="#454f63"/></linearGradient>
  <linearGradient id="tk_blade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f6f9fc"/><stop offset="1" stop-color="#8e9db2"/></linearGradient>
  <radialGradient id="tk_face" cx=".45" cy=".4" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d6dfe9"/></radialGradient>
  <linearGradient id="tk_sand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9f8ff"/><stop offset="1" stop-color="#3fb4f2"/></linearGradient>
  <linearGradient id="tk_gem" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8ecff"/><stop offset="1" stop-color="{BL}"/></linearGradient>
  <linearGradient id="tk_sock" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2232"/><stop offset="1" stop-color="#5a6680"/></linearGradient>
  <radialGradient id="tk_eye" cx=".4" cy=".4" r=".7"><stop offset="0" stop-color="#f2ffff"/><stop offset="1" stop-color="{CY}"/></radialGradient>
  <path id="tk_star" d="M0 -6 L1.5 -1.5 L6 0 L1.5 1.5 L0 6 L-1.5 1.5 L-6 0 L-1.5 -1.5 Z" fill="#fff"/>
</defs>'''

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 480 444" width="480" height="444" overflow="hidden">\n'
       f'<title>うらボス トキクイ</title>\n{style}\n{defs}\n'
       f'<circle cx="240" cy="206" r="240" fill="url(#tk_bg)"/>\n{vortex}\n{floats}{dust}\n'
       f'<g class="breathe"><g transform="translate(240 222) scale(1.08) translate(-240 -214)">{wingL}{wingR}{hourglass}{tail}{legs}{body}{armR}{neck}{staff}{armL}{clock}{pauldrons}{headg}</g></g>\n</svg>\n')
open(sys.argv[1] if len(sys.argv) > 1 else 'tokikui.svg', 'w').write(svg)
