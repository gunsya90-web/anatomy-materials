#!/usr/bin/env python3
"""구조물별 SVG 부품을 만들고 조립 뷰어(arm_assembly.html)를 생성한다.

모든 부품은 같은 좌표계(viewBox 0 0 680 700)를 공유하므로 겹쳐 놓기만 하면 조립된다.
출력: game/parts/*.svg (부품 1개 = 파일 1개), game/parts/parts.json, game/samples/arm_assembly.html
"""
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
VB = '0 0 680 700'
DARK = '#6E1E1C'; BONE_S = '#8F7F55'

DEFS = '''<linearGradient id="bone" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FBF6E6"/><stop offset=".5" stop-color="#EADFBE"/><stop offset="1" stop-color="#B9A97C"/></linearGradient>
<linearGradient id="cart" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E4EEF2"/><stop offset="1" stop-color="#B7C9D3"/></linearGradient>
<linearGradient id="mus" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E88F82"/><stop offset=".55" stop-color="#C95C53"/><stop offset="1" stop-color="#93312E"/></linearGradient>
<linearGradient id="mus2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F0A094"/><stop offset=".6" stop-color="#D86B60"/><stop offset="1" stop-color="#9F3733"/></linearGradient>
<linearGradient id="mus3" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#D9776C"/><stop offset=".6" stop-color="#B34842"/><stop offset="1" stop-color="#7E2926"/></linearGradient>
<linearGradient id="tend" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#F4EEDF"/><stop offset="1" stop-color="#CFC4A6"/></linearGradient>
<linearGradient id="hl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#A9DAFF"/><stop offset=".55" stop-color="#3D93EA"/><stop offset="1" stop-color="#1B55A8"/></linearGradient>
<filter id="sh" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="1.5" dy="2.5" stdDeviation="2.5" flood-color="#3a1210" flood-opacity=".4"/></filter>'''

def bone(d, extra=''):
    return f'<path class="f" d="{d}" fill="url(#bone)" stroke="{BONE_S}" stroke-width="1.6" stroke-linejoin="round"/>{extra}'
def line(d, w, c, op=1, cls=''):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round" class="{cls}"/>'
def shade(d, w=2.5, op=.35):  return line(d, w, '#5A4A22', op)
def gloss(d, w=4, op=.5):     return line(d, w, '#fff', op)
def fibers(clip, d, op=.4):
    return f'<g clip-path="url(#{clip})" fill="none" stroke="{DARK}" stroke-opacity="{op}" stroke-width="1.1" stroke-linecap="round">{d}</g>'
def fan(src, pts):
    return ''.join(f'<path d="M{src[0]} {src[1]} Q{(src[0]+x)/2+dx} {(src[1]+y)/2+dy} {x} {y}"/>' for x, y, dx, dy in pts)
def lerp(a, b, t): return a + (b - a) * t

parts = []   # (id, ko, en, layer, note, inner_svg)
def add(id, ko, en, layer, note, inner): parts.append(dict(id=id, ko=ko, en=en, layer=layer, note=note, svg=inner))

# ───────── 뼈 ─────────
add('scapula', '어깨뼈', 'Scapula (acromion · coracoid)', 'bone',
    '봉우리(어깨봉우리)는 빗장뼈와 어깨봉우리빗장관절을, 부리돌기는 작은가슴근 · 위팔두갈래근 짧은갈래가 붙습니다.',
    bone('M146 94 C158 80 192 76 210 84 C218 98 204 112 192 116 C188 134 182 152 168 156 C152 152 148 138 152 126 C138 118 136 104 146 94 Z')
    + shade('M160 100 C176 94 194 94 204 98') + gloss('M152 100 C158 90 176 84 196 84', 3, .55)
    + '<ellipse cx="172" cy="150" rx="9" ry="6" fill="#E6D9B2" stroke="#8F7F55" stroke-width="1.2" transform="rotate(-20 172 150)"/>')

