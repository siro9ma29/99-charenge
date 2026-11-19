# とくべつカードの 絵：白い はいけいを とって、よこ 440px の WebP に する
#   python3 tools/card_cut.py もとの絵.jpg art/card/1_mori.webp 62
import sys, numpy as np
from PIL import Image
from scipy import ndimage
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB'); a = np.asarray(im).astype(int)
white = (a.min(axis=2) > 232) & ((a.max(axis=2)-a.min(axis=2)) < 22)
lab, n = ndimage.label(white)
edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:,0], lab[:,-1]]))) - {0}
bg = np.isin(lab, list(edge))
# かこまれた 白い すきま(背景の のこり)も とる。白っぽい 体(グリフォンの むね)は 色が すこし あるので のこる
w2 = a.min(axis=2) > 240
lab2, n2 = ndimage.label(w2)
e2 = set(np.unique(np.concatenate([lab2[0], lab2[-1], lab2[:,0], lab2[:,-1]])))
for i in range(1, n2+1):
    if i in e2: continue
    m = lab2 == i
    if m.sum() > 300 and a[m].mean(axis=0).min() >= 251: bg |= m
# 外がわの ふちの うすい色(にじみ)も すこし とりのぞく
near = ndimage.binary_dilation(bg, iterations=2) & (a.min(axis=2) > 205)
bg = bg | near
alpha = np.where(bg, 0, 255).astype(np.uint8)
alpha = ndimage.gaussian_filter(alpha.astype(float), 0.6).clip(0,255).astype(np.uint8)
alpha[bg & (ndimage.binary_erosion(bg, iterations=2))] = 0
rgba = np.dstack([np.asarray(im), alpha])
ys, xs = np.where(alpha > 20)
pad = 6
box = (max(xs.min()-pad,0), max(ys.min()-pad,0), min(xs.max()+pad, a.shape[1]), min(ys.max()+pad, a.shape[0]))
out = Image.fromarray(rgba, 'RGBA').crop(box)
out.thumbnail((440, 440), Image.LANCZOS)
out.save(dst, 'WEBP', quality=int(sys.argv[3]) if len(sys.argv)>3 else 70, method=6)
print(dst, out.size)
