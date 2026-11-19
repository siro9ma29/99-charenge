import math
L='#2b2b3a'
gems=['#ff5a7a','#ff9a4a','#ffd84a','#a0ff6a','#5adf8a','#4ae0e0','#5ab0ff','#b48cff','#ff7ad9']
cx0,cy0,rx,ry=240,318,186,206
def crystal(x,y,ang,h,w,col,cls):
    p=f'M{-w} 0 L{-w} {-h*.55:.1f} L0 {-h} L{w} {-h*.55:.1f} L{w} 0 Z'
    f=f'M{-w} {-h*.55:.1f} L0 {-h} L0 0 L{-w} 0 Z'
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})">'
            f'<path d="M{-w*1.6:.1f} 4 L0 {-h*1.15:.1f} L{w*1.6:.1f} 4 Z" fill="{col}" opacity=".35" filter="url(#soft)" class="glow {cls}"/>'
            f'<path d="{p}" fill="{col}" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="{f}" fill="#fff" opacity=".35"/>'
            f'<path d="M0 {-h} L0 0" stroke="{L}" stroke-width="1.6" opacity=".5"/>'
            f'<path d="M{-w*.55:.1f} {-h*.5:.1f} L{-w*.55:.1f} {-h*.2:.1f}" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>'
            '</g>')
crys=''
for i in range(9):
    t=math.radians(162-i*18)
    x=cx0+rx*math.cos(t)*0.96; y=cy0-ry*math.sin(t)*0.96
    nx,ny=math.cos(t)/rx, -math.sin(t)/ry
    ang=math.degrees(math.atan2(nx, -ny))
    big=1-abs(i-4)/4*0.35
    crys+=crystal(x,y,ang,58*big,13*big,gems[i],'d'+str(i%4))

# shell plates (hexagons) clipped to dome
def hexa(x,y,r):
    pts=' '.join(f'{x+r*math.cos(math.radians(60*k+30)):.1f},{y+r*math.sin(math.radians(60*k+30)):.1f}' for k in range(6))
    return f'<polygon points="{pts}" fill="#6a7ca3" stroke="{L}" stroke-width="2.6" stroke-linejoin="round"/>'
plates=''
for (x,y) in [(240,190),(176,226),(304,226),(240,262),(118,268),(362,268),(176,298),(304,298),(240,330),(90,320),(390,320)]:
    plates+=hexa(x,y,30)

shell=f'''
<clipPath id="dome"><path d="M{cx0-rx} {cy0} A{rx} {ry} 0 0 1 {cx0+rx} {cy0} Z"/></clipPath>
<path d="M{cx0-rx} {cy0} A{rx} {ry} 0 0 1 {cx0+rx} {cy0} Z" fill="#4f5f84" stroke="{L}" stroke-width="3.6"/>
<g clip-path="url(#dome)">{plates}
<path d="M{cx0-rx+30} {cy0-150} Q{cx0-60} {cy0-200} {cx0+20} {cy0-196}" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".25"/></g>
<path d="M{cx0-rx-10} {cy0} Q{cx0} {cy0+30} {cx0+rx+10} {cy0} L{cx0+rx+4} {cy0+18} Q{cx0} {cy0+48} {cx0-rx-4} {cy0+18} Z" fill="#ffd84a" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>
<path d="M{cx0-rx} {cy0+9} Q{cx0} {cy0+38} {cx0+rx} {cy0+9}" fill="none" stroke="#c9902f" stroke-width="2" stroke-dasharray="2 10" stroke-linecap="round"/>
'''

