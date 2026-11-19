import math, sys
# ゆきやまの ぬし しんの すがた（氷のよろいの 狼男）
# 6の段の ひみつの かず＝角の 6本の えだ（先の けっしょう6つ）。ほかのパーツは6にしない
#   肩のトゲ4本ずつ・つらら2本ずつ・こてのトゲ2本ずつ・つめ4本ずつ
L = '#2b2b3a'
def mir(s): return f'<g transform="translate(480 0) scale(-1 1)">{s}</g>'
AR = f'stroke="{L}" stroke-width="3" stroke-linejoin="round"'
def hl(d, w=2.4): return f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{w}" stroke-linecap="round" opacity=".85"/>'

def ice_stroke(d, w=11):
    return (f'<path d="{d}" fill="none" stroke="{L}" stroke-width="{w+5}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#7fd4ff" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#e9f8ff" stroke-width="{w*.35:.1f}" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/>')
def gem(x, y, ang, s=1.0):
    return (f'<g transform="translate({x} {y}) rotate({ang}) scale({s})">'
            f'<circle cx="0" cy="-6" r="16" fill="#bfeaff" opacity=".5" filter="url(#soft)" class="glow"/>'
            f'<path d="M0 -22 L12 -2 L0 12 L-12 -2 Z" fill="#bff0ff" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M0 -22 L0 12 L-12 -2 Z" fill="#fff" opacity=".55"/></g>')
def crystal(d, glow=True):
    # 光る 緑の けっしょう
    g = f'<path d="{d}" fill="#5af0c0" opacity=".6" filter="url(#soft)" class="glow"/>' if glow else ''
    return g + f'<path d="{d}" fill="url(#grn6)" stroke="{L}" stroke-width="2.6" stroke-linejoin="round"/>'
def spike(x1, y1, x2, y2, tx, ty):
    # 底辺(x1,y1)-(x2,y2)、先(tx,ty)の 氷のトゲ
    return (f'<path d="M{x1} {y1} L{tx} {ty} L{x2} {y2} Z" fill="url(#ice6)" {AR}/>'
            f'<path d="M{(x1+x2)/2:.1f} {(y1+y2)/2:.1f} L{tx} {ty}" stroke="#fff" stroke-width="1.8" stroke-linecap="round" opacity=".8"/>')
def icicle(x, y, ln):
    return f'<path d="M{x-5} {y} L{x} {y+ln} L{x+5} {y} Z" fill="#dff6ff" stroke="{L}" stroke-width="2.2" stroke-linejoin="round"/>'

# ---- 角（3本＋3本＝6本の えだ）高さは もとの 2/3 ----
beam = 'M260 104 C266 81 278 59 288 37'
t1 = 'M268 85 C290 76 312 72 334 72'
t2 = 'M279 64 C296 53 314 47 332 44'
antR = ice_stroke(beam) + ice_stroke(t1, 9) + ice_stroke(t2, 9)
antR += gem(290, 33, 25) + gem(340, 72, 90, .85) + gem(338, 43, 80, .85)
horns = antR + mir(antR)

# ---- 頭（顔と鼻先は1つのりんかく。口を大きく開けて きば4本）----
head_d = ('M240 98 C272 98 308 104 330 128 L354 140 L338 150 L362 172 L336 180 L352 200 L314 206 '
          'C300 212 290 222 284 236 L280 262 Q272 288 240 290 Q208 288 200 262 L196 236 '
          'C190 222 180 212 166 206 L128 200 L144 180 L118 172 L142 150 L126 140 L150 128 C172 104 208 98 240 98 Z')
def eye(cx, cy, side, id_):
    if side < 0:
        clip = f'M{cx-22} {cy-18} L{cx+22} {cy} L{cx+22} {cy+26} L{cx-22} {cy+26} Z'; lid = f'M{cx-17} {cy-15} L{cx+19} {cy-1}'
    else:
        clip = f'M{cx-22} {cy} L{cx+22} {cy-18} L{cx+22} {cy+26} L{cx-22} {cy+26} Z'; lid = f'M{cx+17} {cy-15} L{cx-19} {cy-1}'
    hx = -5 if side < 0 else 5
    return (f'<ellipse cx="{cx}" cy="{cy+2}" rx="20" ry="16" fill="#7fe8ff" opacity=".7" filter="url(#soft)" class="glow"/>'
            f'<clipPath id="{id_}"><path d="{clip}"/></clipPath><g clip-path="url(#{id_})">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="13" ry="14" fill="#7fe8ff" stroke="{L}" stroke-width="2.4"/>'
            f'<ellipse cx="{cx}" cy="{cy+2}" rx="6" ry="8" fill="#123050"/>'
            f'<circle cx="{cx+hx}" cy="{cy-3}" r="3.6" fill="#fff"/><circle cx="{cx-hx*.6}" cy="{cy+6}" r="1.8" fill="#fff"/></g>'
            f'<path d="{lid}" stroke="{L}" stroke-width="3.6" stroke-linecap="round"/>')
