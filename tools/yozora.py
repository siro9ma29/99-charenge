import math, sys, random
L = '#2b2b3a'
OUT = sys.argv[1] if len(sys.argv) > 1 else '7_yozora_shin.svg'
random.seed(7)

def mirror(s): return f'<g transform="translate(480 0) scale(-1 1)">{s}</g>'
def lerp(a, b, t): return a + (b - a) * t

# ---------- つばさ（左。右は鏡うつし） ----------
S, C, T = (190, 226), (114, 136), (58, 98)          # かた → うでの線 → つばさの先
def arm(t):
    u = 1 - t
    return (u*u*S[0] + 2*u*t*C[0] + t*t*T[0], u*u*S[1] + 2*u*t*C[1] + t*t*T[1])

def feather(x, y, ang, ln, w, fill, vein=True):
    p = (f'M0 {-w*.42:.1f} L{ln-w*.8:.1f} {-w*.5:.1f} Q{ln:.1f} {-w*.5:.1f} {ln:.1f} 0 '
         f'Q{ln:.1f} {w*.5:.1f} {ln-w*.8:.1f} {w*.5:.1f} L0 {w*.42:.1f} Z')
    v = f'<path d="M{ln*.35:.1f} 0 L{ln-w*.7:.1f} 0" stroke="#7c68e8" stroke-width="1.8" stroke-linecap="round" opacity=".6"/>' if vein else ''
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})">'
            f'<path d="{p}" fill="{fill}" stroke="{L}" stroke-width="2.8" stroke-linejoin="round"/>{v}</g>')

def wing():
    s = ''
    # 風切り羽（長い羽 10まい）— 先のほうから かさねる
    N = 10
    for i in reversed(range(N)):
        t = 0.04 + 0.96 * i / (N - 1)
        x, y = arm(t)
        s += feather(x, y, lerp(92, 150, t), lerp(168, 90, t**1.3), lerp(34, 28, t), 'url(#fw7)')
    # 雨覆（中くらいの羽 8まい）
    N = 8
    for i in reversed(range(N)):
        t = 0.02 + 0.9 * i / (N - 1)
        x, y = arm(t)
        s += feather(x, y, lerp(94, 146, t), lerp(84, 54, t), lerp(36, 30, t), '#4a38a8', vein=False)
    # うでの線（いちばん明るい羽のふち）
    d = f'M{S[0]} {S[1]} Q{C[0]} {C[1]} {T[0]} {T[1]}'
    s += f'<path d="{d}" fill="none" stroke="{L}" stroke-width="30" stroke-linecap="round"/>'
    s += f'<path d="{d}" fill="none" stroke="#6a55d8" stroke-width="24" stroke-linecap="round"/>'
    s += f'<path d="M{S[0]-6} {S[1]-10} Q{C[0]-4} {C[1]-6} {T[0]+4} {T[1]-4}" fill="none" stroke="#a99cff" stroke-width="4" stroke-linecap="round" opacity=".8"/>'
    return s

def dust(n, region):
    o = ''
    for _ in range(n):
        x, y = region()
        o += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(1.1, 2.1):.1f}" fill="#fff" opacity="{random.uniform(.55, .95):.2f}"/>'
    return o
def wing_pt():
    t = random.uniform(.05, .95); x, y = arm(t)
    a = math.radians(lerp(92, 150, t)); r = random.uniform(70, lerp(158, 84, t))
    return x + r*math.cos(a), y + r*math.sin(a)
dustW = dust(22, wing_pt)

# ---------- 北斗七星（7の段の ひみつの かず）右のつばさ ----------
DIP = [(446, 220), (440, 262), (396, 268), (394, 226), (372, 196), (362, 162), (342, 132)]
def spark(x, y, r, cls):
    p = f'M0 {-r} L{r*.28:.1f} {-r*.28:.1f} L{r} 0 L{r*.28:.1f} {r*.28:.1f} L0 {r} L{-r*.28:.1f} {r*.28:.1f} L{-r} 0 L{-r*.28:.1f} {-r*.28:.1f} Z'
    return (f'<g transform="translate({x} {y})"><circle r="{r*1.3:.1f}" fill="#fff3a0" opacity=".5" filter="url(#soft)" class="glow {cls}"/>'
            f'<path d="{p}" fill="#ffe066" stroke="{L}" stroke-width="2.4" stroke-linejoin="round"/></g>')