rib_svg = ''
for i in range(7):
    y = 100 + 30 * i
    rib_svg += line(f'M330 {y} C310 {y+6} 286 {y+14} 266 {y+24}', 9, '#8EA3AE') + line(f'M330 {y} C310 {y+6} 286 {y+14} 266 {y+24}', 7, '#D5E3EA') + gloss(f'M326 {y-1.5} C308 {y+4} 288 {y+12} 270 {y+21}', 1.6, .7)
    rib_svg += line(f'M266 {y+24} C240 {y+34} 218 {y+52} 198 {y+84}', 11, BONE_S) + line(f'M266 {y+24} C240 {y+34} 218 {y+52} 198 {y+84}', 9, '#EADFBE') + gloss(f'M264 {y+21} C240 {y+31} 218 {y+48} 198 {y+78}', 2, .55)
add('ribs', '갈비뼈', 'Ribs (1–7, true ribs)', 'bone', '참갈비뼈는 갈비연골을 통해 복장뼈에 직접 붙는 1–7번 갈비뼈입니다(밝은 청회색이 갈비연골).', rib_svg.replace('<path d', '<path class="f"', 0))

add('sternum', '복장뼈', 'Sternum', 'bone', '복장뼈자루 · 복장뼈몸통 · 칼돌기로 구성되며, 자루와 몸통 사이가 복장뼈각입니다.',
    bone('M324 70 C334 66 352 66 362 70 C366 80 364 94 362 104 L366 112 L366 296 L356 318 L348 356 L342 356 L334 318 L324 296 Z')
    + shade('M326 104 H366', 2) + shade('M334 70 Q344 84 354 70', 2, .5)
    + shade('M324 150 H364 M324 196 H364 M324 242 H364', 1.2, .22) + gloss('M328 120 V290', 3, .55))

add('clavicle', '빗장뼈', 'Clavicle', 'bone', '팔이음뼈를 몸통에 연결하는 유일한 뼈. 가운데 1/3에서 골절이 잦습니다.',
    line('M328 76 C300 50 268 72 238 62 C206 54 176 76 154 100', 15, BONE_S) + line('M328 76 C300 50 268 72 238 62 C206 54 176 76 154 100', 12.5, '#E8DCB8', cls='ps')
    + gloss('M326 72 C300 46 268 68 238 58 C208 50 180 72 158 96', 2.6, .6)
    + '<ellipse class="f" cx="329" cy="77" rx="12" ry="10" fill="url(#bone)" stroke="#8F7F55" stroke-width="1.4"/>'
    + '<ellipse class="f" cx="153" cy="100" rx="12" ry="7" transform="rotate(-38 153 100)" fill="url(#bone)" stroke="#8F7F55" stroke-width="1.4"/>')

add('humerus', '위팔뼈', 'Humerus', 'bone', '큰결절 · 작은결절 사이가 결절사이고랑. 외과목 골절은 겨드랑신경, 몸통 골절은 노신경 손상을 주의합니다.',
    bone('M112 112 C118 100 142 100 148 116 C152 130 144 144 136 148 C131 172 129 200 128 240 C127 300 126 356 130 394 L142 410 C146 424 136 438 122 440 C110 444 98 440 92 432 C88 422 94 412 98 402 C101 360 99 300 99 252 C97 216 97 190 97 164 C94 140 100 120 112 112 Z',
         '<ellipse class="f" cx="140" cy="408" rx="8" ry="7" fill="url(#bone)" stroke="#8F7F55" stroke-width="1.2"/>')
    + shade('M98 152 C112 162 126 160 136 150', 2, .4)                    # 해부목
    + shade('M117 152 C115 190 113 214 113 234', 2.6, .4)                 # 결절사이고랑
    + shade('M100 224 C107 234 109 246 107 258', 3.4, .38)                # 어깨세모근거친면
    + shade('M110 388 C114 398 124 398 128 390', 2, .35) + shade('M114 424 C122 432 122 438 114 440', 1.8, .4)
    + gloss('M104 160 C102 220 103 300 104 392', 3.2, .55) + gloss('M114 106 C124 100 138 102 142 112', 2.4, .6))

