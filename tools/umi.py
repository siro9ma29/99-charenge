import math
L='#2b2b3a'
def tube(d,w):
    return (f'<path d="{d}" fill="none" stroke="{L}" stroke-width="{w+7}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="url(#body)" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#e9f8ff" stroke-width="{w*.22:.1f}" stroke-linecap="round" opacity=".55"/>')
def spike(x,y,ang,s=1):
    return f'<path d="M{-9*s:.1f} 0 L0 {-22*s:.1f} L{9*s:.1f} 0 Z" transform="translate({x} {y}) rotate({ang})" fill="#7fe0e8" stroke="{L}" stroke-width="2.6" stroke-linejoin="round"/>'
def fin(ln,w):
    return (f'<path d="M0 0 C{w*1.1:.1f} {-ln*.35:.1f} {w:.1f} {-ln*.85:.1f} 0 {-ln} C{-w:.1f} {-ln*.85:.1f} {-w*1.1:.1f} {-ln*.35:.1f} 0 0 Z" fill="#7fe0e8" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="M0 -4 Q{w*.55:.1f} {-ln*.45:.1f} {w*.5:.1f} {-ln*.8:.1f} M0 -4 L0 {-ln*.9:.1f} M0 -4 Q{-w*.55:.1f} {-ln*.45:.1f} {-w*.5:.1f} {-ln*.8:.1f}" fill="none" stroke="#3fb5c4" stroke-width="2.2" stroke-linecap="round"/>')
tailD="M352 404 C336 330 426 318 428 236 C430 180 396 160 398 110"
tail=tube(tailD,40)
for (x,y,a) in [(350,344,-60),(392,316,-40),(420,272,-10),(424,214,10),(410,170,30)]:
    tail=spike(x+14,y,a+90,1)+tail if False else tail
def bez(p0,p1,p2,p3,t):
    u=1-t; return tuple(u**3*p0[i]+3*u*u*t*p1[i]+3*u*t*t*p2[i]+t**3*p3[i] for i in range(2))
segs=[((352,404),(336,330),(426,318),(428,236)),((428,236),(430,180),(396,160),(398,110))]
spikes=''
for seg,ts in [(segs[0],(.45,.7,.92)),(segs[1],(.3,.62))]:
    for t in ts:
        p=bez(*seg,t); q=bez(*seg,t+.01)
        dx,dy=q[0]-p[0],q[1]-p[1]; n=math.hypot(dx,dy); nx,ny=dy/n,-dx/n
        if nx<0: nx,ny=-nx,-ny
        ang=math.degrees(math.atan2(nx,-ny))
        spikes+=spike(p[0]+nx*18,p[1]+ny*18,ang,1.1)
fluke=f'<g transform="translate(398 112)">'+''.join(f'<g transform="rotate({a})">{fin(74 if a==0 else 66,26)}</g>' for a in (-52,0,52))+f'<circle r="16" fill="url(#body)" stroke="{L}" stroke-width="3"/></g>'
coil=tube("M44 420 C52 318 170 312 176 420",38)
coilsp=''.join(spike(x,y,a,.9) for x,y,a in [(66,346,-40),(108,318,0),(152,342,40)])
neck=f'''<path d="M176 420 C180 340 184 280 194 232 L286 232 C296 280 300 340 304 420 Z" fill="url(#body)" stroke="{L}" stroke-width="3.4" stroke-linejoin="round"/>
<path d="M212 420 C214 350 216 290 222 240 L258 240 C264 290 266 350 268 420 Z" fill="#e9f8ff" stroke="{L}" stroke-width="2.4" stroke-linejoin="round"/>
'''+''.join(f'<path d="M{217} {y} Q240 {y+8} {263} {y}" fill="none" stroke="#9fd3ff" stroke-width="2.2" stroke-linecap="round"/>' for y in range(262,420,22))
flipL=f'''<g transform="translate(194 312) rotate(-14) scale(1.6) translate(-204 -340)"><path d="M206 340 C182 316 134 314 108 344 C126 346 140 352 146 362 C156 352 170 352 178 362 C186 352 194 348 206 348 Z" fill="#7fe0e8" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>
<path d="M204 343 C176 332 142 332 118 344" fill="none" stroke="#3fb5c4" stroke-width="2" stroke-linecap="round"/>
<path d="M108 344 l-10 6 l12 0 Z M146 362 l-6 10 l10 -4 Z M178 362 l-4 10 l8 -6 Z" fill="#fff" stroke="{L}" stroke-width="2" stroke-linejoin="round"/></g>'''
def mir(s): return f'<g transform="translate(480 0) scale(-1 1)">{s}</g>'
def eye(cx,cy,side,id_):
    if side<0: clip=f'M{cx-26} {cy-22} L{cx+26} {cy+2} L{cx+26} {cy+9} Q{cx} {cy+14} {cx-26} {cy+6} Z'; lid=f'M{cx-20} {cy-19} L{cx+22} {cy+1}'
    else: clip=f'M{cx-26} {cy+2} L{cx+26} {cy-22} L{cx+26} {cy+6} Q{cx} {cy+14} {cx-26} {cy+9} Z'; lid=f'M{cx+20} {cy-19} L{cx-22} {cy+1}'
    hx=-4 if side<0 else 4
    return (f'<clipPath id="{id_}"><path d="{clip}"/></clipPath><g clip-path="url(#{id_})">'
            f'<ellipse cx="{cx}" cy="{cy}" rx="16" ry="15" fill="#ffd34a" stroke="{L}" stroke-width="2.4"/>'
            f'<ellipse cx="{cx}" cy="{cy+1}" rx="3.4" ry="10" fill="#2a1a12"/>'
            f'<circle cx="{cx+hx}" cy="{cy-2}" r="2.6" fill="#fff"/></g>'
            f'<path d="{clip}" fill="none" stroke="{L}" stroke-width="2.2" stroke-linejoin="round"/>'
            f'<path d="{lid}" stroke="{L}" stroke-width="3.8" stroke-linecap="round"/>')