# 面：額当てが ほおの エラまで つづく（頭の上は 毛のまま。耳も出す）
ear = (f'<path d="M172 126 L118 86 L204 104 Z" fill="url(#fur6)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>'
       f'<path d="M172 118 L136 92 L194 106 Z" fill="#9fc8f0"/>')
cheek = f'<path d="M150 142 C148 166 156 188 166 206 L188 206 L186 170 L172 152 Z" fill="url(#arm6)" {AR}/>'
# 面のふちは なめらか。外がわの ギザギザの たてがみ（毛）が 面の横から出る
# ほおの先は あごの りんかくに そって 鼻先の方へ とがる
mask_d = ('M182 126 Q240 108 298 126 L326 150 C334 168 328 190 314 204 C302 210 292 222 286 238 '
          'L290 206 L294 170 L284 156 L254 160 L240 174 L226 160 L196 156 L186 170 L190 206 L194 238 '
          'C188 222 178 210 166 204 C152 190 146 168 154 150 L182 126 Z')
helmet = (f'<path d="{mask_d}" fill="url(#ice6)" {AR}/>'
          + hl('M194 126 Q210 118 224 116') + hl('M286 126 Q270 118 256 116') + hl('M160 164 Q160 186 174 202') + hl('M320 164 Q320 186 306 202')
          + crystal('M240 112 L251 130 L240 152 L229 130 Z'))
head = f'''{ear}{mir(ear)}
<path d="{head_d}" fill="url(#fur6)" stroke="{L}" stroke-width="3.4" stroke-linejoin="round"/>
<path d="M198 160 Q240 150 282 160 Q292 190 286 210 Q278 230 278 262 Q270 284 240 286 Q210 284 202 262 Q202 230 194 210 Q188 190 198 160 Z" fill="#dcefff"/>
{helmet}
{eye(212,176,-1,'e6L')}{eye(268,176,1,'e6R')}
<path d="M210 248 Q240 238 270 248 Q266 280 240 284 Q214 280 210 248 Z" fill="#7a1f35" stroke="{L}" stroke-width="2.8" stroke-linejoin="round"/>
<ellipse cx="240" cy="274" rx="14" ry="7" fill="#ff7aa0"/>
<path d="M216 249 L222 266 L229 246 Z M264 249 L258 266 L251 246 Z" fill="#fff" stroke="{L}" stroke-width="2" stroke-linejoin="round"/>
<path d="M222 278 L227 266 L232 280 Z M258 278 L253 266 L248 280 Z" fill="#fff" stroke="{L}" stroke-width="2" stroke-linejoin="round"/>
<path d="M226 222 Q240 214 254 222 Q252 234 240 236 Q228 234 226 222 Z" fill="{L}"/>
<path d="M234 220 q6 -3 10 0" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".7"/>
<path d="M240 236 v6" stroke="{L}" stroke-width="2.4" stroke-linecap="round"/>
'''

# ---- 体：前かがみで 脚を大きく開いた 狼男（1つのりんかく）----
def sym_path(start, segs):
    m = lambda q: (480 - q[0], q[1])
    d = f'M{start[0]} {start[1]} '; pts = [start]
    for sg in segs:
        d += sg[0] + ' ' + ' '.join(f'{x} {y}' for x, y in sg[1:]) + ' '; pts.append(sg[-1])
    for i in range(len(segs) - 1, -1, -1):
        sg = segs[i]; p0 = pts[i]
        if sg[0] == 'C': d += f'C{m(sg[2])[0]} {m(sg[2])[1]} {m(sg[1])[0]} {m(sg[1])[1]} {m(p0)[0]} {m(p0)[1]} '
        elif sg[0] == 'Q': d += f'Q{m(sg[1])[0]} {m(sg[1])[1]} {m(p0)[0]} {m(p0)[1]} '
        else: d += f'L{m(p0)[0]} {m(p0)[1]} '
    return d + 'Z'