def leg(x,flip=False):
    s=(f'<path d="M{x-38} 318 Q{x-44} 360 {x-40} 392 L{x+40} 392 Q{x+44} 360 {x+38} 318 Z" fill="#8f9dbb" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>'
       f'<path d="M{x-30} 342 q10 -8 20 0 q10 -8 20 0 q10 -8 20 0" fill="none" stroke="#4f5f84" stroke-width="2.4" stroke-linecap="round"/>'
       f'<path d="M{x-30} 362 q10 -8 20 0 q10 -8 20 0 q10 -8 20 0" fill="none" stroke="#4f5f84" stroke-width="2.4" stroke-linecap="round"/>')
    for dx in (-26,0,26):
        s+=f'<ellipse cx="{x+dx}" cy="394" rx="17" ry="14" fill="#8f9dbb" stroke="{L}" stroke-width="3"/>'
        s+=f'<path d="M{x+dx-10} 402 L{x+dx} 420 L{x+dx+10} 402 Z" fill="#fff" stroke="{L}" stroke-width="2.6" stroke-linejoin="round"/>'
    s+=f'<path d="M{x-38} 384 L{x+38} 384" stroke="#8f9dbb" stroke-width="6"/>'
    return s
legs=leg(112)+leg(368)
plastron=f'''
<path d="M58 326 C60 374 140 404 240 404 C340 404 420 374 422 326 Q240 356 58 326 Z" fill="#e8d9a8" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>
<path d="M76 362 C140 384 340 384 404 362" fill="none" stroke="#c9b27a" stroke-width="2.6" stroke-linecap="round"/>
<path d="M160 346 L158 394 M240 352 L240 402 M320 346 L322 394" stroke="#c9b27a" stroke-width="2.6" stroke-linecap="round"/>
'''

tail=f'''
<path d="M396 300 Q452 300 468 340 Q480 372 470 408 Q456 380 436 368 Q414 356 400 356 Z" fill="#8f9dbb" stroke="{L}" stroke-width="3.4" stroke-linejoin="round"/>
<path d="M470 408 L478 418 L462 404 Z" fill="#8f9dbb" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>
<path d="M418 304 L432 284 L438 308 Z M446 316 L466 302 L462 326 Z M464 342 L480 336 L472 358 Z" fill="#6a7ca3" stroke="{L}" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M416 324 q10 -6 20 0 q10 -6 20 0 M430 344 q10 -6 18 0 M446 364 q8 -6 16 2" fill="none" stroke="#5a6a8e" stroke-width="2.2" stroke-linecap="round"/>
'''


def eye(cx,cy,side,id_):
    if side<0: clip=f'M{cx-24} {cy-18} L{cx+24} {cy-2} L{cx+24} {cy+30} L{cx-24} {cy+30} Z'; lid=f'M{cx-17} {cy-15} L{cx+19} {cy-3}'
    else: clip=f'M{cx-24} {cy-2} L{cx+24} {cy-18} L{cx+24} {cy+30} L{cx-24} {cy+30} Z'; lid=f'M{cx+17} {cy-15} L{cx-19} {cy-3}'
    hx=-5 if side<0 else 5
    return (f'<clipPath id="{id_}"><path d="{clip}"/></clipPath><g clip-path="url(#{id_})">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="14" ry="15" fill="#b48cff" stroke="{L}" stroke-width="2.4"/>'
            f'<ellipse cx="{cx}" cy="{cy+2}" rx="7.5" ry="9" fill="#2a1a12"/>'
            f'<circle cx="{cx+hx}" cy="{cy-3}" r="3.8" fill="#fff"/><circle cx="{cx-hx*.6}" cy="{cy+7}" r="1.9" fill="#fff"/></g>'
            f'<path d="{lid}" stroke="{L}" stroke-width="3.4" stroke-linecap="round"/>')
