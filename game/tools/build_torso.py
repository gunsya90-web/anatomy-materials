#!/usr/bin/env python3
"""몸통 앞면(가슴·배·골반) 장면: 뼈 · 근육 · 장기 부품을 만들고 조립 뷰어를 생성한다.
출력: game/parts/torso/*.svg, game/parts/torso/parts.json, game/samples/torso_assembly.html
좌표계 viewBox 0 0 680 700, 정중선 x=340. 좌우 쌍 구조물은 mirror=True로 한 번만 그린다(환자의 오른쪽 = 화면 왼쪽)."""
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
VB = '0 0 680 700'; MID = 340
DARK = '#5E1B1A'; BS = '#8F7F55'

def lin(id, a, b, c):  # 대각선 그라데이션
    return f'<linearGradient id="{id}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset=".55" stop-color="{b}"/><stop offset="1" stop-color="{c}"/></linearGradient>'
COMMON = ''.join([
    lin('bone', '#FBF6E6', '#EADFBE', '#B9A97C'), lin('cart', '#E9F1F5', '#CBDAE3', '#9DB3C0'),
    lin('mus', '#E88F82', '#C95C53', '#93312E'), lin('mus2', '#F0A094', '#D86B60', '#9F3733'), lin('mus3', '#D9776C', '#B34842', '#7E2926'),
    lin('tend', '#FAF5E8', '#EFE7D0', '#CFC4A6'), lin('hl', '#A9DAFF', '#3D93EA', '#1B55A8'),
    '<filter id="sh" x="-10%" y="-10%" width="120%" height="120%"><feDropShadow dx="1.5" dy="2.5" stdDeviation="2.5" flood-color="#3a1210" flood-opacity=".35"/></filter>'])

def lerp(a, b, t): return a + (b - a) * t
def line(d, w, c, op=1, cls=''): return f'<path d="{d}" fill="none" stroke="{c}" stroke-opacity="{op}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" class="{cls}"/>'
def gloss(d, w=4, op=.45): return line(d, w, '#fff', op)
def shade(d, w=2, op=.35, c='#4a3318'): return line(d, w, c, op)
def shp(d, g, s=DARK, w=1.4, sh=True): return f'<path class="f" d="{d}" fill="url(#{g})" stroke="{s}" stroke-width="{w}" stroke-linejoin="round"' + (' filter="url(#sh)"/>' if sh else '/>')
def bonep(d): return f'<path class="f" d="{d}" fill="url(#bone)" stroke="{BS}" stroke-width="1.5" stroke-linejoin="round"/>'
def tube(d, w, fill, edge, g=None):  # 관(혈관·기관지 등): 테두리 + 안쪽 색
    return line(d, w + 3, edge) + line(d, w, fill, cls='ps')

parts = []
def add(id, ko, en, layer, note, body, defs='', mirror=False):
    parts.append(dict(id=id, ko=ko, en=en, layer=layer, note=note, body=body, defs=defs, mirror=mirror))
def clip(id, d): return f'<clipPath id="c-{id}"><path d="{d}"/></clipPath>'
def fib(id, paths, op=.35): return f'<g clip-path="url(#c-{id})" fill="none" stroke="{DARK}" stroke-opacity="{op}" stroke-width="1.1" stroke-linecap="round">{paths}</g>'
def mg(id, a, b, c): return lin(id, a, b, c)

# ═════════ 뼈 ═════════
sp = ''
for i in range(24):
    y = 92 + i * 15.6; w = 17 + i * 0.75 + (4 if i > 18 else 0)
    sp += f'<rect class="f" x="{MID - w/2:.1f}" y="{y:.1f}" width="{w:.1f}" height="12" rx="4" fill="url(#bone)" stroke="{BS}" stroke-width="1.1"/>'
    if i >= 7: sp += line(f'M{MID - w/2:.1f} {y+6:.1f} L{MID - w/2 - (9 + (i-7)*.5):.1f} {y+4:.1f} M{MID + w/2:.1f} {y+6:.1f} L{MID + w/2 + (9 + (i-7)*.5):.1f} {y+4:.1f}', 4, BS) + line(f'M{MID - w/2:.1f} {y+6:.1f} L{MID - w/2 - (9 + (i-7)*.5):.1f} {y+4:.1f} M{MID + w/2:.1f} {y+6:.1f} L{MID + w/2 + (9 + (i-7)*.5):.1f} {y+4:.1f}', 2.4, '#EADFBE', cls='ps')
