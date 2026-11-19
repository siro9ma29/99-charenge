import math, sys
# さばくの ぬし しんの すがた（金のよろいの 大さそり）— ななめ前向き（参考画像のアングル）
# 8の段の ひみつの かず＝脚 8本（手前4本＋おく4本）。ほかのパーツは8にしない
#   しっぽの節5つ＋毒針1・ハサミの歯3つずつ・ハサミのトゲ2本ずつ・背中の板4まい・きば2本・ピラミッド2つ
L = '#2b2b3a'
AR = f'stroke="{L}" stroke-width="3" stroke-linejoin="round"'
def mir(s): return f'<g transform="translate(480 0) scale(-1 1)">{s}</g>'
def hl(d, w=2.4, op=.85): return f'<path d="{d}" fill="none" stroke="#fff6d0" stroke-width="{w}" stroke-linecap="round" opacity="{op}"/>'
def eng(d, w=2): return f'<path d="{d}" fill="none" stroke="#b9772a" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity=".8"/>'
def P(pts): return 'M' + ' L'.join(f'{x} {y}' for x, y in pts)

# ---- 脚 ----
def leg(pts, w, far=False):
    col, hi, gd = ('#c98e34', '#e8b85a', 'url(#gf8)') if far else ('#e9aa3c', '#ffe48a', 'url(#gd8)')
    s = ''
    tx, ty = pts[-1]; ax, ay = pts[-2]
    ang = math.atan2(ty - ay, tx - ax); nx, ny = -math.sin(ang), math.cos(ang)
    bx, by = tx - math.cos(ang) * 4, ty - math.sin(ang) * 4
    s += (f'<path d="{P(pts)}" fill="none" stroke="{L}" stroke-width="{w+6}" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="{P(pts)}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
          f'<path d="{P(pts[:-1])}" fill="none" stroke="{hi}" stroke-width="{w*.32:.1f}" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')
    s += (f'<path d="M{bx+nx*w*.55:.1f} {by+ny*w*.55:.1f} L{tx+math.cos(ang)*15:.1f} {ty+math.sin(ang)*15:.1f} '
          f'L{bx-nx*w*.55:.1f} {by-ny*w*.55:.1f} Z" fill="url(#br8)" {AR}/>')
    # もも（つけね側）は 太いよろい
    s += (f'<path d="{P(pts[:2])}" fill="none" stroke="{L}" stroke-width="{w*1.25+6:.1f}" stroke-linecap="round"/>'
          f'<path d="{P(pts[:2])}" fill="none" stroke="{gd}" stroke-width="{w*1.25:.1f}" stroke-linecap="round"/>')
    for (x, y), r in zip(pts[1:-1], (w*.55, w*.45)):
        s += f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="url(#br8)" stroke="{L}" stroke-width="2.4"/>'
    return s
legsNear = (leg([(290, 290), (302, 334), (292, 378), (286, 408)], 18)
            + leg([(330, 286), (354, 328), (350, 374), (348, 406)], 17)
            + leg([(370, 278), (402, 318), (408, 366), (414, 400)], 16)
            + leg([(408, 266), (442, 302), (456, 350), (464, 386)], 15))
legsFar = (leg([(296, 200), (306, 150), (320, 370)], 13, True)
           + leg([(334, 196), (346, 146), (382, 366)], 12.5, True)
           + leg([(372, 192), (386, 144), (436, 358)], 12, True)
           + leg([(408, 188), (424, 146), (466, 334)], 11.5, True))

# ---- ハサミ（左向き。歯3つ・こうのトゲ2本）----
claw_d = ('M200 -34 C172 -48 132 -48 112 -36 C80 -42 40 -36 4 -14 C40 -20 76 -16 98 -2 '
          'C72 6 36 12 0 22 C36 42 80 48 112 38 C140 50 176 48 200 34 Z')