ld = ('M' + ' L'.join(f'{DIP[i][0]} {DIP[i][1]}' for i in [0, 1, 2, 3, 0]) +
      ' M' + ' L'.join(f'{DIP[i][0]} {DIP[i][1]}' for i in [3, 4, 5, 6]))
dipper = f'<path d="{ld}" fill="none" stroke="#fff6a8" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>'
dipper += ''.join(spark(x, y, 13 if i in (0, 3) else 11.5, f'd{i%4}') for i, (x, y) in enumerate(DIP))

# ---------- 尾羽（えだの うしろ） ----------
tail = ''
for a, ln in [(66, 64), (80, 76), (94, 80), (108, 74), (122, 62)]:
    tail += feather(240, 380, a, ln, 30, '#2e2470', vein=False)

# ---------- 体（むねに 銀河の うず） ----------
body = f'''<path d="M174 216 Q136 276 156 336 Q174 384 212 398 L268 398 Q306 384 324 336 Q344 276 306 216 Q240 196 174 216 Z"
 fill="url(#bd7)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>'''
def spiral(cx, cy, k, rot, sx=1.0, sy=0.8, r0=6, turns=1.35):
    pts = []
    for i in range(40):
        th = i / 39 * turns * 2 * math.pi
        r = r0 * math.exp(k * th)
        a = th + rot
        pts.append((cx + r*math.cos(a)*sx, cy + r*math.sin(a)*sy))
    return 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts)
GX, GY = 240, 272
galaxy = f'<ellipse cx="{GX}" cy="{GY}" rx="70" ry="58" fill="url(#gx7)"/>'
arms = ''
for rot in (0, math.pi):
    d = spiral(0, 0, 0.27, rot)
    arms += f'<path d="{d}" fill="none" stroke="#9fb4ff" stroke-width="9" stroke-linecap="round" opacity=".55"/>'
    arms += f'<path d="{d}" fill="none" stroke="#e3e9ff" stroke-width="3.4" stroke-linecap="round" opacity=".9"/>'
galaxy += f'<g transform="translate({GX} {GY})"><g class="gspin">{arms}</g></g>'
galaxy += f'<circle cx="{GX}" cy="{GY}" r="20" fill="#fff6c0" opacity=".7" filter="url(#soft)" class="glow"/><circle cx="{GX}" cy="{GY}" r="8" fill="#fffbe6"/>'
bodydust = dust(14, lambda: (random.uniform(178, 302), random.uniform(232, 386)))

# ---------- えだ と 足 ----------
def by(x): return 408 - 0.25 * (x - 20)          # えだの上の線
branch = (f'<path d="M-10 {by(-10)+2:.0f} L490 {by(490):.0f} L490 {by(490)+30:.0f} L-10 {by(-10)+32:.0f} Z" fill="#4b4157" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>'
          f'<path d="M60 {by(60)+14:.0f} L170 {by(170)+12:.0f} M300 {by(300)+16:.0f} L420 {by(420)+12:.0f}" stroke="#665a72" stroke-width="3" stroke-linecap="round"/>')
def leg(x):
    yb = by(x)
    pd = f'M{x-24} 322 Q{x-30} {yb-14:.0f} {x-16} {yb-4:.0f} L{x+16} {yb-4:.0f} Q{x+30} {yb-14:.0f} {x+24} 322'
    o = f'<path d="{pd} Z" fill="#3a2f90"/><path d="{pd}" fill="none" stroke="{L}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
    o += f'<path d="M{x-14} {yb-22:.0f} q7 6 14 0 q7 6 14 0" fill="none" stroke="#6f5bd6" stroke-width="2.4" stroke-linecap="round"/>'
    for dx in (-15, 0, 15):          # 前に 3本、えだを つかむ
        x0, y0 = x + dx*0.5, yb - 6
        x1, y1 = x + dx, by(x + dx) + 12
        o += f'<path d="M{x0:.1f} {y0:.1f} Q{x1+2:.1f} {y0:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{L}" stroke-width="12" stroke-linecap="round"/>'
        o += f'<path d="M{x0:.1f} {y0:.1f} Q{x1+2:.1f} {y0:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="#5a4f86" stroke-width="7.4" stroke-linecap="round"/>'
        o += f'<path d="M{x1-4:.1f} {y1-2:.1f} Q{x1:.1f} {y1+12:.1f} {x1-8:.1f} {y1+16:.1f}" fill="none" stroke="{L}" stroke-width="4.4" stroke-linecap="round"/>'
        o += f'<path d="M{x1-4:.1f} {y1-1:.1f} Q{x1-1:.1f} {y1+10:.1f} {x1-7:.1f} {y1+14:.1f}" fill="none" stroke="#c9d2ff" stroke-width="1.6" stroke-linecap="round"/>'
    return o