sp += bonep(f'M{MID-22} 466 C{MID-22} 500 {MID-12} 530 {MID-6} 548 L{MID+6} 548 C{MID+12} 530 {MID+22} 500 {MID+22} 466 Z') + shade(f'M{MID-14} 486 H{MID+14} M{MID-11} 504 H{MID+11} M{MID-8} 522 H{MID+8}', 1.2, .3)
sp += f'<ellipse class="f" cx="{MID}" cy="555" rx="6" ry="8" fill="url(#bone)" stroke="{BS}"/>'
add('spine', '척주', 'Vertebral column', 'bone', '목뼈 7 · 등뼈 12 · 허리뼈 5 · 엉치뼈 · 꼬리뼈. 등뼈에는 갈비뼈가 붙습니다.', sp)

rib = ''
EXW = [62, 88, 104, 116, 124, 130, 132, 130, 124, 114, 86, 72]
for i in range(12):
    y0 = 96 + 22 * i; lx = MID - EXW[i]; ly = y0 + 34 + i * 3
    if i < 7: ex, ey = MID - 18, 112 + 31 * i
    elif i < 10: ex, ey = [MID - 38, MID - 66, MID - 92][i - 7], [314, 338, 362][i - 7]
    else: ex, ey = lx + 26 + (i - 10) * 6, ly + 28 + (i - 10) * 4
    cx, cy = ((ex + 44, ey - 6) if i < 7 else (ex - 24, ey + 22)) if i < 10 else (ex, ey)
    bone_d = f'M{MID-12} {y0} C{lx+50} {y0-14} {lx} {y0+4} {lx} {ly} C{lx} {ly+34} {cx-34} {cy-18} {cx} {cy}'
    rib += line(bone_d, 10.5, BS) + line(bone_d, 8, '#EADFBE', cls='ps') + gloss(bone_d.replace(f'M{MID-12} {y0}', f'M{MID-12} {y0-2}'), 1.6, .55)
    if i < 10:
        cd = f'M{cx} {cy} C{cx-14} {cy+2} {ex+14} {ey} {ex} {ey}'
        rib += line(cd, 9, '#8EA3AE') + line(cd, 7, '#D3E1E9', cls='ps')
add('ribs', '갈비뼈', 'Ribs (1–12)', 'bone', '12쌍: 참갈비뼈 7 · 거짓갈비뼈 3 · 뜬갈비뼈 2. 밝은 청회색 부분이 갈비연골입니다.', rib, mirror=True)

add('sternum', '복장뼈', 'Sternum', 'bone', '복장뼈자루 · 복장뼈몸통 · 칼돌기로 구성되며, 자루와 몸통 사이가 복장뼈각입니다.',
    bonep(f'M{MID-19} 98 C{MID-9} 94 {MID+9} 94 {MID+19} 98 C{MID+22} 108 {MID+20} 116 {MID+19} 124 L{MID+22} 130 L{MID+22} 298 L{MID+12} 312 L{MID+5} 340 L{MID-5} 340 L{MID-12} 312 L{MID-22} 298 L{MID-22} 130 L{MID-19} 124 C{MID-20} 116 {MID-22} 108 {MID-19} 98 Z')
    + shade(f'M{MID-22} 129 H{MID+22}', 2, .5) + shade(f'M{MID-8} 97 Q{MID} 109 {MID+8} 97', 2, .5)
    + shade(f'M{MID-22} 170 H{MID+22} M{MID-22} 212 H{MID+22} M{MID-22} 254 H{MID+22}', 1.1, .25) + gloss(f'M{MID-12} 140 V290', 3, .5))

