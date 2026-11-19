import math
L='#2b2b3a'
def petal(length,w,fill):
    return (f'<path d="M0 0 C{length*.3:.1f} {-w:.1f} {length*.85:.1f} {-w*.9:.1f} {length:.1f} {-w*.15:.1f} '
            f'Q{length*.93:.1f} 0 {length:.1f} {w*.15:.1f} C{length*.85:.1f} {w*.9:.1f} {length*.3:.1f} {w:.1f} 0 0 Z" '
            f'fill="{fill}" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M{length*.12:.1f} 0 Q{length*.5:.1f} {-w*.12:.1f} {length*.82:.1f} 0" fill="none" stroke="#e2557d" stroke-width="1.8" stroke-linecap="round" opacity=".6"/>')
def wing(x,y):
    s=f'<g transform="translate({x} {y})">'
    for a,ln in [(236,150),(216,172),(196,174),(176,158),(156,126)]:
        s+=f'<g transform="rotate({a})">'+petal(ln,44,'url(#pet)')+'</g>'
    for a,ln in [(226,104),(206,118),(186,110),(166,86)]:
        s+=f'<g transform="rotate({a})">'+petal(ln,30,'#ffd6e8')+'</g>'
    s+=f'<circle r="20" fill="#ffe066" stroke="{L}" stroke-width="3"/>'
    for k in range(8):
        t=math.radians(k*45)
        s+=f'<circle cx="{11*math.cos(t):.1f}" cy="{11*math.sin(t):.1f}" r="3" fill="#ff9a3a"/>'
    return s+'</g>'
def mir(s): return f'<g transform="translate(480 0) scale(-1 1)">{s}</g>'
fl=lambda x,y,c,sc=1: f'<g transform="translate({x} {y}) scale({sc})"><use href="#fl{c}"/></g>'

wingL=wing(196,244)
ear=f'''<path d="M214 128 Q176 40 192 -14 Q214 -22 228 10 Q238 60 236 124 Z" fill="url(#fur)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>
<path d="M218 116 Q192 46 202 0 Q214 -2 220 20 Q228 64 228 116 Z" fill="#ffb0d0"/>'''
legL0=f'''<ellipse cx="194" cy="340" rx="42" ry="38" fill="url(#fur)" stroke="{L}" stroke-width="3.2"/>
<g transform="translate(0 -20)">
<path d="M200 390 Q150 386 140 400 Q144 412 196 412 Q214 410 214 398 Q212 390 200 390 Z" fill="#fff6c8" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>
<path d="M156 400 v10 M170 398 v13 M184 398 v13" stroke="{L}" stroke-width="2.4" stroke-linecap="round"/></g>
<path d="M168 330 q8 -8 16 0" fill="none" stroke="#e0a020" stroke-width="2.4" stroke-linecap="round"/>'''
armL0=f'''<path d="M206 240 C166 242 142 282 146 314 C148 338 186 340 190 318 C192 294 202 276 222 262 Z" fill="url(#fur)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>
<circle cx="168" cy="322" r="20" fill="#fff6c8" stroke="{L}" stroke-width="3"/>
<path d="M157 333 v6 M168 335 v6 M179 333 v6" stroke="{L}" stroke-width="2.4" stroke-linecap="round"/>'''
legL=f'<g transform="translate(-8 0)">{legL0}</g>'
armL=f'<g transform="translate(-6 0)">{armL0}</g>'
def eye(cx,cy,side,id_):
    if side<0: clip=f'M{cx-24} {cy-18} L{cx+24} {cy-2} L{cx+24} {cy+30} L{cx-24} {cy+30} Z'; lid=f'M{cx-17} {cy-15} L{cx+19} {cy-3}'
    else: clip=f'M{cx-24} {cy-2} L{cx+24} {cy-18} L{cx+24} {cy+30} L{cx-24} {cy+30} Z'; lid=f'M{cx+17} {cy-15} L{cx-19} {cy-3}'
    hx=-5 if side<0 else 5
    return (f'<clipPath id="{id_}"><path d="{clip}"/></clipPath><g clip-path="url(#{id_})">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="14" ry="15" fill="#e2557d" stroke="{L}" stroke-width="2.4"/>'
            f'<ellipse cx="{cx}" cy="{cy+2}" rx="7.5" ry="9" fill="#2a1a12"/>'
            f'<circle cx="{cx+hx}" cy="{cy-3}" r="3.8" fill="#fff"/><circle cx="{cx-hx*.6}" cy="{cy+7}" r="1.9" fill="#fff"/></g>'
            f'<path d="{lid}" stroke="{L}" stroke-width="3.4" stroke-linecap="round"/>')
