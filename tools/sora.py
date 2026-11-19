import math
L='#2b2b3a'
def feather(length,w,fill,tip):
    Lr=length
    p=f'M0 {-w*.55:.1f} L{Lr-w:.1f} {-w:.1f} Q{Lr:.1f} {-w:.1f} {Lr:.1f} 0 Q{Lr:.1f} {w:.1f} {Lr-w:.1f} {w:.1f} L0 {w*.55:.1f} Z'
    t=f'M{Lr*.72:.1f} {-w*.93:.1f} L{Lr-w:.1f} {-w:.1f} Q{Lr:.1f} {-w:.1f} {Lr:.1f} 0 Q{Lr:.1f} {w:.1f} {Lr-w:.1f} {w:.1f} L{Lr*.72:.1f} {w*.93:.1f} Z'
    return (f'<path d="{p}" fill="{fill}" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="{t}" fill="{tip}" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M{length*.08:.1f} 0 L{length*.7:.1f} 0" stroke="#9fc8ea" stroke-width="1.8" stroke-linecap="round"/>')
def wing(x,y,ang,length,n,spread,w,cov,sgn=-1):
    s=f'<g transform="translate({x} {y}) rotate({ang})">'
    cols=['#ffffff','#d6eeff']
    arm=cov*1.05
    items=[]
    for i in range(n):
        t=1-i/(n-1)*0.85          # 1=tip side, 0.15=body side
        bx=arm*t
        an=sgn*spread*(1-t)/0.85
        ln=length*(0.55+0.45*t)
        items.append(f'<g transform="translate({bx:.1f} 0) rotate({an:.1f})">'+feather(ln,w,cols[i%2],'#9fd3ff')+'</g>')
    s+=''.join(reversed(items))
    c=cov
    s+=(f'<path d="M-6 {-c*.30:.1f} Q{c*.5:.1f} {-c*.5:.1f} {c*1.12:.1f} {-c*.06:.1f} '
        f'Q{c*1.1:.1f} {c*.2:.1f} {c*.9:.1f} {c*.14:.1f} Q{c*.78:.1f} {c*.34:.1f} {c*.6:.1f} {c*.2:.1f} '
        f'Q{c*.46:.1f} {c*.4:.1f} {c*.3:.1f} {c*.24:.1f} Q{c*.12:.1f} {c*.4:.1f} -6 {c*.22:.1f} Z" '
        f'fill="#9fd3ff" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>')
    s+=f'<path d="M{c*.1:.1f} {-c*.16:.1f} Q{c*.5:.1f} {-c*.34:.1f} {c:.1f} {-c*.04:.1f}" fill="none" stroke="#ffc94a" stroke-width="3.2" stroke-linecap="round"/>'
    return s+'</g>'
def mirror(s): return f'<g transform="translate(480 0) scale(-1 1)">{s}</g>'

rays=''
for i in range(12):
    a=math.radians(i*30)
    def P(r,da): return (240+r*math.cos(a+da),170+r*math.sin(a+da))
    p1,p2,p3=P(84,-0.11),P(122,0),P(84,0.11)
    rays+=f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} L{p3[0]:.1f} {p3[1]:.1f} Z" fill="#ffd65a" stroke="{L}" stroke-width="2.4" stroke-linejoin="round"/>'

upper=wing(206,258,198,136,6,62,20,90,1)
lower=wing(214,312,170,116,5,50,16,66,-1)
wings=upper+lower

# tail feathers (behind body)
tail=''
for a,ln in [(70,92),(90,104),(110,92)]:
    tail+=f'<g transform="translate(240 350) rotate({a})">'+feather(ln,15,'#d6eeff' if a!=90 else '#ffffff','#9fd3ff')+'</g>'

body=f'''
<path d="M182 262 Q168 316 206 360 Q240 384 274 360 Q312 316 298 262 Q240 236 182 262 Z" fill="#ffffff" stroke="{L}" stroke-width="3.2" stroke-linejoin="round"/>'''
# chest V feathers
for row,(y,xs) in enumerate([(282,[210,240,270]),(304,[198,225,255,282]),(326,[210,240,270]),(348,[225,255])]):
    for x in xs:
        body+=f'<path d="M{x-11} {y} Q{x} {y+12} {x+11} {y}" fill="none" stroke="#9fd3ff" stroke-width="2.4" stroke-linecap="round"/>'