hy=176
earfin=f'<path d="M182 {hy} L140 {hy-132} L133 {hy-107} Z" fill="#7fe0e8"/><path d="M182 {hy} L133 {hy-107} L108 {hy-121} Z" fill="#a8eef3"/><path d="M182 {hy} L108 {hy-121} L106 {hy-94} Z" fill="#5fcfdc"/><path d="M182 {hy} L106 {hy-94} L77 {hy-99} Z" fill="#7fe0e8"/><path d="M182 {hy} L77 {hy-99} L82 {hy-71} Z" fill="#7fe0e8"/><path d="M182 {hy} L82 {hy-71} L52 {hy-68} Z" fill="#a8eef3"/><path d="M182 {hy} L52 {hy-68} L64 {hy-40} Z" fill="#5fcfdc"/><path d="M182 {hy} L64 {hy-40} L34 {hy-27} Z" fill="#7fe0e8"/><path d="M182 {hy} L34 {hy-27} L59 {hy-3} Z" fill="#7fe0e8"/><path d="M182 {hy} L59 {hy-3} L40 {hy+18} Z" fill="#a8eef3"/><path d="M182 {hy} L40 {hy+18} L68 {hy+32} Z" fill="#5fcfdc"/><path d="M182 {hy} L68 {hy+32} L55 {hy+57} Z" fill="#7fe0e8"/><path d="M182 {hy} L55 {hy+57} L85 {hy+62} Z" fill="#7fe0e8"/><path d="M182 {hy} L85 {hy+62} L79 {hy+89} Z" fill="#a8eef3"/><path d="M182 {hy} L79 {hy+89} L107 {hy+85} Z" fill="#5fcfdc"/><path d="M182 {hy} L107 {hy+85} L107 {hy+111} Z" fill="#7fe0e8"/><path d="M182 {hy} L140 {hy-132} M182 {hy} L108 {hy-121} M182 {hy} L77 {hy-99} M182 {hy} L52 {hy-68} M182 {hy} L34 {hy-27} M182 {hy} L40 {hy+18} M182 {hy} L55 {hy+57} M182 {hy} L79 {hy+89} M182 {hy} L107 {hy+111}" stroke="#3fb5c4" stroke-width="2.2" stroke-linecap="round"/><path d="M182 {hy-18} L140 {hy-132} L133 {hy-107} L108 {hy-121} L106 {hy-94} L77 {hy-99} L82 {hy-71} L52 {hy-68} L64 {hy-40} L34 {hy-27} L59 {hy-3} L40 {hy+18} L68 {hy+32} L55 {hy+57} L85 {hy+62} L79 {hy+89} L107 {hy+85} L107 {hy+111} L184 {hy+20} Z" fill="none" stroke="{L}" stroke-width="3.2" stroke-linejoin="miter"/>'
def mkhorn():
    P0,P1,P2,P3=(214,-44),(204,-96),(176,-112),(152,-132)
    def bz(t):
        u=1-t; return [u**3*P0[i]+3*u*u*t*P1[i]+3*u*t*t*P2[i]+t**3*P3[i] for i in range(2)]
    N=24; left=[];right=[];norms=[]
    for k in range(N+1):
        t=k/N; p=bz(t); q=bz(min(t+.01,1)) if t<1 else p; r=bz(t-.01) if t>0 else p
        dx,dy=q[0]-r[0],q[1]-r[1]; n=math.hypot(dx,dy) or 1; nx,ny=-dy/n,dx/n
        w=15*(1-t)**0.8+1.2
        left.append((p[0]+nx*w,p[1]+ny*w)); right.append((p[0]-nx*w,p[1]-ny*w)); norms.append((p,nx,ny,w))
    pts=left+right[::-1]
    d='M'+' L'.join(f'{x:.1f} {{hy+{y:.1f}}}' for x,y in pts)+' Z'
    rings=''
    for t in (.2,.38,.54,.68,.8):
        p,nx,ny,w=norms[int(t*N)]
        rings+=f'M{p[0]+nx*w:.1f} {{hy+{p[1]+ny*w:.1f}}} Q{p[0]+(P3[0]-P0[0])*0.02:.1f} {{hy+{p[1]+4:.1f}}} {p[0]-nx*w:.1f} {{hy+{p[1]-ny*w:.1f}}} '
    return (f'<path d="{d}" fill="#fff6c8" stroke="{{L}}" stroke-width="3" stroke-linejoin="round"/>'
            f'<path d="{rings}" fill="none" stroke="#c9b27a" stroke-width="2.6" stroke-linecap="round"/>')