hy=300
head=f'''
<path d="M158 {hy} Q156 {hy-84} 240 {hy-90} Q324 {hy-84} 322 {hy} Q322 {hy+56} 240 {hy+64} Q158 {hy+56} 158 {hy} Z" fill="#b3bfd6" stroke="{L}" stroke-width="3.4" stroke-linejoin="round"/>
<path d="M200 {hy-66} l8 -10 l8 10 M232 {hy-74} l8 -12 l8 12 M264 {hy-66} l8 -10 l8 10" fill="#8f9dbb" stroke="{L}" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M186 {hy-48} q12 -8 24 0 M270 {hy-48} q12 -8 24 0" fill="none" stroke="#5a6a8e" stroke-width="2.4" stroke-linecap="round"/>
<ellipse cx="182" cy="{hy+18}" rx="11" ry="6" fill="#ffb3c8" opacity=".6"/><ellipse cx="298" cy="{hy+18}" rx="11" ry="6" fill="#ffb3c8" opacity=".6"/>
{eye(206,hy-10,-1,'e9L')}{eye(274,hy-10,1,'e9R')}
<path d="M206 {hy+34} Q240 {hy+58} 274 {hy+34}" fill="none" stroke="{L}" stroke-width="3" stroke-linecap="round"/>
<path d="M194 {hy+20} Q240 {hy+4} 286 {hy+20} Q270 {hy+32} 252 {hy+32} L240 {hy+48} L228 {hy+32} Q210 {hy+32} 194 {hy+20} Z" fill="#5a6a8e" stroke="{L}" stroke-width="2.8" stroke-linejoin="round"/>
<path d="M210 {hy+16} Q240 {hy+8} 270 {hy+16}" fill="none" stroke="#8f9dbb" stroke-width="2.4" stroke-linecap="round"/>
<circle cx="232" cy="{hy+2}" r="2" fill="{L}"/><circle cx="248" cy="{hy+2}" r="2" fill="{L}"/>
'''
coins=''
for (x,y) in [(70,404),(92,410),(404,406),(426,401),(386,412)]:
    coins+=f'<ellipse cx="{x}" cy="{y}" rx="11" ry="5" fill="#ffd84a" stroke="{L}" stroke-width="2"/>'
coins+=crystal(48,408,-12,26,7,'#4ae0e0','d1')+crystal(26,396,-20,20,5,'#ff7ad9','d2')

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 480 444" width="480" height="444">
<title>どうくつの ぬし しんの すがた</title>
<style>
  .breathe{{transform-origin:240px 320px;animation:br 3.6s ease-in-out infinite}}
  @keyframes br{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.012,1.022)}}}}
  .sway{{transform-origin:240px 360px;animation:sw 4s ease-in-out infinite}}
  @keyframes sw{{0%,100%{{transform:rotate(-1.4deg)}}50%{{transform:rotate(1.4deg)}}}}
  .glow{{animation:gl 2.4s ease-in-out infinite}}
  .d1{{animation-delay:.6s}}.d2{{animation-delay:1.2s}}.d3{{animation-delay:1.8s}}
  @keyframes gl{{0%,100%{{opacity:.25}}50%{{opacity:.8}}}}
  .tw{{animation:tw 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
  @keyframes tw{{0%,100%{{opacity:0;transform:scale(.4)}}50%{{opacity:1;transform:scale(1)}}}}
</style>
<defs>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
  <path id="sp" d="M0 -6 L1.5 -1.5 L6 0 L1.5 1.5 L0 6 L-1.5 1.5 L-6 0 L-1.5 -1.5 Z" fill="#fffbd0"/>
  <radialGradient id="bg" cx="50%" cy="55%" r="55%"><stop offset="0" stop-color="#e3dcff"/><stop offset=".6" stop-color="#c9bdf5" stop-opacity=".5"/><stop offset="1" stop-color="#c9bdf5" stop-opacity="0"/></radialGradient>
</defs>
<!-- はいけいの光 -->
<ellipse cx="240" cy="230" rx="238" ry="205" fill="url(#bg)"/>
<g class="breathe">
<ellipse cx="240" cy="404" rx="200" ry="14" fill="{L}" opacity=".18"/>
<!-- しっぽ（こうらの うしろから のびる） -->
<g transform="translate(-16 0)">{tail}</g>
<!-- 宝石9つ（9の段の ひみつの かず）こうらの ふちに ならぶ -->
{crys}
<!-- こうら -->
{shell}
<!-- おなかの こうら（こうらと 同じ はば） -->
{plastron}
<!-- 足 -->
{legs}
</g>
<!-- 頭（こうらから のりだす） -->
<g class="sway">{head}</g>
<!-- たから -->
{coins}
<use href="#sp" x="60" y="60" class="tw"/><use href="#sp" x="420" y="50" class="tw d1"/><use href="#sp" x="30" y="230" class="tw d2"/><use href="#sp" x="450" y="240" class="tw d3"/>
</svg>'''
open('9_dokutsu_shin.svg','w').write(svg)
