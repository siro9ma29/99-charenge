# 裏ボスの とくべつカードの 絵（art/card/ の WebP）を index.html に うめこむ
#   python3 tools/build_card_art.py
# index.html の「/*UB_CARD_BEGIN*/ 〜 /*UB_CARD_END*/」の あいだを 書きかえる。
# 絵は もとの イラスト（白い はいけい）から はいけいを とり、よこ 440px に ちぢめた WebP（tools/card_cut.py）
import base64, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEYS = {'1': '1_mori', '2': '2_kusahara', '3': '3_umi', '4': '4_sora', '5': '5_kazan', '6': '6_yukiyama',
        '7': '7_yozora', '8': '8_sabaku', '9': '9_dokutsu', 'kd': 'kukudora', 'tk': 'tokikui'}


def main():
    art = {k: 'data:image/webp;base64,' + base64.b64encode((ROOT / 'art/card' / (v + '.webp')).read_bytes()).decode() for k, v in KEYS.items()}
    js = 'const UB_CARD = ' + json.dumps(art, separators=(',', ':')) + ';'
    html_path = ROOT / 'index.html'
    html = html_path.read_text()
    a, b = '/*UB_CARD_BEGIN*/', '/*UB_CARD_END*/'
    i, j = html.index(a), html.index(b)
    html = html[:i + len(a)] + '\n' + js + '\n  ' + html[j:]
    html_path.write_text(html)
    print('UB_CARD', len(js.encode()), 'bytes / index.html', len(html.encode()), 'bytes')


if __name__ == '__main__':
    main()