add('clavicle', '빗장뼈', 'Clavicle', 'bone', '팔이음뼈를 몸통에 연결하는 유일한 뼈. 가운데 1/3에서 골절이 잦습니다.',
    line('M326 104 C300 88 270 96 244 90 C218 84 198 92 184 106', 16, BS) + line('M326 104 C300 88 270 96 244 90 C218 84 198 92 184 106', 13, '#E8DCB8', cls='ps')
    + gloss('M324 100 C300 84 270 92 244 86 C220 80 202 88 188 100', 2.6, .6)
    + f'<ellipse class="f" cx="328" cy="106" rx="12" ry="10" fill="url(#bone)" stroke="{BS}" stroke-width="1.4"/><ellipse class="f" cx="184" cy="105" rx="13" ry="7" transform="rotate(-30 184 105)" fill="url(#bone)" stroke="{BS}" stroke-width="1.4"/>', mirror=True)

PELV = 'M322 468 C304 440 246 428 212 452 C190 482 198 522 224 550 C242 570 262 582 286 592 L316 598 C326 584 326 564 320 544 C312 514 320 492 322 468 Z'
add('pelvis', '볼기뼈', 'Hip bone (pelvis)', 'bone', '엉덩뼈 · 궁둥뼈 · 두덩뼈가 합쳐져 이루며, 좌우 두덩뼈가 두덩결합으로 만납니다.',
    bonep(PELV) + f'<path d="M322 468 C310 470 306 482 308 496" fill="none" stroke="{BS}" stroke-width="1.2"/>'
    + '<ellipse cx="272" cy="562" rx="13" ry="19" transform="rotate(-24 272 562)" fill="#5B5340" fill-opacity=".5" stroke="#8F7F55"/>'
    + shade('M214 456 C240 446 280 450 312 470', 2.2, .35) + gloss('M216 470 C206 500 214 524 232 546', 3, .55)
    + '<circle cx="246" cy="540" r="9" fill="#E3D6AE" stroke="#8F7F55" stroke-width="1.2"/>', mirror=True)

# ═════════ 장기 ═════════
def organ(id, ko, en, note, d, cols, extra='', mirror=False, sh=True):
    g = f'g-{id}'
    add(id, ko, en, 'organ', note, shp(d, g, sh=sh) + extra, defs=lin(g, *cols[:3]).replace('id="%s"' % g, 'id="%s"' % g), mirror=mirror)
    parts[-1]['stroke'] = cols[3] if len(cols) > 3 else DARK
def organ_s(id, ko, en, note, d, cols, extra='', mirror=False):
    g = f'g-{id}'; s = cols[3]
    add(id, ko, en, 'organ', note, shp(d, g, s=s) + extra, defs=lin(g, *cols[:3]), mirror=mirror)

organ_s('kidney', '콩팥', 'Kidney', '복막뒤 장기. 오른쪽이 간 때문에 약간 더 낮습니다. 안쪽 오목한 곳이 콩팥문입니다.',
    'M262 380 C286 370 304 388 300 414 C298 428 304 436 300 444 C290 458 268 454 260 436 C252 416 250 390 262 380 Z',
    ['#C77070', '#8E3B3B', '#5C2020', '#4D1D1D'], shade('M286 400 C292 410 292 420 286 428', 2.5, .5, '#2a0a0a') + gloss('M262 392 C256 410 258 430 266 446', 3, .35), mirror=True)
organ_s('adrenal', '콩팥위샘', 'Adrenal gland', '콩팥 위쪽에 놓이는 내분비샘. 겉질과 속질로 나뉩니다.',
    'M276 366 C286 360 300 366 304 376 C296 378 284 376 276 366 Z', ['#EFD58A', '#D8B25A', '#9A7A30', '#7A5E20'], mirror=True)
add('ureter', '요관', 'Ureter', 'organ', '콩팥깔때기에서 방광으로 오줌을 내려보내는 근육관. 세 곳의 좁은 부위가 있습니다.',
    tube('M296 436 C300 480 318 520 330 566', 4, '#EBC66E', '#8A6B22'), mirror=True)
organ_s('spleen', '지라', 'Spleen', '왼쪽 윗배, 9–11번 갈비뼈 높이. 면역과 낡은 적혈구 제거를 담당합니다.',
    'M430 306 C448 306 460 330 454 358 C450 372 436 376 430 362 C424 342 420 318 430 306 Z', ['#A8587C', '#7A3B5A', '#4A1F36', '#3E1A2D'], gloss('M436 316 C446 330 448 350 444 362', 3, .3))