def leg(x):
    s=f'<path d="M{x-8} 362 L{x-7} 392 L{x+7} 392 L{x+8} 362 Z" fill="#ffc94a" stroke="{L}" stroke-width="2.8" stroke-linejoin="round"/>'
    s+=f'<path d="M{x-6} 372 h12 M{x-6} 381 h12" stroke="#e0a020" stroke-width="2" stroke-linecap="round"/>'
    for dx in (-14,0,14):
        s+=f'<path d="M{x} 390 Q{x+dx*0.8} 396 {x+dx} 404" fill="none" stroke="{L}" stroke-width="8" stroke-linecap="round"/>'
        s+=f'<path d="M{x} 390 Q{x+dx*0.8} 396 {x+dx} 404" fill="none" stroke="#ffc94a" stroke-width="4.4" stroke-linecap="round"/>'
        s+=f'<path d="M{x+dx-3} 402 Q{x+dx+1} 410 {x+dx+5} 406" fill="none" stroke="{L}" stroke-width="3.2" stroke-linecap="round"/>'
    return s
legs=leg(222)+leg(258)

# head
head=f'''
<path d="M176 206 L156 222 L180 222 L164 240 L190 234 L184 250 L206 240 Z" fill="#d6eeff" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>
<path d="M304 206 L324 222 L300 222 L316 240 L290 234 L296 250 L274 240 Z" fill="#d6eeff" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>
<path d="M172 196 Q170 134 240 126 Q310 134 308 196 Q306 240 240 252 Q174 240 172 196 Z" fill="#ffffff" stroke="{L}" stroke-width="3.4" stroke-linejoin="round"/>
<path d="M214 130 Q226 112 236 126 M244 126 Q254 112 266 130" fill="none" stroke="{L}" stroke-width="3" stroke-linecap="round"/>
<path d="M200 140 q8 -6 16 0 M264 140 q8 -6 16 0 M232 136 q8 -6 16 0" fill="none" stroke="#9fd3ff" stroke-width="2.4" stroke-linecap="round"/>
<ellipse cx="192" cy="222" rx="10" ry="6" fill="#ffb3c8" opacity=".6"/><ellipse cx="288" cy="222" rx="10" ry="6" fill="#ffb3c8" opacity=".6"/>
'''
def eye(cx,side,id_):
    # side=-1 left, +1 right ; lid slopes down toward center
    if side<0: clip=f'M{cx-22} {178} L{cx+22} {196} L{cx+22} 230 L{cx-22} 230 Z'; lid=f'M{cx-16} {181} L{cx+18} {195}'
    else: clip=f'M{cx-22} {196} L{cx+22} {178} L{cx+22} 230 L{cx-22} 230 Z'; lid=f'M{cx+16} {181} L{cx-18} {195}'
    hx=-5 if side<0 else 5
    return (f'<clipPath id="{id_}"><path d="{clip}"/></clipPath><g clip-path="url(#{id_})">'
            f'<ellipse cx="{cx}" cy="196" rx="14" ry="15" fill="#3fa0ff" stroke="{L}" stroke-width="2.4"/>'
            f'<ellipse cx="{cx}" cy="198" rx="7.5" ry="9" fill="#2a1a12"/>'
            f'<circle cx="{cx+hx}" cy="193" r="3.8" fill="#fff"/><circle cx="{cx-hx*0.6}" cy="203" r="1.9" fill="#fff"/></g>'
            f'<path d="{lid}" stroke="{L}" stroke-width="3.2" stroke-linecap="round"/>')
head+=eye(210,-1,'e4L')+eye(270,1,'e4R')
head+=f'''
<path d="M218 210 Q240 198 262 210 Q264 236 244 258 Q240 263 236 258 Q216 236 218 210 Z" fill="#ffc94a" stroke="{L}" stroke-width="2.8" stroke-linejoin="round"/>
<path d="M236 258 Q240 268 244 258" fill="#e0a020" stroke="{L}" stroke-width="2.4" stroke-linejoin="round"/>
<path d="M222 226 Q240 234 258 226" fill="none" stroke="#c9902f" stroke-width="2.2" stroke-linecap="round"/>
<circle cx="232" cy="214" r="1.8" fill="#c9902f"/><circle cx="248" cy="214" r="1.8" fill="#c9902f"/>
'''