horn=eval("f'"+mkhorn().replace("{hy+-","{hy-")+"'")
head=f'''{earfin}{mir(earfin)}{horn}{mir(horn)}
<path d="M226 {hy-58} L240 {hy-92} L254 {hy-58} Z" fill="#7fe0e8" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>

<path d="M206 {hy+68}Q240 {hy+84} 274 {hy+68}L272 {hy+110}Q240 {hy+126} 208 {hy+110}Z" fill="#7a2240" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>
<path d="M222 {hy+108}Q240 {hy+92} 258 {hy+108}Q240 {hy+120} 222 {hy+108}Z" fill="#ff7aa8"/>
<path d="M205 {hy+104}Q240 {hy+126} 275 {hy+104}L277 {hy+116}Q240 {hy+142} 203 {hy+116}Z" fill="url(#body)" stroke="{L}" stroke-width="3" stroke-linejoin="round"/>
<path d="M215 {hy+110}l5 -20l6 22ZM254 {hy+112}l6 -22l5 20Z" fill="#fff" stroke="{L}" stroke-width="2.2" stroke-linejoin="round"/>
<path d="M180 {hy} C178 {hy-38} 184 {hy-54} 208 {hy-56} L272 {hy-56} C296 {hy-54} 302 {hy-38} 300 {hy} C299 {hy+22} 284 {hy+34} 276 {hy+52} L204 {hy+52} C196 {hy+34} 181 {hy+22} 180 {hy} Z" fill="none" stroke="{L}" stroke-width="6.8" stroke-linejoin="round"/><path d="M205 {hy+12}C203 {hy+40} 208 {hy+56} 215 {hy+62}L265 {hy+62}C272 {hy+56} 277 {hy+40} 275 {hy+12}Q240 {hy} 205 {hy+12}Z" fill="none" stroke="{L}" stroke-width="6.8" stroke-linejoin="round"/><path d="M198 {hy+62}Q196 {hy+44} 240 {hy+42}Q284 {hy+44} 282 {hy+62}Q280 {hy+80} 240 {hy+82}Q200 {hy+80} 198 {hy+62}Z" fill="none" stroke="{L}" stroke-width="6.8" stroke-linejoin="round"/><path d="M180 {hy} C178 {hy-38} 184 {hy-54} 208 {hy-56} L272 {hy-56} C296 {hy-54} 302 {hy-38} 300 {hy} C299 {hy+22} 284 {hy+34} 276 {hy+52} L204 {hy+52} C196 {hy+34} 181 {hy+22} 180 {hy} Z" fill="url(#hg)"/><path d="M205 {hy+12}C203 {hy+40} 208 {hy+56} 215 {hy+62}L265 {hy+62}C272 {hy+56} 277 {hy+40} 275 {hy+12}Q240 {hy} 205 {hy+12}Z" fill="url(#hg)"/><path d="M198 {hy+62}Q196 {hy+44} 240 {hy+42}Q284 {hy+44} 282 {hy+62}Q280 {hy+80} 240 {hy+82}Q200 {hy+80} 198 {hy+62}Z" fill="url(#hg)"/><path d="M206 {hy+50}Q240 {hy+36} 274 {hy+50}" fill="none" stroke="#2e6cc8" stroke-width="2" stroke-linecap="round" opacity=".45"/>
<path d="M226 {hy+24} q14 -6 28 0 M229 {hy+38} q11 -5 22 0" fill="none" stroke="#9fd3ff" stroke-width="2.4" stroke-linecap="round"/>

<path d="M208 {hy+58}q3 -12 15 -10q-7 4 -5 12ZM272 {hy+58}q-3 -12 -15 -10q7 4 5 12Z" fill="{L}"/>
<path d="M211 {hy+76}l5 26l7 -24ZM257 {hy+78}l7 24l5 -26Z" fill="#fff" stroke="{L}" stroke-width="2.2" stroke-linejoin="round"/>
<path d="M186 {hy-36} q10 -8 22 -2 M272 {hy-38} q12 -6 22 2" fill="none" stroke="#9fd3ff" stroke-width="2.4" stroke-linecap="round"/>
{eye(208,hy-8,-1,'e3L')}{eye(272,hy-8,1,'e3R')}
<path d="M204 {hy+64} C176 {hy+64} 142 {hy+86} 148 {hy+122} C150 {hy+136} 164 {hy+136} 164 {hy+124} M276 {hy+64} C304 {hy+64} 338 {hy+86} 332 {hy+122} C330 {hy+136} 316 {hy+136} 316 {hy+124}" fill="none" stroke="#7fe0e8" stroke-width="4.4" stroke-linecap="round"/>
'''
water=f'''<path d="M0 392 Q30 378 60 392 T120 392 T180 392 T240 392 T300 392 T360 392 T420 392 T480 392 L480 420 L0 420 Z" fill="url(#sea)" stroke="{L}" stroke-width="2.6"/>
<path d="M0 404 Q30 396 60 404 T120 404 T180 404 T240 404 T300 404 T360 404 T420 404 T480 404" fill="none" stroke="#fff" stroke-width="2.4" opacity=".8"/>
<circle cx="90" cy="380" r="6" fill="#fff" stroke="{L}" stroke-width="2"/><circle cx="330" cy="376" r="5" fill="#fff" stroke="{L}" stroke-width="2"/><circle cx="380" cy="384" r="4" fill="#fff" stroke="{L}" stroke-width="2"/>'''
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -24 480 444" width="480" height="444">
<title>うみの ぬし しんの すがた</title>
<style>
  .sway{{transform-origin:240px 300px;animation:sw 4s ease-in-out infinite}}
  @keyframes sw{{0%,100%{{transform:rotate(-1.4deg)}}50%{{transform:rotate(1.4deg)}}}}
  .wag{{transform-origin:360px 400px;animation:wg 3.4s ease-in-out infinite}}
  @keyframes wg{{0%,100%{{transform:rotate(-2deg)}}50%{{transform:rotate(2deg)}}}}
  .wave{{animation:wv 3s ease-in-out infinite}}
  @keyframes wv{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(-8px)}}}}
  .tw{{animation:tw 1.8s ease-in-out infinite;transform-box:fill-box;transform-origin:center}}
  .d1{{animation-delay:.6s}}.d2{{animation-delay:1.2s}}.d3{{animation-delay:1.8s}}
  @keyframes tw{{0%,100%{{opacity:0;transform:scale(.4)}}50%{{opacity:1;transform:scale(1)}}}}