organ_s('pancreas', '이자', 'Pancreas', '복막뒤 장기. 소화효소(외분비)와 인슐린(내분비)을 만듭니다. 머리 · 몸통 · 꼬리로 나뉩니다.',
    'M296 396 C292 410 300 424 316 420 C330 410 360 392 396 390 C414 390 426 396 424 404 C410 406 372 408 340 424 C316 436 292 440 288 416 C286 404 290 398 296 396 Z', ['#F2D88A', '#E3C16F', '#A0842F', '#8A7230'], shade('M312 412 C350 394 390 396 418 400', 1.6, .3))
add('duodenum', '샘창자', 'Duodenum', 'organ', '작은창자의 첫 부분(C자 모양). 이자머리를 감싸고 쓸개즙과 이자액이 합류합니다.',
    tube('M332 372 C300 370 278 388 284 410 C290 434 320 440 346 434', 13, '#EBB0A6', '#9A5A52'))
organ_s('rectum', '곧창자', 'Rectum', '큰창자의 끝부분. 엉치뼈 앞쪽을 따라 내려가 항문관으로 이어집니다.',
    f'M{MID-8} 540 C{MID-14} 570 {MID-6} 600 {MID-5} 640 L{MID+5} 640 C{MID+6} 600 {MID+14} 570 {MID+8} 540 Z', ['#E6B592', '#C98B5A', '#8A5A30', '#7A4E2C'])

col_d = 'M252 526 L252 446 C252 424 270 418 290 424 C320 436 360 436 392 424 C412 418 428 424 428 446 L428 526 C428 552 404 560 384 552 C372 546 352 548 340 544'
add('colon', '큰창자', 'Large intestine', 'organ', '막창자(+막창자꼬리) · 잘록창자(오름·가로·내림·구불) · 곧창자. 겉면에 잘록창자주름이 보입니다.',
    line(col_d, 25, '#7A4E2C') + line(col_d, 22, '#D29C68', cls='ps') + line(col_d, 22, '#8A5A2E', .38) .replace('stroke-linecap="round"', 'stroke-linecap="butt" stroke-dasharray="2 10"')
    + gloss(col_d.replace('252 526', '257 526'), 3, .22)
    + f'<ellipse class="f" cx="252" cy="530" rx="17" ry="15" fill="#D29C68" stroke="#7A4E2C" stroke-width="1.5"/>' + tube('M248 544 C240 560 246 572 258 572', 6, '#D9A878', '#7A4E2C'))

import random
random.seed(7)
si = 'M300 462'
y = 462
for r in range(8):
    x1, x2 = (300 + random.randint(-8, 6), 384 + random.randint(-6, 10))
    xa, xb = (x2, x1) if r % 2 == 0 else (x1, x2)
    y2 = y + 12 + random.randint(-2, 3)
    si += f' C{xa+ (22 if r%2==0 else -22)} {y-6} {xa+(22 if r%2==0 else -22)} {y+10} {xa} {y+10}'
    si += f' C{(xa+xb)//2} {y+4+random.randint(-6,8)} {(xa+xb)//2} {y2+random.randint(-4,6)} {xb} {y2}'
    y = y2
sid = si
add('small', '작은창자', 'Small intestine', 'organ', '샘창자 · 빈창자 · 돌창자로 이루어집니다(빈창자 2/5, 돌창자 3/5).',
    line(sid, 15, '#9A5A52') + line(sid, 12, '#EDA89E', cls='ps') + line(sid, 3.4, '#fff', .35))

organ_s('stomach', '위', 'Stomach', '왼쪽 윗배. 들문 · 위바닥 · 위몸통 · 날문부로 나뉘며 큰굽이/작은굽이가 있습니다.',
    'M362 306 C392 288 436 300 440 336 C442 372 414 396 384 392 C360 388 346 372 354 352 C358 340 352 328 356 318 C358 312 360 308 362 306 Z',
    ['#EBA897', '#D9917F', '#A8564A', '#8A4C3E'], shade('M372 320 C396 312 420 322 424 346', 1.8, .3) + gloss('M366 318 C390 302 420 308 430 326', 4, .35))