add('radius', '노뼈', 'Radius', 'bone', '엄지쪽 아래팔뼈. 먼쪽 끝 골절은 콜레스 골절입니다.',
    bone('M88 438 C86 428 108 424 112 436 C112 442 108 446 105 452 C100 520 92 580 91 612 C94 618 100 624 102 632 C96 648 78 654 66 648 C62 640 66 632 72 628 C78 600 84 540 90 472 C90 460 89 448 88 438 Z',
         '<path d="M70 646 L64 654 L72 652Z" fill="#E1D4AC" stroke="#8F7F55"/>')
    + gloss('M92 462 C88 520 82 580 77 620', 2.6, .55) + shade('M92 436 C98 440 106 438 109 436', 1.6, .35))

add('ulna', '자뼈', 'Ulna', 'bone', '새끼쪽 아래팔뼈. 팔꿈치머리가 팔꿈치 뒤로 튀어나옵니다.',
    bone('M118 428 C112 414 130 406 140 416 C144 426 140 440 136 454 C132 520 122 580 114 618 L116 632 C110 642 96 640 94 632 C94 624 98 620 100 614 C106 578 110 520 112 464 C112 450 118 440 118 428 Z')
    + gloss('M126 440 C124 520 114 580 106 620', 2.6, .5) + shade('M118 428 C124 436 132 436 138 428', 1.6, .35))

# ───────── 근육 ─────────
PEC = 'M322 76 C290 62 240 70 192 98 C166 112 150 130 148 148 C190 176 255 214 322 296 L330 296 L328 76 Z'
DEL = 'M206 90 C160 76 110 94 98 140 C90 176 100 202 112 238 C130 206 152 176 166 150 C176 124 196 106 206 90 Z'
BIC = 'M140 200 C168 250 162 340 128 410 L104 414 C90 340 90 262 108 210 C116 198 128 194 140 200 Z'
pec_pts = [(lerp(322, 215, i/9), lerp(74, 92, i/9), 0, -6) for i in range(10)] + [(326, lerp(90, 300, i/12), -4, 4) for i in range(13)]
del_pts = [(lerp(205, 100, i/10), lerp(92, 128, i/10), 6, 0) for i in range(11)]
bic_f = ''.join(f'<path d="M{lerp(112,142,t):.1f} 206 C{lerp(94,166,t):.1f} 270 {lerp(94,160,t):.1f} 340 {lerp(104,128,t):.1f} 410"/>' for t in [i/8 for i in range(9)])

def muscle(id, d, grad, extra=''):
    return f'<defs><clipPath id="c-{id}"><path d="{d}"/></clipPath></defs><path class="f" d="{d}" fill="url(#{grad})" stroke="{DARK}" stroke-width="1.4" filter="url(#sh)"/>{extra}'

add('brachialis', '위팔근', 'Brachialis', 'muscle', '근육피부신경(일부 노신경) 지배. 팔꿈치 굽힘의 주동근이며 위팔두갈래근 아래에 놓입니다.',
    muscle('brachialis', 'M96 250 C82 300 86 360 102 410 L114 406 C104 350 100 290 108 240 Z', 'mus3'))
add('flexors', '아래팔 굽힘근', 'Forearm flexors', 'muscle', '대부분 정중신경, 자쪽손목굽힘근과 깊은손가락굽힘근 안쪽 절반은 자신경 지배.',
    muscle('flexors', 'M104 420 C122 440 128 520 110 642 L86 642 C72 540 80 470 94 424 Z', 'mus3',
           fibers('c-flexors', ''.join(f'<path d="M{lerp(112,100,t):.1f} 440 C{lerp(120,100,t):.1f} 520 {lerp(110,96,t):.1f} 590 {lerp(104,94,t):.1f} 640"/>' for t in [i/6 for i in range(7)]), .3)))