hy=172
head=f'''{ear}{mir(ear)}
<path d="M172 {hy+10} L150 {hy+20} L170 {hy+28} L154 {hy+42} L182 {hy+40} Z" fill="url(#fur)" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>
{mir(f'<path d="M172 {hy+10} L150 {hy+20} L170 {hy+28} L154 {hy+42} L182 {hy+40} Z" fill="url(#fur)" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>')}
<path d="M172 {hy} Q170 {hy-62} 240 {hy-66} Q310 {hy-62} 308 {hy} Q306 {hy+54} 240 {hy+60} Q174 {hy+54} 172 {hy} Z" fill="url(#fur)" stroke="{L}" stroke-width="3.4" stroke-linejoin="round"/>
<path d="M206 {hy+22} Q240 {hy+6} 274 {hy+22} Q276 {hy+52} 240 {hy+58} Q204 {hy+52} 206 {hy+22} Z" fill="#fff6c8"/>
<ellipse cx="190" cy="{hy+20}" rx="11" ry="6" fill="#ffb3c8" opacity=".7"/><ellipse cx="290" cy="{hy+20}" rx="11" ry="6" fill="#ffb3c8" opacity=".7"/>
{eye(208,hy-6,-1,'e2L')}{eye(272,hy-6,1,'e2R')}
<path d="M232 {hy+20} Q240 {hy+14} 248 {hy+20} L240 {hy+30} Z" fill="#ff7aa8" stroke="{L}" stroke-width="2.4" stroke-linejoin="round"/>
<path d="M240 {hy+30} v8 M240 {hy+38} q-10 8 -18 0 M240 {hy+38} q10 8 18 0" fill="none" stroke="{L}" stroke-width="2.6" stroke-linecap="round"/>
<path d="M233 {hy+41} h14 v10 h-14 Z M240 {hy+41} v10" fill="#fff" stroke="{L}" stroke-width="2" stroke-linejoin="round"/>
<path d="M214 {hy+26} L182 {hy+22} M214 {hy+32} L184 {hy+36} M266 {hy+26} L298 {hy+22} M266 {hy+32} L296 {hy+36}" stroke="{L}" stroke-width="1.8" stroke-linecap="round"/>
{fl(240,hy-62,'Yel',1.4)}{fl(214,hy-58,'Pink',1.2)}{fl(266,hy-58,'Blue',1.2)}
'''
torso=f'''<path d="M240 212 C304 212 326 288 318 330 C310 368 276 380 240 380 C204 380 170 368 162 330 C154 288 176 212 240 212 Z" fill="url(#fur)" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>
<path d="M240 250 C280 250 292 300 286 330 C280 356 262 364 240 364 C218 364 200 356 194 330 C188 300 200 250 240 250 Z" fill="#fff6c8"/>
<path d="M206 262 Q214 246 224 258 Q232 242 240 256 Q248 242 256 258 Q266 246 274 262" fill="#fff6c8" stroke="{L}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>
{fl(226,290,'Pink',1)}{fl(256,306,'Blue',.9)}{fl(236,330,'Yel',.9)}'''
petals=''.join(f'<ellipse cx="{x}" cy="{y}" rx="6" ry="3.5" transform="rotate({r} {x} {y})" fill="#ffb0d0" class="fall {d}"/>' for x,y,r,d in [(70,60,30,''),(410,40,-20,'d1'),(100,180,10,'d2'),(400,190,40,'d3'),(60,300,-30,'d1'),(430,320,20,'')])
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 480 444" width="480" height="444">
<title>くさはらの ぬし しんの すがた</title>
<style>
  .breathe{{transform-origin:240px 320px;animation:br 3.2s ease-in-out infinite}}
  @keyframes br{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.015,1.025)}}}}
  .sway{{transform-origin:240px 230px;animation:sw 4s ease-in-out infinite}}
  @keyframes sw{{0%,100%{{transform:rotate(-1.2deg)}}50%{{transform:rotate(1.2deg)}}}}
  .flapL{{transform-origin:204px 236px;animation:fl 2.8s ease-in-out infinite}}
  .flapR{{transform-origin:276px 236px;animation:fr 2.8s ease-in-out infinite}}
  @keyframes fl{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(6deg)}}}}
  @keyframes fr{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-6deg)}}}}
  .fall{{animation:fa 5s linear infinite}}
  .d1{{animation-delay:1.2s}}.d2{{animation-delay:2.4s}}.d3{{animation-delay:3.6s}}
  @keyframes fa{{0%{{transform:translateY(-30px);opacity:0}}15%{{opacity:1}}100%{{transform:translateY(120px);opacity:0}}}}
  .tw{{animation:tw 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
  @keyframes tw{{0%,100%{{opacity:0;transform:scale(.4)}}50%{{opacity:1;transform:scale(1)}}}}
</style>
<defs>
  <path id="sp" d="M0 -6 L1.5 -1.5 L6 0 L1.5 1.5 L0 6 L-1.5 1.5 L-6 0 L-1.5 -1.5 Z" fill="#fffbd0"/>
  <g id="fp"><circle cx="0" cy="-7" r="5.5"/><circle cx="6.7" cy="-2.2" r="5.5"/><circle cx="4.1" cy="5.7" r="5.5"/><circle cx="-4.1" cy="5.7" r="5.5"/><circle cx="-6.7" cy="-2.2" r="5.5"/></g>
  <g id="flPink"><use href="#fp" fill="#ff9ccf" stroke="{L}" stroke-width="1.4"/><circle r="3.2" fill="#fff6a8"/></g>
  <g id="flBlue"><use href="#fp" fill="#7fc8ff" stroke="{L}" stroke-width="1.4"/><circle r="3.2" fill="#fff"/></g>
  <g id="flYel"><use href="#fp" fill="#ffe066" stroke="{L}" stroke-width="1.4"/><circle r="3.2" fill="#ff9a3a"/></g>
  <radialGradient id="bg" cx="50%" cy="55%" r="55%"><stop offset="0" stop-color="#fff1a8"/><stop offset=".6" stop-color="#fff1a8" stop-opacity=".5"/><stop offset="1" stop-color="#fff1a8" stop-opacity="0"/></radialGradient>
  <linearGradient id="fur" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0a6"/><stop offset="1" stop-color="#ffd257"/></linearGradient>
  <radialGradient id="pet" cx="0" cy="0" r="1" gradientUnits="objectBoundingBox"><stop offset="0" stop-color="#ffd6e8"/><stop offset="1" stop-color="#ff8fbf"/></radialGradient>
</defs>
<!-- はいけいの光 -->
<ellipse cx="240" cy="230" rx="238" ry="205" fill="url(#bg)"/>
<g class="breathe">
<ellipse cx="240" cy="396" rx="150" ry="12" fill="{L}" opacity=".15"/>
<!-- 花の つばさ 2まい（2の段の ひみつの かず） -->
<g class="flapL">{wingL}</g><g class="flapR">{mir(wingL)}</g>
<!-- 足（大きな うしろ足） -->
{legL}{mir(legL)}
<!-- 体 -->
{torso}
<!-- うで -->
{armL}{mir(armL)}
</g>
<!-- 頭と 耳 -->
<g class="sway"><g transform="translate(240 262) scale(1.15) translate(-240 -232)">{head}</g></g>
<!-- 花びら -->
{petals}
<!-- 草 -->
<path d="M20 418 l10 -26 l6 26 l10 -20 l4 20 M434 418 l8 -22 l6 22 l10 -26 l4 26" fill="#7fd26a" stroke="{L}" stroke-width="2.4" stroke-linejoin="round"/>
<use href="#sp" x="60" y="20" class="tw"/><use href="#sp" x="420" y="10" class="tw d1"/><use href="#sp" x="40" y="240" class="tw d2"/><use href="#sp" x="446" y="250" class="tw d3"/>
</svg>'''
open('2_kusahara_shin.svg','w').write(svg)