organ_s('liver', '간', 'Liver', '몸에서 가장 큰 샘. 오른엽 · 왼엽을 낫인대가 나눕니다. 오른쪽 윗배에 있습니다.',
    'M214 306 C256 290 324 290 372 310 C392 320 386 340 364 346 C340 358 310 372 278 374 C240 374 216 348 214 306 Z',
    ['#BE7A57', '#9B5A3C', '#6A3A22', '#5A301D'], shade('M338 296 C340 322 332 344 322 358', 2.4, .5) + gloss('M224 316 C250 298 300 296 340 304', 4, .3))
organ_s('gallbladder', '쓸개', 'Gallbladder', '간 아래면의 주머니. 쓸개즙을 저장하고 농축합니다.',
    'M288 366 C296 360 306 368 304 384 C302 394 292 396 286 388 C282 380 282 372 288 366 Z', ['#8DBE74', '#5E8C4A', '#3A5E2A', '#2E4A22'])
organ_s('lung_r', '오른허파', 'Right lung', '오른쪽 3엽(위엽 · 중간엽 · 아래엽). 가로틈과 빗틈으로 나뉩니다.',
    'M332 114 C298 106 250 116 238 170 C228 232 238 288 262 300 C296 306 330 294 332 270 Z',
    ['#F0C4C8', '#E3A9AE', '#B07880', '#8D5F64'], shade('M238 198 C270 208 306 202 332 190', 1.8, .45) + shade('M244 150 C272 214 300 262 330 282', 1.8, .45) + gloss('M250 140 C240 190 244 250 262 288', 4, .35))
organ_s('lung_l', '왼허파', 'Left lung', '왼쪽 2엽(위엽 · 아래엽). 앞모서리에 심장패임, 아래에 혀부분이 있습니다.',
    'M348 114 C384 106 430 116 442 170 C452 230 442 290 418 300 C392 306 366 294 360 264 C362 240 372 226 360 206 C352 188 348 150 348 114 Z',
    ['#F0C4C8', '#E3A9AE', '#B07880', '#8D5F64'], shade('M444 150 C410 190 384 240 362 268', 1.8, .45) + gloss('M432 140 C444 190 440 250 422 288', 4, .35))

heart = 'M338 194 C346 180 368 178 380 188 C394 190 402 208 398 228 C392 258 366 290 346 300 C328 278 326 234 332 212 C332 204 334 198 338 194 Z'
add('heart', '심장', 'Heart', 'organ', '심방 2 · 심실 2의 네 방. 가슴 안에서 약간 왼쪽에 놓이며 심장막에 싸여 있습니다.',
    tube('M332 196 L332 130', 12, '#6F8FC4', '#34507E') + tube('M350 190 C346 160 372 148 394 160 C410 168 408 192 406 216', 14, '#D85A5A', '#6E1F1F')
    + shp(heart, 'g-heart') + shade('M346 214 C352 240 358 266 352 290', 2, .35, '#400') + shade('M338 214 C356 214 380 210 396 222', 1.8, .3, '#400') + gloss('M350 194 C362 186 378 190 384 198', 4, .4),
    defs=lin('g-heart', '#E98080', '#C94B4B', '#7A2222'))

add('trachea', '기관', 'Trachea', 'organ', '목뼈 6번 높이에서 시작해 등뼈 4–5번 높이(복장뼈각)에서 두 기관지로 갈라집니다. C자 연골고리가 있습니다.',
    tube(f'M{MID} 62 L{MID} 178', 17, '#BFDCEC', '#4E7A94') + ''.join(line(f'M{MID-7} {y} H{MID+7}', 1.6, '#4E7A94', .6) for y in range(68, 176, 7))
    + tube(f'M{MID} 178 C{MID-14} 188 {MID-30} 198 {MID-40} 210', 12, '#BFDCEC', '#4E7A94') + tube(f'M{MID} 178 C{MID+12} 190 {MID+28} 200 {MID+40} 212', 11, '#BFDCEC', '#4E7A94'))