def claw(far=False):
    gd = 'url(#gf8)' if far else 'url(#gd8)'
    teeth = ''.join(f'<path d="M{x} {y} l{dx} {dy} l{ex} {ey} Z" fill="#fff6d0" stroke="{L}" stroke-width="1.8" stroke-linejoin="round"/>'
                    for x, y, dx, dy, ex, ey in [(60, -20, 4, 9, 6, -10), (36, 14, 4, -9, 7, 7), (72, 7, 4, -9, 7, 6)])
    spikes = ''.join(f'<path d="M{x-9} -42 L{x+4} -66 L{x+10} -44 Z" fill="url(#br8)" {AR}/>' for x in (140, 172))
    return (spikes + f'<path d="{claw_d}" fill="{gd}" stroke="{L}" stroke-width="3.4" stroke-linejoin="round"/>'
            + f'<path d="M116 -30 C140 -36 176 -36 196 -24 L196 24 C176 38 140 40 116 30 C108 10 108 -10 116 -30 Z" fill="url(#br8)" opacity=".35"/>'
            + f'<path d="M116 -32 C108 -10 108 12 116 34" fill="none" stroke="{L}" stroke-width="2.6" stroke-linecap="round"/>'
            + eng('M132 -4 c6 -10 18 -10 22 0 c4 10 16 10 22 0') + eng('M134 14 L180 14', 1.6)
            + teeth + hl('M104 -38 C72 -40 40 -32 16 -18') + hl('M120 -36 C150 -42 178 -40 196 -30', 2)
            + f'<path d="M150 -2 L160 -12 L170 -2 L160 8 Z" fill="url(#tq8)" stroke="{L}" stroke-width="2.2" stroke-linejoin="round"/>')
def arm(pts, w):
    return (f'<path d="{P(pts)}" fill="none" stroke="{L}" stroke-width="{w+7}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{P(pts)}" fill="none" stroke="#e9aa3c" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{P(pts[:2])}" fill="none" stroke="#ffe48a" stroke-width="{w*.3:.1f}" stroke-linecap="round" opacity=".9"/>'
            f'<circle cx="{pts[1][0]}" cy="{pts[1][1]}" r="{w*.6:.1f}" fill="url(#br8)" stroke="{L}" stroke-width="2.8"/>')
clawFar = (arm([(236, 196), (232, 128), (182, 114)], 20)
           + f'<g transform="translate(30 112) scale(.74)"><g class="snap">{claw(True)}</g></g>')
clawNear = (arm([(240, 288), (310, 330), (256, 364)], 26)
            + f'<g transform="translate(40 364) scale(1.02)"><g class="snap d1">{claw()}</g></g>')

# ---- しっぽ（節5つ＋毒針）。背中の うしろから 立ち上がり、前へ 巻いて 毒針を かまえる ----
def bez(t, p):
    a, b, c, d = p; u = 1 - t
    return (u**3*a[0] + 3*u*u*t*b[0] + 3*u*t*t*c[0] + t**3*d[0], u**3*a[1] + 3*u*u*t*b[1] + 3*u*t*t*c[1] + t**3*d[1])
TP = [(420, 214), (488, 150), (462, 6), (352, 34)]
def seg(t, w, ln):
    x, y = bez(t, TP); x2, y2 = bez(t + .01, TP)
    a = math.degrees(math.atan2(y2 - y, x2 - x)); h = ln / 2; r = w / 2
    body = (f'M{-h} {-r+5} Q{-h} {-r} {-h+7} {-r} L{h-7} {-r} Q{h} {-r} {h} {-r+5} '
            f'L{h} {r-5} Q{h} {r} {h-7} {r} L{-h+7} {r} Q{-h} {r} {-h} {r-5} Z')
    sp = f'M{-h*.3:.1f} {-r+1} L{h*.15:.1f} {-r-12} L{h*.5:.1f} {-r+1} Z'
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({a:.1f})">'
            f'<path d="{sp}" fill="url(#br8)" {AR}/>'
            f'<path d="{body}" fill="url(#gd8)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>'
            f'<path d="M{-h+5} {-r+7} L{-h+5} {r-7}" stroke="#b9772a" stroke-width="5" stroke-linecap="round"/>'
            + eng(f'M{-h+14} {r*.35:.1f} c5 -7 11 -7 14 0 c3 7 9 7 14 0', 1.8) +
            f'<path d="M{-h+12} {-r*.5:.1f} L{h-8} {-r*.5:.1f}" stroke="#fff6d0" stroke-width="2.6" stroke-linecap="round" opacity=".85"/>'
            f'</g>')