legs = leg(206) + leg(274)

# ---------- 頭 ----------
# 光る えだ角（左右 3本ずつ。先は 6つ → 7にしない）
def antler():
    d = 'M200 94 Q188 60 168 14 M188 62 Q170 54 150 50 M178 38 Q186 26 196 16'
    return (f'<path d="{d}" fill="none" stroke="#8fd3ff" stroke-width="16" stroke-linecap="round" opacity=".45" filter="url(#soft)" class="glow d2"/>'
            f'<path d="{d}" fill="none" stroke="{L}" stroke-width="10" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#bfe8ff" stroke-width="5.4" stroke-linecap="round"/>')
head = antler() + mirror(antler())
head += f'''
<path d="M160 146 Q160 84 240 78 Q320 84 320 146 Q320 206 280 228 Q240 242 200 228 Q160 206 160 146 Z" fill="#2e2470" stroke="{L}" stroke-width="3.4" stroke-linejoin="round"/>
<path d="M240 122 Q220 106 198 110 Q172 118 172 156 Q174 196 206 212 Q226 220 240 232 Q254 220 274 212 Q306 196 308 156 Q308 118 282 110 Q260 106 240 122 Z" fill="#8a80d8" stroke="{L}" stroke-width="2.6" stroke-linejoin="round"/>
<g transform="translate(240 100)"><path d="{spiral(0, 0, 0.3, 0.6, 1, .7, 2.4, 1.2)}" fill="none" stroke="#c9bfff" stroke-width="3" stroke-linecap="round"/><circle r="3" fill="#fffbe6"/></g>
'''
def eye(cx, side, id_):
    cy = 158
    if side < 0:
        clip = f'M{cx-32} {cy-22} L{cx+32} {cy-2} L{cx+32} {cy+40} L{cx-32} {cy+40} Z'; lid = f'M{cx-26} {cy-19} L{cx+28} {cy-3}'
    else:
        clip = f'M{cx-32} {cy-2} L{cx+32} {cy-22} L{cx+32} {cy+40} L{cx-32} {cy+40} Z'; lid = f'M{cx+26} {cy-19} L{cx-28} {cy-3}'
    hx = -6 if side < 0 else 6
    return (f'<circle cx="{cx}" cy="{cy+4}" r="30" fill="#ffb84a" opacity=".35" filter="url(#soft)" class="glow"/>'
            f'<clipPath id="{id_}"><path d="{clip}"/></clipPath><g clip-path="url(#{id_})">'
            f'<circle cx="{cx}" cy="{cy+2}" r="24" fill="#fff0c0" stroke="{L}" stroke-width="2.6"/>'
            f'<circle cx="{cx}" cy="{cy+3}" r="19" fill="#ffa928"/>'
            f'<circle cx="{cx}" cy="{cy+5}" r="10" fill="#1f1640"/>'
            f'<circle cx="{cx+hx}" cy="{cy-1}" r="4.2" fill="#fff"/><circle cx="{cx-hx*0.6}" cy="{cy+11}" r="2" fill="#fff"/></g>'
            f'<path d="{lid}" stroke="{L}" stroke-width="3.6" stroke-linecap="round"/>')
head += eye(206, -1, 'e7L') + eye(274, 1, 'e7R')
head += f'''
<path d="M228 178 Q240 170 252 178 Q252 202 240 218 Q228 202 228 178 Z" fill="#3d4a7a" stroke="{L}" stroke-width="2.8" stroke-linejoin="round"/>
<path d="M235 180 Q238 194 240 206" fill="none" stroke="#8fa3d8" stroke-width="2.2" stroke-linecap="round"/>
'''