add('larynx', '후두', 'Larynx', 'organ', '발성과 기도 보호를 맡는 기관. 갑상연골이 목의 후두융기를 이룹니다.',
    shp(f'M{MID-22} 40 L{MID+22} 40 C{MID+24} 52 {MID+18} 64 {MID+10} 72 L{MID-10} 72 C{MID-18} 64 {MID-24} 52 {MID-22} 40 Z', 'g-larynx', '#5C7A8C') + shade(f'M{MID} 42 V68', 2, .4, '#2a4452'),
    defs=lin('g-larynx', '#E4EFF5', '#BFDCEC', '#7FA3B8'))
organ_s('thyroid', '갑상샘', 'Thyroid gland', '목 앞쪽의 나비 모양 샘. 두 엽이 갑상샘잘록으로 이어지며 갑상샘호르몬을 분비합니다.',
    f'M{MID-8} 82 C{MID-22} 70 {MID-34} 82 {MID-30} 104 C{MID-28} 116 {MID-14} 116 {MID-8} 100 L{MID+8} 100 C{MID+14} 116 {MID+28} 116 {MID+30} 104 C{MID+34} 82 {MID+22} 70 {MID+8} 82 Z',
    ['#CC7A5E', '#B5654A', '#7A3D28', '#6B3523'], gloss(f'M{MID-26} 88 C{MID-24} 82 {MID-16} 80 {MID-12} 84', 2.4, .4))
organ_s('bladder', '방광', 'Urinary bladder', '오줌을 저장. 골반강 앞쪽, 두덩뼈 뒤에 있습니다.',
    f'M{MID-30} 578 C{MID-30} 556 {MID-12} 552 {MID} 552 C{MID+12} 552 {MID+30} 556 {MID+30} 578 C{MID+28} 600 {MID+10} 608 {MID} 608 C{MID-10} 608 {MID-28} 600 {MID-30} 578 Z',
    ['#F2E3A6', '#E8D58F', '#B5A04A', '#8A7A36'], gloss(f'M{MID-22} 568 C{MID-14} 560 {MID-4} 558 {MID+6} 560', 3.4, .45))

# ═════════ 근육 ═════════
PEC = 'M326 100 C292 84 246 92 214 114 C200 124 192 138 190 152 C228 174 282 210 326 292 L334 292 L334 100 Z'
add('pec', '큰가슴근', 'Pectoralis major', 'muscle', '안쪽·가쪽 가슴근신경 지배. 팔의 굽힘 · 모음 · 안쪽돌림.',
    shp(PEC, 'mus') + fib('pec', ''.join(f'<path d="M194 152 Q{(194+x)/2} {(152+y)/2 + dy} {x} {y}"/>' for x, y, dy in
        [(lerp(326, 220, i/9), lerp(98, 112, i/9), -8) for i in range(10)] + [(330, lerp(110, 290, i/12), 5) for i in range(13)])) + gloss('M300 108 C260 100 232 114 212 134', 4, .25),
    defs=clip('pec', PEC), mirror=True)
PMIN = 'M300 168 L218 124 C214 132 222 144 232 152 C252 166 276 190 296 214 Z'
add('pecminor', '작은가슴근', 'Pectoralis minor', 'muscle', '안쪽가슴근신경 지배. 어깨뼈를 앞아래로 당깁니다. 3–5번 갈비뼈에서 부리돌기로 이어집니다.',
    shp(PMIN, 'mus3') + fib('pecminor', ''.join(f'<path d="M222 130 L{lerp(262,300,i/6)} {lerp(170,220,i/6)}"/>' for i in range(7)), .3), defs=clip('pecminor', PMIN), mirror=True)