segs = ''.join(seg(t, w, ln) for t, w, ln in [(.10, 42, 54), (.26, 41, 54), (.42, 40, 52), (.58, 38, 50), (.73, 36, 46)])
ex, ey = bez(.86, TP); fx, fy = bez(.87, TP)
ea = math.degrees(math.atan2(fy - ey, fx - ex))
stinger = (f'<g transform="translate({ex:.1f} {ey:.1f}) rotate({ea:.1f}) scale(1 -1)">'
           f'<ellipse cx="22" cy="0" rx="28" ry="21" fill="url(#gd8)" stroke="{L}" stroke-width="3.2"/>'
           + eng('M8 6 c6 -8 14 -8 18 0 c4 8 12 8 18 0', 1.8) +
           f'<path d="M6 -10 Q22 -18 40 -10" fill="none" stroke="#fff6d0" stroke-width="2.6" stroke-linecap="round" opacity=".9"/>'
           f'<circle cx="72" cy="44" r="26" fill="#ffd24a" opacity=".6" filter="url(#soft)" class="glow"/>'
           f'<path d="M40 -12 C62 0 78 22 84 64 C70 40 56 24 40 14 Z" fill="url(#br8)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>'
           f'<path d="M50 -2 C64 10 74 26 78 46" fill="none" stroke="#ffd37a" stroke-width="2.4" stroke-linecap="round" opacity=".9"/>'
           f'<circle cx="83" cy="60" r="4" fill="#fffbd0" class="glow"/>'
           f'</g>')
tail = segs + stinger

# ---- 体：むねの こうら＋背中の板4まい（右おくへ 小さくなる）----
plates = ''
for cx, cy, a, b in [(420, 222, 24, 52), (386, 226, 26, 58), (350, 230, 28, 64), (312, 234, 30, 70)]:
    plates += (f'<path d="M{cx-a} {cy-b+12} Q{cx} {cy-b-8} {cx+a} {cy-b+12} L{cx+a+2} {cy+b-14} Q{cx} {cy+b+4} {cx-a+2} {cy+b-14} Z" '
               f'fill="url(#gd8)" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>'
               + eng(f'M{cx-a*.55:.1f} {cy+6} c{a*.25:.1f} -9 {a*.55:.1f} -9 {a*.55:.1f} 0 c0 9 {a*.3:.1f} 9 {a*.55:.1f} 0')
               + eng(f'M{cx-a*.6:.1f} {cy-b*.35:.1f} L{cx+a*.6:.1f} {cy-b*.35:.1f}', 1.6)
               + hl(f'M{cx-a+8} {cy-b+10} Q{cx} {cy-b-2} {cx+a-8} {cy-b+10}', 2.2))
shell = (f'<path d="M200 180 C220 150 270 146 292 170 C306 196 306 262 294 292 C276 310 230 312 212 296 C194 270 190 220 200 180 Z" '
         f'fill="url(#br8)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>')
belly = f'<path d="M264 292 C320 302 380 292 440 262 L442 244 C380 274 320 286 268 276 Z" fill="url(#br8)" {AR}/>'
body = belly + plates + shell

# ---- 頭（ななめ前向き。ファラオの かぶとのような こうら・つり目）----
head_d = ('M240 86 L256 106 C284 108 310 116 326 132 L352 146 L334 160 C338 178 332 196 318 208 '
          'C304 226 280 240 240 244 C200 240 176 226 162 208 C148 196 142 178 146 160 L128 146 L154 132 '
          'C170 116 196 108 224 106 Z')
face_d = ('M240 144 Q282 144 312 158 L316 176 Q312 198 296 212 L272 232 Q256 240 240 240 '
          'Q224 240 208 232 L184 212 Q168 198 164 176 L168 158 Q198 144 240 144 Z')