</style>
<defs>
  <path id="sp" d="M0 -6 L1.5 -1.5 L6 0 L1.5 1.5 L0 6 L-1.5 1.5 L-6 0 L-1.5 -1.5 Z" fill="#fffbd0"/>
  <radialGradient id="bg" cx="50%" cy="55%" r="55%"><stop offset="0" stop-color="#d4f1ff"/><stop offset=".6" stop-color="#d4f1ff" stop-opacity=".5"/><stop offset="1" stop-color="#d4f1ff" stop-opacity="0"/></radialGradient>
  <linearGradient id="body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5aa8ff"/><stop offset="1" stop-color="#2e6cc8"/></linearGradient>
  <linearGradient id="hg" gradientUnits="userSpaceOnUse" x1="0" y1="100" x2="0" y2="270"><stop offset="0" stop-color="#5aa8ff"/><stop offset="1" stop-color="#3a7fda"/></linearGradient>
  <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fdcff"/><stop offset="1" stop-color="#e8f4ff"/></linearGradient>
</defs>
<!-- はいけいの光 -->
<ellipse cx="240" cy="230" rx="238" ry="205" fill="url(#bg)"/>
<!-- しっぽ（先が 3つに わかれた ひれ＝3の段の ひみつの かず） -->
<g class="wag">{spikes}{tail}{fluke}</g>
<!-- うしろの とぐろ -->
{coilsp}{coil}
<!-- 首と 体 -->
<g class="sway">{neck}{flipL}{mir(flipL)}
<!-- 頭 -->
{head}</g>
<!-- 海 -->
<g class="wave">{water}</g>
<use href="#sp" x="60" y="40" class="tw"/><use href="#sp" x="300" y="10" class="tw d1"/><use href="#sp" x="30" y="220" class="tw d2"/><use href="#sp" x="120" y="120" class="tw d3"/>
</svg>'''
open('3_umi_shin.svg','w').write(svg)