ser = ''.join(shp(f'M{240 - (k*2 if k>3 else 0) - 20:.0f} {166 + k*17} C{240 - 8 - (k*2 if k>3 else 0):.0f} {160 + k*17} {240 + 8:.0f} {168 + k*17} {240 + 14:.0f} {178 + k*17} C{240 + 4:.0f} {188 + k*17} {240 - 14 - (k*2 if k>3 else 0):.0f} {184 + k*17} {240 - 20 - (k*2 if k>3 else 0):.0f} {166 + k*17} Z', 'mus2', sh=False) for k in range(8))
add('serratus', '앞톱니근', 'Serratus anterior', 'muscle', '긴가슴신경 지배. 어깨뼈를 앞으로 당기고 돌립니다. 손상 시 날개어깨뼈가 생깁니다.', ser, mirror=True)
DEL = 'M214 112 C176 96 142 112 130 150 C124 184 134 214 148 244 C168 214 190 182 204 156 C212 136 214 124 214 112 Z'
add('deltoid', '삼각근', 'Deltoid', 'muscle', '겨드랑신경 지배. 팔 가쪽 벌림의 주동근입니다.',
    shp(DEL, 'mus2') + fib('deltoid', ''.join(f'<path d="M148 244 Q{(148+x)/2+8} {(244+y)/2} {x} {y}"/>' for x, y in [(lerp(214,132,i/10), lerp(110,150,i/10)) for i in range(11)]), .42) + gloss('M200 118 C170 112 146 130 138 160', 5, .3),
    defs=clip('deltoid', DEL), mirror=True)
RA = 'M334 262 C318 262 300 270 290 286 L294 470 L334 478 Z'
add('rectus', '배곧은근', 'Rectus abdominis', 'muscle', '가슴신경(T7–T12) 지배. 몸통 굽힘. 힘줄 교차(보통 3개)가 있어 \'식스팩\'을 이룹니다. 배곧은근집에 싸입니다.',
    shp(RA, 'mus') + fib('rectus', ''.join(f'<path d="M{lerp(296,332,i/6):.0f} 270 C{lerp(296,330,i/6):.0f} 380 {lerp(298,332,i/6):.0f} 430 {lerp(296,332,i/6):.0f} 476"/>' for i in range(7)), .22)
    + shade('M296 366 H334 M295 408 H334 M294 444 H334', 3.2, .55, DARK) + line('M335 322 V478', 3, '#EFE7D0', .95) + gloss('M300 332 V462', 4, .22),
    defs=clip('rectus', RA), mirror=True)
EO = 'M228 244 C258 250 284 296 294 336 L294 464 L256 458 L222 442 C208 392 208 320 228 244 Z'
add('oblique_ext', '배바깥빗근', 'External oblique', 'muscle', '아래 가슴신경(T7–T12) 지배. 몸통 굽힘과 반대쪽 돌림. 섬유가 \'주머니에 손 넣는\' 방향(아래안쪽)으로 달립니다.',
    shp(EO, 'mus2') + fib('oblique_ext', ''.join(f'<path d="M{lerp(230,288,i/9):.0f} {lerp(256,336,i/9):.0f} L{lerp(222,292,i/9)+ 6:.0f} {lerp(360,462,i/9):.0f}"/>' for i in range(10)) + ''.join(f'<path d="M{216+ i*4} {330+i*20} L{250+i*6} {350+i*20+16}"/>' for i in range(5)), .35)
    + line('M294 330 L294 464', 7, '#EFE7D0', .9), defs=clip('oblique_ext', EO), mirror=True)
IO = 'M236 342 C262 332 286 352 294 374 L294 462 L246 452 C236 420 232 380 236 342 Z'
add('oblique_int', '배속빗근', 'Internal oblique', 'muscle', '아래 가슴신경 · 엉덩아랫배신경 지배. 몸통 굽힘과 같은쪽 돌림. 섬유는 배바깥빗근과 직각으로 달립니다.',
    shp(IO, 'mus3') + fib('oblique_int', ''.join(f'<path d="M{238+i*3} {450-i*14} L{292} {376 + i*8 - 12}"/>' for i in range(8)), .3), defs=clip('oblique_int', IO), mirror=True)
TA = 'M244 366 L294 372 L294 458 L250 448 C240 424 238 392 244 366 Z'
add('transversus', '배가로근', 'Transversus abdominis', 'muscle', '아래 가슴신경 · 엉덩아랫배신경 지배. 배 속 압력을 높이는 가장 깊은 납작근. 섬유가 가로로 달립니다.',
    shp(TA, 'mus3') + fib('transversus', ''.join(f'<path d="M244 {372+i*11} L294 {376+i*11}"/>' for i in range(8)), .32), defs=clip('transversus', TA), mirror=True)