body_d = sym_path((240, 250), [
    ('C', (200, 248), (160, 246), (124, 260)),   # 首→肩
    ('C', (90, 272), (72, 298), (70, 320)),      # 肩の丸み
    ('C', (70, 332), (74, 340), (80, 348)),      # 前うで（内がわへ）
    ('L', (114, 352)),                            # 手首
    ('C', (116, 340), (118, 330), (122, 320)),   # 前うで（内がわ）
    ('C', (126, 306), (138, 298), (152, 296)),   # わきの下
    ('C', (160, 310), (172, 322), (182, 328)),   # 細い腰
    ('C', (176, 340), (166, 352), (162, 366)),   # 太もも→ひざ
    ('C', (160, 380), (158, 392), (154, 402)),   # すね→足
    ('L', (210, 402)),
    ('C', (210, 390), (212, 380), (216, 370)),   # すね（内がわ）
    ('C', (224, 360), (232, 352), (240, 350)),   # 太もも（内がわ）
])
def hand(x, y):
    s_ = (f'<path d="M{x-22} {y-10} C{x-30} {y+8} {x-20} {y+26} {x} {y+26} C{x+20} {y+26} {x+30} {y+8} {x+22} {y-10} Z" '
          f'fill="url(#fur6)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>')
    for cx in (x-17, x-6, x+6, x+17):   # かぎ形に まがった 氷のつめ（4本）
        s_ += (f'<path d="M{cx-5} {y+20} Q{cx-8} {y+38} {cx+3} {y+50} Q{cx+2} {y+36} {cx+5} {y+20} Z" '
               f'fill="#cff4ff" stroke="{L}" stroke-width="2.2" stroke-linejoin="round"/>')
    return s_
def foot(x):
    s_ = ''
    for cx in (x-24, x-8, x+8, x+24):
        s_ += f'<path d="M{cx-5} 398 Q{cx-2} 410 {cx+4} 414 Q{cx+4} 406 {cx+5} 398 Z" fill="#cff4ff" stroke="{L}" stroke-width="2" stroke-linejoin="round"/>'
    return s_

# ---- よろい ----
pauldron = (spike(80, 272, 98, 256, 52, 226) + spike(100, 256, 122, 248, 88, 200)
            + spike(124, 248, 148, 244, 128, 192) + spike(150, 246, 172, 250, 172, 204)
            + f'<path d="M60 312 Q74 252 180 244 L188 284 L152 310 L94 316 Z" fill="url(#ice6)" {AR}/>'
            + f'<path d="M70 314 L114 296 L158 306 L140 330 L92 332 Z" fill="url(#arm6)" {AR}/>'
            + crystal('M112 266 L134 258 L146 276 L120 284 Z', glow=False)
            + icicle(104, 331, 22) + icicle(128, 329, 16) + hl('M76 292 Q98 258 150 252'))
vamb = (spike(68, 324, 72, 336, 36, 318) + spike(72, 336, 78, 346, 40, 350)
        + f'<path d="M70 316 L124 320 L116 352 L78 350 Z" fill="url(#arm6)" {AR}/>'
        + crystal('M90 326 L108 328 L104 344 L88 342 Z', glow=False) + hl('M78 324 L82 344'))
chest = (f'<path d="M182 274 L212 266 L240 272 L268 266 L298 274 L306 306 L290 330 L262 326 L240 344 L218 326 L190 330 L174 306 Z" fill="url(#arm6)" {AR}/>'
         + hl('M192 284 Q200 302 196 320') + hl('M288 284 Q280 302 284 320')
         + crystal('M240 284 L258 300 L240 332 L222 300 Z')
         + f'<path d="M196 330 L204 330 L200 344 Z M276 330 L284 330 L280 344 Z" fill="#dff6ff" stroke="{L}" stroke-width="2" stroke-linejoin="round"/>')
belt = (f'<path d="M196 336 L284 336 L270 362 L240 374 L210 362 Z" fill="url(#ice6)" {AR}/>'
        + crystal('M240 344 L250 356 L240 368 L230 356 Z', glow=False))
thigh = f'<path d="M150 340 L194 346 L186 364 L140 362 Z" fill="url(#arm6)" {AR}/>' + hl('M154 346 L148 358')
knee = (f'<path d="M124 352 L148 340 L162 366 L146 390 L124 376 Z" fill="url(#ice6)" {AR}/>'
        + crystal('M142 352 L152 366 L142 380 L134 366 Z'))
greave = f'<path d="M114 384 L176 384 L178 400 L110 400 Z" fill="url(#arm6)" {AR}/>' + hl('M120 390 L170 390', 2)
tk = lambda x, g: f'<g transform="translate({x} 0)">{g}</g>'
armor = (chest + belt + tk(22, thigh) + mir(tk(22, thigh)) + tk(40, greave) + mir(tk(40, greave)) + tk(34, knee) + mir(tk(34, knee))
         + vamb + mir(vamb))
ruff = ('M154 236 L138 254 L160 258 L156 274 L180 268 L188 284 L210 272 L222 288 L240 278 '
        'L258 288 L270 272 L292 284 L300 268 L324 274 L320 258 L342 254 L326 236 Z')