add('brachioradialis', '위팔노근', 'Brachioradialis', 'muscle', '노신경 지배. 팔꿈치 굽힘(중립 위치에서). 노신경이 지배하는 굽힘근입니다.',
    muscle('brachioradialis', 'M90 424 C62 470 60 560 70 642 L84 642 C82 560 84 486 100 428 Z', 'mus2') + gloss('M84 450 C70 500 68 570 74 630', 3, .25))
add('pronator', '원엎침근', 'Pronator teres', 'muscle', '정중신경 지배. 아래팔 엎침(안쪽돌림)과 팔꿈치 굽힘.',
    line('M120 426 C108 450 96 480 86 510', 13, DARK) + line('M120 426 C108 450 96 480 86 510', 10.5, 'url(#mus)', cls='f').replace('stroke="url(#mus)"', 'stroke="#C95C53"'))
add('pec', '큰가슴근', 'Pectoralis major', 'muscle', '안쪽·가쪽 가슴근신경 지배. 팔의 굽힘 · 모음 · 안쪽돌림.',
    muscle('pec', PEC, 'mus', fibers('c-pec', fan((152, 150), pec_pts))))
add('biceps', '위팔두갈래근', 'Biceps brachii', 'muscle', '근육피부신경 지배. 아래팔 뒤침과 팔꿈치 굽힘. 힘줄은 노뼈거친면에 붙습니다.',
    line('M116 410 C112 424 108 436 104 450', 9, '#B8AB88') + line('M116 410 C112 424 108 436 104 450', 7, '#EDE6D2')
    + muscle('biceps', BIC, 'mus2', fibers('c-biceps', bic_f, .38)) + gloss('M120 214 C132 250 136 300 126 350', 5, .28))
add('deltoid', '삼각근', 'Deltoid', 'muscle', '겨드랑신경 지배. 팔 가쪽 벌림의 주동근입니다.',
    muscle('deltoid', DEL, 'mus2', fibers('c-deltoid', fan((113, 236), del_pts), .45)) + gloss('M178 104 C150 100 120 118 110 150', 5, .3))

Z = ['scapula', 'ribs', 'sternum', 'radius', 'ulna', 'humerus', 'clavicle', 'brachialis', 'flexors', 'brachioradialis', 'pronator', 'pec', 'biceps', 'deltoid']
parts.sort(key=lambda p: Z.index(p['id']))
LABEL_ANCHOR = {}  # (생략: 표시선은 뷰어에서 처리)

def wrap(p):
    return (f'<g class="part" id="p-{p["id"]}" data-id="{p["id"]}" data-layer="{p["layer"]}" data-ko="{p["ko"]}" data-en="{p["en"]}">'
            f'<g transform="translate(170 0)">{p["svg"]}</g></g>')

(ROOT / 'parts').mkdir(exist_ok=True)
for p in parts:
    (ROOT / 'parts' / f'{p["id"]}.svg').write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}"><defs>{DEFS}</defs>{wrap(p)}</svg>', encoding='utf-8')
(ROOT / 'parts' / 'parts.json').write_text(json.dumps(
    [{k: p[k] for k in ('id', 'ko', 'en', 'layer', 'note')} for p in parts], ensure_ascii=False, indent=1), encoding='utf-8')

meta = json.dumps([{k: p[k] for k in ('id', 'ko', 'en', 'layer', 'note')} for p in parts], ensure_ascii=False)
svg_all = f'<svg id="svg" xmlns="http://www.w3.org/2000/svg" viewBox="{VB}"><defs>{DEFS}</defs>' + ''.join(wrap(p) for p in parts) + '</svg>'
html = (ROOT / 'tools' / 'viewer_template.html').read_text(encoding='utf-8').replace('/*META*/', meta).replace('/*OFF*/', '[]').replace('<!--SVG-->', svg_all)
(ROOT / 'samples' / 'arm_assembly.html').write_text(html, encoding='utf-8')
print(len(parts), 'parts')