def eye(cx, cy, side, id_):
    if side < 0:
        clip = f'M{cx-24} {cy-20} L{cx+24} {cy-2} L{cx+24} {cy+26} L{cx-24} {cy+26} Z'; lid = f'M{cx-19} {cy-17} L{cx+21} {cy-2}'
    else:
        clip = f'M{cx-24} {cy-2} L{cx+24} {cy-20} L{cx+24} {cy+26} L{cx-24} {cy+26} Z'; lid = f'M{cx+19} {cy-17} L{cx-21} {cy-2}'
    hx = -5 if side < 0 else 5
    return (f'<clipPath id="{id_}"><path d="{clip}"/></clipPath><g clip-path="url(#{id_})">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="15" ry="16" fill="#fff" stroke="{L}" stroke-width="2.6"/>'
            f'<ellipse cx="{cx-4}" cy="{cy+2}" rx="11" ry="13" fill="url(#tq8)"/>'
            f'<ellipse cx="{cx-5}" cy="{cy+3}" rx="5.5" ry="8" fill="#123040"/>'
            f'<circle cx="{cx+hx-4}" cy="{cy-3}" r="3.8" fill="#fff"/><circle cx="{cx-hx*.6-4}" cy="{cy+7}" r="1.8" fill="#fff"/></g>'
            f'<path d="{lid}" stroke="{L}" stroke-width="4" stroke-linecap="round"/>')
head = f'''
<path d="{head_d}" fill="url(#gd8)" stroke="{L}" stroke-width="3.6" stroke-linejoin="round"/>
<path d="M150 146 L128 146 L154 132 C170 116 196 108 224 106 L240 86 L256 106 C284 108 310 116 326 132 L352 146 L330 146 C306 130 276 122 240 122 C204 122 174 130 150 146 Z" fill="url(#br8)" opacity=".5"/>
{eng('M178 132 c10 -8 22 -8 26 0')}{eng('M302 132 c-10 -8 -22 -8 -26 0')}
{hl('M170 128 C190 116 210 112 226 112')}{hl('M310 128 C290 116 270 112 254 112')}
<path d="{face_d}" fill="#fff0c0" stroke="{L}" stroke-width="2.8" stroke-linejoin="round"/>
<path d="M240 104 L254 124 L240 146 L226 124 Z" fill="#2fd0c4" opacity=".6" filter="url(#soft)" class="glow"/>
<path d="M240 104 L254 124 L240 146 L226 124 Z" fill="url(#tq8)" stroke="{L}" stroke-width="2.8" stroke-linejoin="round"/>
<path d="M240 106 L240 144 L227 124 Z" fill="#fff" opacity=".45"/>
{eye(208,178,-1,'e8L')}{eye(272,178,1,'e8R')}
<path d="M216 206 Q238 200 260 206 Q256 228 238 230 Q220 228 216 206 Z" fill="#7a2a20" stroke="{L}" stroke-width="2.8" stroke-linejoin="round"/>
<ellipse cx="238" cy="222" rx="10" ry="5" fill="#ff8a6a"/>
<path d="M222 207 L227 220 L233 205 Z M254 207 L249 220 L243 205 Z" fill="#fff" stroke="{L}" stroke-width="2" stroke-linejoin="round"/>
'''
headG = f'<g transform="translate(160 234) rotate(-6) scale(.95) translate(-240 -170)">{head}</g>'

# ---- 背景 ----
dunes = (f'<path d="M-10 344 C60 320 140 326 200 346 C260 366 340 316 490 334 L490 430 L-10 430 Z" fill="#f6cf7a" opacity=".55"/>'
         f'<path d="M-10 392 C80 376 160 384 240 396 C320 408 400 380 490 388 L490 430 L-10 430 Z" fill="#efbb5a" opacity=".6"/>')
pyramids = (f'<path d="M150 336 L186 290 L222 336 Z" fill="#e8b458" opacity=".5"/><path d="M186 290 L222 336 L198 336 Z" fill="#c98a30" opacity=".4"/>'
            f'<path d="M196 332 L218 304 L240 332 Z" fill="#e8b458" opacity=".45"/>')