tail = (f'<path d="M296 344 C360 356 426 334 442 280 C448 254 440 226 424 214 C412 240 420 266 412 288 C400 316 350 322 302 318 Z" '
        f'fill="url(#fur6)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>'
        + spike(418, 214, 440, 220, 430, 172))
# 地面から つき出た 氷（5本）
ground = (spike(20, 404, 40, 404, 26, 350) + spike(40, 404, 56, 404, 54, 368) + spike(70, 404, 84, 404, 72, 378)
          + spike(398, 404, 414, 404, 404, 372) + spike(414, 404, 438, 404, 448, 346))
aurora = (f'<path d="M-10 60 C80 10 160 70 240 30 C320 -10 400 50 490 10 L490 60 C400 100 320 40 240 80 C160 120 80 60 -10 110 Z" '
          f'fill="url(#aur6)" opacity=".35" filter="url(#soft)"/>')
snow = ''.join(f'<g class="fall {d}"><circle cx="{x}" cy="{y}" r="{r}" fill="#fff"/></g>'
               for x, y, r, d in [(60, 40, 3, ''), (420, 70, 2.5, 'd1'), (40, 170, 3, 'd2'), (452, 150, 2, 'd3'),
                                  (90, 280, 2.5, 'd1'), (30, 260, 2, 'd3'), (110, 10, 2, 'd2'), (380, 20, 3, ''), (460, 290, 2.5, 'd2')])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 480 444" width="480" height="444">
<title>ゆきやまの ぬし しんの すがた</title>
<style>
  .breathe{{transform-origin:240px 330px;animation:br 3s ease-in-out infinite}}
  @keyframes br{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.015,1.025)}}}}
  .sway{{transform-origin:240px 270px;animation:sw 4s ease-in-out infinite}}
  @keyframes sw{{0%,100%{{transform:rotate(-1.2deg)}}50%{{transform:rotate(1.2deg)}}}}
  .wag{{transform-origin:310px 330px;animation:wg 3s ease-in-out infinite}}
  @keyframes wg{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-4deg)}}}}
  .glow{{animation:gl 2.4s ease-in-out infinite}}
  @keyframes gl{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
  .fall{{animation:fa 5s linear infinite}}
  .d1{{animation-delay:1.2s}}.d2{{animation-delay:2.4s}}.d3{{animation-delay:3.6s}}
  @keyframes fa{{0%{{transform:translate(0,-30px);opacity:0}}15%{{opacity:1}}100%{{transform:translate(-30px,140px);opacity:0}}}}
</style>
<defs>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
  <radialGradient id="bg" cx="50%" cy="55%" r="55%"><stop offset="0" stop-color="#bfe2ff"/><stop offset=".6" stop-color="#bfe2ff" stop-opacity=".5"/><stop offset="1" stop-color="#bfe2ff" stop-opacity="0"/></radialGradient>
  <linearGradient id="aur6" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5af0c0"/><stop offset=".5" stop-color="#7fd4ff"/><stop offset="1" stop-color="#b48cff"/></linearGradient>
  <linearGradient id="ice6" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f0fbff"/><stop offset="1" stop-color="#8fd6ff"/></linearGradient>
  <linearGradient id="arm6" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e0f6ff"/><stop offset=".55" stop-color="#9fd8f5"/><stop offset="1" stop-color="#6aa8dc"/></linearGradient>
  <linearGradient id="grn6" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c8ffe8"/><stop offset=".5" stop-color="#4fe0b0"/><stop offset="1" stop-color="#1fa88a"/></linearGradient>
  <linearGradient id="fur6" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a8fd0"/><stop offset="1" stop-color="#2f5a9e"/></linearGradient>
</defs>
<ellipse cx="240" cy="230" rx="238" ry="205" fill="url(#bg)"/>
{aurora}
<ellipse cx="240" cy="404" rx="170" ry="12" fill="{L}" opacity=".18"/>
<g class="wag">{tail}</g>
<g class="breathe">
<path d="{body_d}" fill="url(#fur6)" stroke="{L}" stroke-width="3.4" stroke-linejoin="round"/>
{foot(182)}{mir(foot(182))}
{armor}
<path d="{ruff}" fill="url(#fur6)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>
{pauldron}{mir(pauldron)}
{hand(96, 356)}{hand(384, 356)}
</g>
<!-- 角（6の段の ひみつの かず＝6本の えだ）と 頭 -->
<g class="sway"><g transform="translate(0 36)">{horns}</g><g transform="translate(240 290) scale(.8 .8) translate(-240 -290)">{head}</g></g>
{snow}
</svg>'''
open(sys.argv[1] if len(sys.argv) > 1 else '6_yukiyama_shin.svg', 'w').write(svg)