cloud='''<path d="M120 420 q0 -18 20 -18 q8 -16 28 -12 q16 -10 30 6 q24 -2 24 24 Z" fill="#fff" stroke="#2b2b3a" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M258 420 q0 -18 20 -18 q8 -16 28 -12 q16 -10 30 6 q24 -2 24 24 Z" fill="#fff" stroke="#2b2b3a" stroke-width="2.6" stroke-linejoin="round"/>
<path d="M176 420 q4 -22 30 -20 q14 -16 34 -6 q20 -10 34 6 q26 -2 30 20 Z" fill="#fff" stroke="#2b2b3a" stroke-width="2.6" stroke-linejoin="round"/>'''

svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 480 444" width="480" height="444">
<title>そらの ぬし しんの すがた</title>
<style>
  .breathe{{transform-origin:240px 300px;animation:br 3.2s ease-in-out infinite}}
  @keyframes br{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.018,1.03)}}}}
  .sway{{transform-origin:240px 230px;animation:sw 4s ease-in-out infinite}}
  @keyframes sw{{0%,100%{{transform:rotate(-1.2deg)}}50%{{transform:rotate(1.2deg)}}}}
  .flapU{{transform-origin:204px 262px;animation:fu 2.6s ease-in-out infinite}}
  .flapUR{{transform-origin:276px 262px;animation:fur 2.6s ease-in-out infinite}}
  @keyframes fu{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(5deg)}}}}
  @keyframes fur{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-5deg)}}}}
  .glow{{animation:gl 2.4s ease-in-out infinite}}
  .d1{{animation-delay:.6s}}.d2{{animation-delay:1.2s}}.d3{{animation-delay:1.8s}}
  @keyframes gl{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
  .tw{{animation:tw 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
  @keyframes tw{{0%,100%{{opacity:0;transform:scale(.4)}}50%{{opacity:1;transform:scale(1)}}}}
  .spin{{transform-origin:240px 170px;animation:spn 24s linear infinite}}
  @keyframes spn{{to{{transform:rotate(360deg)}}}}
</style>
<defs>
  <filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>
  <path id="sp" d="M0 -6 L1.5 -1.5 L6 0 L1.5 1.5 L0 6 L-1.5 1.5 L-6 0 L-1.5 -1.5 Z" fill="#fffbd0"/>
  <radialGradient id="bg" cx="50%" cy="55%" r="55%"><stop offset="0" stop-color="#cfeaff"/><stop offset=".6" stop-color="#cfeaff" stop-opacity=".5"/><stop offset="1" stop-color="#cfeaff" stop-opacity="0"/></radialGradient>
  <radialGradient id="sun4" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff6b0"/><stop offset="1" stop-color="#ffc94a"/></radialGradient>
</defs>
<!-- はいけいの光 -->
<ellipse cx="240" cy="230" rx="238" ry="205" fill="url(#bg)"/>
<!-- 太陽（せなかの光の輪） -->
<g class="spin">{rays}</g>
<circle cx="240" cy="170" r="80" fill="url(#sun4)" stroke="{L}" stroke-width="3"/>
<circle cx="240" cy="170" r="96" fill="#fff3a0" opacity=".35" filter="url(#soft)" class="glow"/>
<g class="breathe">
<ellipse cx="240" cy="412" rx="160" ry="12" fill="{L}" opacity=".15"/>
<!-- 4まいの つばさ（4の段の ひみつの かず）上2まい・下2まい -->
<g class="flapU">{upper}</g>
<g class="flapUR">{mirror(upper)}</g>
{lower}{mirror(lower)}
<!-- 尾羽 -->
{tail}
<!-- 体（むね板） -->
{body}
<!-- 足と かぎづめ -->
{legs}
</g>
<!-- 頭 -->
<g class="sway">{head}</g>
<!-- 雲 -->
{cloud}
<use href="#sp" x="60" y="40" class="tw"/><use href="#sp" x="420" y="30" class="tw d1"/><use href="#sp" x="30" y="200" class="tw d2"/><use href="#sp" x="450" y="210" class="tw d3"/><use href="#sp" x="240" y="-10" class="tw"/>
</svg>'''
open('/home/claude/work/4_sora_shin.svg','w').write(svg)