# ---------- はいけい ----------
aur = ''
for k, (col, y0) in enumerate([('#5ee0a8', 40), ('#57c8e8', 62), ('#a78bff', 84)]):
    aur += f'<path d="M-20 {y0+40} Q90 {y0-10} 200 {y0+30} T420 {y0+10} T520 {y0+30}" fill="none" stroke="{col}" stroke-width="26" stroke-linecap="round" opacity=".32" filter="url(#soft2)"/>'

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 480 444" width="480" height="444">
<title>よぞらの ぬし しんの すがた</title>
<style>
  .breathe{{transform-origin:240px 330px;animation:br 3.2s ease-in-out infinite}}
  @keyframes br{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.015,1.025)}}}}
  .sway{{transform-origin:240px 220px;animation:sw 4s ease-in-out infinite}}
  @keyframes sw{{0%,100%{{transform:rotate(-1.2deg)}}50%{{transform:rotate(1.2deg)}}}}
  .flapL{{transform-origin:192px 224px;animation:fl 3s ease-in-out infinite}}
  .flapR{{transform-origin:288px 224px;animation:fr 3s ease-in-out infinite}}
  @keyframes fl{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(4deg)}}}}
  @keyframes fr{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-4deg)}}}}
  .glow{{animation:gl 2.4s ease-in-out infinite}}
  .d1{{animation-delay:.6s}}.d2{{animation-delay:1.2s}}.d3{{animation-delay:1.8s}}
  @keyframes gl{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
  .gspin{{animation:gs 14s linear infinite}}
  @keyframes gs{{to{{transform:rotate(360deg)}}}}
  .aur{{animation:au 6s ease-in-out infinite}}
  @keyframes au{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(14px)}}}}
  .tw{{animation:tw 2.2s ease-in-out infinite}}
  @keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:.9}}}}
  .shoot{{animation:sh 4s ease-in infinite}}
  @keyframes sh{{0%,60%{{transform:translate(0,0);opacity:0}}65%{{opacity:1}}100%{{transform:translate(60px,40px);opacity:0}}}}
</style>
<defs>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
  <filter id="soft2" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
  <radialGradient id="bg7" cx="50%" cy="45%" r="58%"><stop offset="0" stop-color="#7d72d8"/><stop offset=".55" stop-color="#a59df0" stop-opacity=".6"/><stop offset="1" stop-color="#cfc8ff" stop-opacity="0"/></radialGradient>
  <linearGradient id="fw7" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2e2470"/><stop offset=".5" stop-color="#3d2f96"/><stop offset=".78" stop-color="#2f8f8c"/><stop offset="1" stop-color="#3a2a8a"/></linearGradient>
  <linearGradient id="bd7" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e2470"/><stop offset="1" stop-color="#3a2f90"/></linearGradient>
  <radialGradient id="gx7" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#8aa0ff" stop-opacity=".8"/><stop offset=".6" stop-color="#6a5ad8" stop-opacity=".45"/><stop offset="1" stop-color="#6a5ad8" stop-opacity="0"/></radialGradient>
  <radialGradient id="moon7" cx="40%" cy="40%" r="60%"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#dfe3f5"/></radialGradient>
</defs>
<!-- はいけい：夜空・オーロラ・満月・流れ星 -->
<ellipse cx="240" cy="210" rx="250" ry="220" fill="url(#bg7)"/>
<g class="aur">{aur}</g>
<circle cx="424" cy="14" r="34" fill="#fff" opacity=".35" filter="url(#soft)" class="glow"/>
<circle cx="424" cy="14" r="24" fill="url(#moon7)" stroke="{L}" stroke-width="2.4"/>
<circle cx="416" cy="8" r="4" fill="#cfd4ea"/><circle cx="430" cy="22" r="5" fill="#cfd4ea"/>
<g class="shoot"><path d="M20 -14 L62 14" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".7"/><circle cx="62" cy="14" r="3.4" fill="#fff"/></g>
<g class="tw"><circle cx="120" cy="-6" r="1.6" fill="#fff"/><circle cx="350" cy="-12" r="1.6" fill="#fff"/><circle cx="270" cy="20" r="1.3" fill="#fff"/><circle cx="20" cy="40" r="1.5" fill="#fff"/></g>
<g class="breathe">
{tail}
<!-- つばさ（長い羽 10まい＋雨覆 8まい ずつ） -->
<g class="flapL">{wing()}{dustW}</g>
<g class="flapR">{mirror(wing() + dustW)}{dipper}</g>
{body}{galaxy}{bodydust}
</g>
{branch}
{legs}
<g class="sway">{head}</g>
</svg>'''
open(OUT, 'w').write(svg)