DI = f'M232 304 C262 262 {MID-24} 250 {MID} 262 C{MID+24} 250 {680-262} 262 {680-232} 304 C{680-270} 286 {MID+30} 290 {MID} 300 C{MID-30} 290 270 286 232 304 Z'
add('diaphragm', '가로막', 'Diaphragm', 'muscle', '가로막신경(C3–5) 지배. 가장 중요한 호흡근. 대동맥열공(T12) · 식도열공(T10) · 대정맥공(T8)이 지납니다.',
    shp(DI, 'mus2', sh=False) + f'<ellipse cx="{MID}" cy="272" rx="34" ry="10" fill="url(#tend)" stroke="{DARK}" stroke-opacity=".5"/>'
    + fib('diaphragm', ''.join(f'<path d="M{MID} 272 L{x} {y}"/>' for x, y in [(lerp(236, 444, i/16), 300 - 4 * math.sin(math.pi * i/16)) for i in range(17)]), .3), defs=clip('diaphragm', DI))

Z = ['spine', 'kidney', 'adrenal', 'ureter', 'spleen', 'pancreas', 'duodenum', 'rectum', 'colon', 'small', 'diaphragm', 'stomach', 'liver', 'gallbladder',
     'lung_r', 'lung_l', 'trachea', 'heart', 'larynx', 'thyroid', 'bladder', 'pelvis', 'ribs', 'sternum', 'clavicle',
     'transversus', 'oblique_int', 'rectus', 'oblique_ext', 'serratus', 'pecminor', 'pec', 'deltoid']
parts.sort(key=lambda p: Z.index(p['id']))
assert len(set(p['id'] for p in parts)) == len(parts)

SIL = ('<g class="bg" pointer-events="none" fill="#9aa0b4" fill-opacity=".14" stroke="#9aa0b4" stroke-opacity=".45" stroke-width="1.5">'
       f'<rect x="{MID-24}" y="20" width="48" height="80"/>'
       f'<path d="M196 112 C240 92 300 88 {MID} 88 C380 88 440 92 484 112 L470 300 C462 360 452 420 456 470 C470 520 456 580 438 650 L242 650 C224 580 210 520 224 470 C228 420 218 360 210 300 Z"/>'
       '<path d="M192 118 L150 250 L140 300" fill="none" stroke-width="0" /></g>')
def wrap(p):
    inner = p['body'] + (f'<g transform="translate({2*MID} 0) scale(-1 1)">{p["body"]}</g>' if p['mirror'] else '')
    return (f'<g class="part" id="p-{p["id"]}" data-id="{p["id"]}" data-layer="{p["layer"]}" data-ko="{p["ko"]}" data-en="{p["en"]}">{inner}</g>')

out = ROOT / 'parts' / 'torso'; out.mkdir(parents=True, exist_ok=True)
for p in parts:
    (out / f'{p["id"]}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}"><defs>{COMMON}{p["defs"]}</defs>{wrap(p)}</svg>', encoding='utf-8')
meta = [{k: p[k] for k in ('id', 'ko', 'en', 'layer', 'note')} for p in parts]
(out / 'parts.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding='utf-8')
svg_all = f'<svg id="svg" xmlns="http://www.w3.org/2000/svg" viewBox="{VB}"><defs>{COMMON}{"".join(p["defs"] for p in parts)}</defs>{SIL}' + ''.join(wrap(p) for p in parts) + '</svg>'
html = (ROOT / 'tools' / 'viewer_template.html').read_text(encoding='utf-8').replace('/*META*/', json.dumps(meta, ensure_ascii=False)).replace('/*OFF*/', '["muscle"]').replace('<!--SVG-->', svg_all).replace('구조물 조립 뷰어', '몸통 조립 뷰어 (가슴·배·골반)')
(ROOT / 'samples' / 'torso_assembly.html').write_text(html, encoding='utf-8')
print(len(parts), 'parts', {l: sum(p['layer'] == l for p in parts) for l in ('bone', 'muscle', 'organ')})