sand = ''.join(f'<g class="rise {d}"><circle cx="{x}" cy="{y}" r="{r}" fill="#e0a040" opacity=".8"/></g>'
               for x, y, r, d in [(40, 400, 3, ''), (110, 410, 2.5, 'd1'), (200, 414, 2, 'd2'), (290, 414, 3, 'd3'),
                                  (370, 410, 2.5, ''), (446, 402, 2, 'd2'), (150, 404, 2, 'd3')])
wind = (f'<path d="M14 412 q40 -12 80 0 t80 0 M320 414 q40 -12 80 0 t70 0" fill="none" stroke="#d9a032" stroke-width="3" '
        f'stroke-linecap="round" opacity=".7"/>')
sp = ''.join(f'<use href="#sp" x="{x}" y="{y}" class="tw {d}"/>' for x, y, d in [(40, 30, ''), (240, 40, 'd1'), (24, 250, 'd2'), (440, 280, 'd3')])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 480 444" width="480" height="444">
<title>さばくの ぬし しんの すがた</title>
<style>
  .breathe{{transform-origin:340px 300px;animation:br 3.2s ease-in-out infinite}}
  @keyframes br{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.012,1.022)}}}}
  .sway{{transform-origin:200px 290px;animation:sw 4s ease-in-out infinite}}
  @keyframes sw{{0%,100%{{transform:rotate(-1.4deg)}}50%{{transform:rotate(1.4deg)}}}}
  .wag{{transform-origin:420px 214px;animation:wg 2.6s ease-in-out infinite}}
  @keyframes wg{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-3deg)}}}}
  .snap{{transform-box:fill-box;transform-origin:100% 50%;animation:sn 2.4s ease-in-out infinite}}
  @keyframes sn{{0%,70%,100%{{transform:rotate(0)}}80%{{transform:rotate(5deg)}}90%{{transform:rotate(-2deg)}}}}
  .glow{{animation:gl 2.4s ease-in-out infinite}}
  @keyframes gl{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}
  .tw{{animation:tw 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
  @keyframes tw{{0%,100%{{opacity:0;transform:scale(.4)}}50%{{opacity:1;transform:scale(1)}}}}
  .rise{{animation:rs 3.6s linear infinite}}
  @keyframes rs{{0%{{transform:translate(0,0);opacity:0}}15%{{opacity:1}}100%{{transform:translate(30px,-110px);opacity:0}}}}
  .d1{{animation-delay:.9s}}.d2{{animation-delay:1.8s}}.d3{{animation-delay:2.7s}}
</style>
<defs>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
  <path id="sp" d="M0 -6 L1.5 -1.5 L6 0 L1.5 1.5 L0 6 L-1.5 1.5 L-6 0 L-1.5 -1.5 Z" fill="#fffbd0"/>
  <radialGradient id="bg" cx="50%" cy="50%" r="55%"><stop offset="0" stop-color="#ffe2a0"/><stop offset=".6" stop-color="#ffe2a0" stop-opacity=".5"/><stop offset="1" stop-color="#ffe2a0" stop-opacity="0"/></radialGradient>
  <linearGradient id="gd8" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe88c"/><stop offset=".55" stop-color="#f4bf4a"/><stop offset="1" stop-color="#d8952c"/></linearGradient>
  <linearGradient id="gf8" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0cc6a"/><stop offset=".55" stop-color="#d9a23c"/><stop offset="1" stop-color="#b87a26"/></linearGradient>
  <linearGradient id="br8" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c88634"/><stop offset="1" stop-color="#8a531e"/></linearGradient>
  <linearGradient id="tq8" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#b8fff4"/><stop offset=".5" stop-color="#3fd8c8"/><stop offset="1" stop-color="#168f88"/></linearGradient>
</defs>
<ellipse cx="240" cy="230" rx="238" ry="205" fill="url(#bg)"/>
{pyramids}{dunes}
<ellipse cx="270" cy="404" rx="210" ry="14" fill="{L}" opacity=".16"/>
<g class="wag">{tail}</g>
<g class="breathe">{legsFar}</g>
{clawFar}
<g class="breathe">{body}{legsNear}</g>
<g class="sway">{headG}</g>
{clawNear}
{wind}{sand}{sp}
</svg>'''
open(sys.argv[1] if len(sys.argv) > 1 else '8_sabaku_shin.svg', 'w').write(svg)
