# 裏ボス戦の絵（art/ の SVG）を index.html に うめこむ
#   python3 tools/build_ura_art.py
# index.html の「/*UB_ART_BEGIN*/ 〜 /*UB_ART_END*/」の あいだを 書きかえる。
# - しんの すがた 9まい：<img>（Blob URL）で 出すので そのまま（CSS が べつの 文書に なり、名前が ぶつからない）
# - ククドラ・トキクイ：HTML に じかに 入れて 首や 砂を 動かすので、class名・keyframes名に 接頭辞（kd- / tk-）を つける
# - ククドラの 首（class="nk"）に data-n（ひたいの 数字 1〜9）を つける。描く順は 9,1,8,2,7,3,6,4,5（tools/kukudora.py の order）
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHIN = ['1_mori', '2_kusahara', '3_umi', '4_sora', '5_kazan', '6_yukiyama', '7_yozora', '8_sabaku', '9_dokutsu']
NECK_ORDER = [9, 1, 8, 2, 7, 3, 6, 4, 5]


def slim(s):
    s = re.sub(r'<\?xml[^>]*>', '', s)
    s = re.sub(r'<title>.*?</title>', '', s, flags=re.S)
    s = re.sub(r'>\s+<', '><', s)
    s = re.sub(r'<path d="M\s*"[^>]*/>', '', s)   # 点の ない 線(ククドラに 1つ ある。ブラウザが エラーを 出す)
    s = re.sub(r'\n\s*', ' ', s).strip()
    # 形の 座標だけ 小数1けたに（アニメの 数字は そのまま）
    s = re.sub(r'(\sd|\spoints)="([^"]*)"', lambda m: m.group(1) + '="' + re.sub(r'(\d+\.\d)\d+', r'\1', m.group(2)) + '"', s)
    s = re.sub(r'(transform-origin:)(-?\d+\.\d)\d+', r'\1\2', s)
    return s


def ns(s, p):
    """class名と keyframes名に 接頭辞を つける"""
    classes = set()
    for m in re.finditer(r'class="([^"]*)"', s):
        classes.update(m.group(1).split())
    style = re.search(r'<style>(.*?)</style>', s, flags=re.S)
    css = style.group(1) if style else ''
    classes.update(re.findall(r'\.([A-Za-z_][\w-]*)', css))
    frames = set(re.findall(r'@keyframes\s+([\w-]+)', css))
    for c in sorted(classes, key=len, reverse=True):
        css = re.sub(r'\.' + re.escape(c) + r'(?![\w-])', '.' + p + c, css)
    for f in frames:
        css = re.sub(r'@keyframes\s+' + re.escape(f) + r'(?![\w-])', '@keyframes ' + p + f, css)
        css = re.sub(r'(animation(?:-name)?\s*:\s*)' + re.escape(f) + r'(?![\w-])', r'\1' + p + f, css)
    if style:
        s = s[:style.start(1)] + css + s[style.end(1):]
    s = re.sub(r'class="([^"]*)"', lambda m: 'class="' + ' '.join(p + c for c in m.group(1).split()) + '"', s)
    return s


def boss(name, p):
    s = slim((ROOT / 'art/boss' / (name + '.svg')).read_text())
    s = re.sub(r'\s(width|height)="\d+"', '', s, count=2)
    s = ns(s, p)
    if name == 'kukudora':
        it = iter(NECK_ORDER)
        s = re.sub(r'<g class="kd-nk"', lambda m: '<g class="kd-nk" data-n="' + str(next(it)) + '"', s)
    return s


def main():
    art = {
        'shin': [slim((ROOT / 'art/shin' / (n + '_shin.svg')).read_text()) for n in SHIN],
        'kd': boss('kukudora', 'kd-'),
        'tk': boss('tokikui', 'tk-'),
    }
    js = 'const UB_ART = ' + json.dumps(art, ensure_ascii=False, separators=(',', ':')) + ';'
    assert '</script' not in js
    html_path = ROOT / 'index.html'
    html = html_path.read_text()
    a, b = '/*UB_ART_BEGIN*/', '/*UB_ART_END*/'
    i, j = html.index(a), html.index(b)
    html = html[:i + len(a)] + '\n' + js + '\n  ' + html[j:]
    html_path.write_text(html)
    print('UB_ART', len(js.encode()), 'bytes / index.html', len(html.encode()), 'bytes')


if __name__ == '__main__':
    main()
