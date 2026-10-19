# -*- coding: utf-8 -*-
"""
성경말씀 이미지카드 생성기
사용법(터미널):  python make_card.py 감사 1 48
  → verses.json의 '감사' 주제 1번 구절로 48일차 카드를 output/ 폴더에 저장
"""
import json, os, sys, math, random, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# 폴더 구분
#  APP_DIR : 이 파일이 있는 곳 (업데이트되는 코드·구절·화면·설정)  ← 실행기가 Supabase에서 받아 둔 폴더
#  RES_DIR : 폰트·기본배경·성경전체·사용법GIF (exe에 내장, 잘 안 바뀌는 것)
#  USER_DIR: 사용자 기록(지인·이력·내 배경·만든 카드)
FROZEN = getattr(sys, "frozen", False)
APP_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.environ.get("MALSSUM_RES") or (getattr(sys, "_MEIPASS", None) if FROZEN else APP_DIR)
BASE = APP_DIR
USER_DIR = os.path.join(os.environ.get("APPDATA") or os.path.expanduser("~"), "말씀카드")
FONT_DIR = os.path.join(RES_DIR, "fonts")
BG_DIRS = [os.path.join(USER_DIR, "backgrounds"), os.path.join(RES_DIR, "backgrounds")]   # 내 배경 우선, 없으면 기본 배경
OUT_DIR = os.path.join(USER_DIR, "output")
LAST = {"bg": ""}   # 마지막 카드에 쓴 배경 정보

W, H = 1080, 1920
CREAM = (251, 247, 241)
INK = (40, 38, 34)
GREEN = (94, 122, 74)
GREEN_SOFT = (120, 145, 105)
GRAY = (120, 116, 108)


_FONTS = {}


def font(name, size):
    key = (name, size)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _FONTS[key]


def wrap(draw, text, fnt, max_w):
    """공백 단위 줄바꿈. 한 단어가 너무 길면 글자 단위로 자름."""
    lines, cur = [], ""
    for word in text.split(" "):
        test = (cur + " " + word).strip()
        if draw.textlength(test, font=fnt) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            if draw.textlength(word, font=fnt) <= max_w:
                cur = word
            else:  # 글자 단위 강제 분할
                cur = ""
                for ch in word:
                    if draw.textlength(cur + ch, font=fnt) <= max_w:
                        cur += ch
                    else:
                        lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, fontfile, max_size, min_size, max_w, max_lines):
    """max_lines 안에 들어갈 때까지 글자 크기를 줄여가며 맞춤"""
    size = max_size
    while size >= min_size:
        fnt = font(fontfile, size)
        lines = wrap(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 2
    fnt = font(fontfile, min_size)
    return fnt, wrap(draw, text, fnt, max_w)


def draw_centered_lines(draw, lines, fnt, y, fill, spacing=1.45, shadow=False):
    ascent, descent = fnt.getmetrics()
    lh = int((ascent + descent) * spacing)
    for line in lines:
        w = draw.textlength(line, font=fnt)
        x = (W - w) / 2
        if shadow:
            draw.text((x + 2, y + 2), line, font=fnt, fill=(255, 255, 255, 180))
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def _bez(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
            (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])


def _leaf_poly(base, tip, width):
    """base→tip 방향의 뾰족한 잎 모양 (양쪽 곡선) 좌표"""
    dx, dy = tip[0] - base[0], tip[1] - base[1]
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L * width, dx / L * width          # 법선
    mid = ((base[0] + tip[0]) / 2, (base[1] + tip[1]) / 2)
    c1 = (mid[0] + nx, mid[1] + ny); c2 = (mid[0] - nx, mid[1] - ny)
    pts = [_bez(base, c1, tip, t / 14) for t in range(15)]
    pts += [_bez(tip, c2, base, t / 14) for t in range(15)]
    return pts, mid


def make_sprig(size=200, angle=-55, color=GREEN, flip=False):
    """참고 이미지 스타일의 나뭇가지: 가는 곡선 줄기 + 번갈아 달린 뾰족한 잎(선화). 4배 확대 후 축소로 매끈하게."""
    S = 4
    W_, H_ = size * S, size * S
    layer = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    # 줄기: 왼쪽 아래 → 오른쪽 위 완만한 곡선
    p0 = (W_ * 0.12, H_ * 0.90); p2 = (W_ * 0.88, H_ * 0.12); p1 = (W_ * 0.30, H_ * 0.35)
    stem = [_bez(p0, p1, p2, t / 60) for t in range(61)]
    lw = max(2, int(2.2 * S))
    d.line(stem, fill=color + (255,), width=lw, joint="curve")
    # 잎: 줄기 위 t=0.18~0.92 사이에 번갈아, 끝으로 갈수록 작게
    n = 7
    for i in range(n):
        t = 0.18 + 0.74 * i / (n - 1)
        bx, by = _bez(p0, p1, p2, t)
        # 접선
        ax, ay = _bez(p0, p1, p2, min(1, t + 0.02)); tx, ty = ax - bx, ay - by
        tl = math.hypot(tx, ty) or 1; tx, ty = tx / tl, ty / tl
        side = 1 if i % 2 == 0 else -1
        leaf_ang = math.radians(48) * side
        ca, sa = math.cos(leaf_ang), math.sin(leaf_ang)
        dxr, dyr = tx * ca - ty * sa, tx * sa + ty * ca
        ln = (0.30 - 0.12 * (i / (n - 1))) * W_
        tip = (bx + dxr * ln, by + dyr * ln)
        pts, mid = _leaf_poly((bx, by), tip, ln * 0.30)
        d.polygon(pts, fill=(255, 255, 255, 235), outline=color + (255,), width=lw)
        d.line([(bx, by), tip], fill=color + (255,), width=max(1, int(1.2 * S)))   # 잎맥
    # 끝 잎 하나
    tipL = _bez(p0, p1, p2, 1.0); prev = _bez(p0, p1, p2, 0.96)
    dx, dy = tipL[0] - prev[0], tipL[1] - prev[1]; L = math.hypot(dx, dy) or 1
    tip = (tipL[0] + dx / L * 0.17 * W_, tipL[1] + dy / L * 0.17 * W_)
    pts, _ = _leaf_poly(tipL, tip, 0.17 * W_ * 0.28)
    d.polygon(pts, fill=(255, 255, 255, 235), outline=color + (255,), width=lw)
    layer = layer.resize((size, size), Image.LANCZOS)
    if flip:
        layer = layer.transpose(Image.FLIP_LEFT_RIGHT)
    return layer.rotate(angle + 55, resample=Image.BICUBIC, expand=True)


def draw_sprig(draw, cx, cy, scale=1.0, angle=-35, color=GREEN):
    """(호환용) draw 대신 카드 이미지에 직접 합성해야 하므로 make_card 안에서 paste 사용"""
    pass


def placeholder_bg(topic):
    """배경 이미지가 없을 때 쓰는 부드러운 그라데이션 (임시용)"""
    import numpy as np
    palettes = [((233, 225, 205), (176, 190, 160)), ((238, 226, 214), (200, 178, 160)),
                ((225, 232, 220), (150, 175, 140)), ((240, 232, 218), (205, 190, 165))]
    c1, c2 = palettes[sum(map(ord, topic)) % len(palettes)]
    yy, xx = np.mgrid[0:H, 0:W]
    t = yy / H
    s = 0.5 + 0.5 * np.sin((xx / W) * 3 + t * 4)
    k = (t * 0.7 + s * 0.3)[..., None]
    arr = np.array(c1) + (np.array(c2) - np.array(c1)) * k
    glow = Image.new("L", (W, H), 0)
    g = ImageDraw.Draw(glow)
    rnd = random.Random(topic)
    for _ in range(6):
        r = rnd.randint(180, 320)
        x, y = rnd.randint(0, W), rnd.randint(H // 2, H)
        g.ellipse([x - r, y - r, x + r, y + r], fill=70)
    glow = np.asarray(glow.filter(ImageFilter.GaussianBlur(120)))[..., None]
    arr = np.clip(arr + glow, 0, 255).astype("uint8")
    return Image.fromarray(arr, "RGB")


def pick_background(topic, bg_path=None):
    if bg_path and os.path.exists(bg_path):
        LAST["bg"] = os.path.basename(bg_path)
        return Image.open(bg_path).convert("RGB"), True
    exts = (".jpg", ".jpeg", ".jfif", ".png", ".webp", ".bmp")
    # 1순위: 주제 폴더 사진 → 2순위: 공통 폴더 사진 → 3순위: 임시 그라데이션
    for folder in (topic, "공통"):
        for i, bg_root in enumerate(BG_DIRS):
            cands = [c for c in glob.glob(os.path.join(bg_root, folder, "*.*")) if c.lower().endswith(exts)]
            if cands:
                pick = random.choice(cands)
                LAST["bg"] = f"{'내 배경' if i == 0 else '기본 배경'} / {folder} / {os.path.basename(pick)}"
                return Image.open(pick).convert("RGB"), True
    LAST["bg"] = f"임시 배경 ({topic} 배경 사진 없음)"
    return placeholder_bg(topic), False


def cover(img, w, h):
    """이미지를 w×h에 꽉 차게 자르기 (비율 유지)"""
    r = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * r) + 1, int(img.height * r) + 1), Image.LANCZOS)
    x = (img.width - w) // 2
    return img.crop((x, 0, x + w, h))


def make_card(topic, verse, day, bg_path=None, out_path=None):
    card = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(card)

    # ── 1. 일차 배지 ──
    cx, cy, r = W // 2, 190, 92
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GREEN, width=4)
    f_day = font("NanumMyeongjo-ExtraBold.ttf", 50 if day < 100 else 44)
    draw.text((cx, cy + 2), f"{day}일차", font=f_day, fill=INK, anchor="mm")   # 원 정중앙
    sp = make_sprig(150, angle=-55)                                            # 배지 왼쪽 위 나뭇가지
    card.paste(sp, (cx - r - 78, cy - r - 8), sp)

    # ── 2. 성경 구절 ──
    y = 330
    f_v, lines = fit_text(draw, verse["text"], "NanumMyeongjo-Bold.ttf", 46, 30, 900, 7)
    y = draw_centered_lines(draw, lines, f_v, y, INK, spacing=1.5)
    f_ref = font("NanumMyeongjo-Regular.ttf", 32)
    ref = f"({verse['ref']}, {verse.get('version', '개역한글')})"
    y += 6
    draw.text(((W - draw.textlength(ref, font=f_ref)) / 2, y), ref, font=f_ref, fill=GREEN_SOFT)
    y += 80

    # ── 3. 구분선 + 잎 ──
    draw.line([(190, y), (cx - 70, y)], fill=GREEN, width=2)
    draw.line([(cx + 70, y), (W - 190, y)], fill=GREEN, width=2)
    sp = make_sprig(96, angle=-50)                                             # 구분선 가운데 나뭇가지
    card.paste(sp, (cx - sp.width // 2, y - sp.height // 2 + 4), sp)
    y += 60

    # ── 4. 믿음의 선포 ──
    f_t = font("NanumPenScript-Regular.ttf", 56)
    t = "- 믿음의 선포 -"
    draw.text(((W - draw.textlength(t, font=f_t)) / 2, y), t, font=f_t, fill=GREEN)
    y += 90
    # 선포문: 줄바꿈(\n)마다 한 문장, 문장이 길면 자동 줄바꿈. 전체가 최대 줄수 안에 들도록 글자 크기 자동 조정
    sents = [t.strip() for t in verse["declaration"].split("\n") if t.strip()]
    size = 46
    while True:
        f_d = font("NanumGothic-Bold.ttf", size)
        dlines = []
        for i, t in enumerate(sents):
            dlines += wrap(draw, t, f_d, 920)
            if i < len(sents) - 1:
                dlines.append("")          # 문장 사이 빈 줄(간격)
        if len([l for l in dlines if l]) <= 8 or size <= 34:
            break
        size -= 2
    ascent, descent = f_d.getmetrics(); lh = int((ascent + descent) * 1.45); gap = int(lh * 0.35)
    for line in dlines:
        if line == "":
            y += gap; continue
        w = draw.textlength(line, font=f_d)
        draw.text(((W - w) / 2, y), line, font=f_d, fill=INK)
        y += lh
    text_end = y + 20

    # ── 5. 하단 사진 (텍스트 끝 이후 영역) ──
    bg, is_photo = pick_background(topic, bg_path)
    if is_photo:
        photo_top = max(text_end + 40, 900)
        final_h = H
    else:
        # 사진이 없으면 카드 길이를 줄여 빈 공간 최소화
        photo_top = text_end + 30
        final_h = photo_top + 260
    ph = final_h - photo_top
    bg = cover(bg, W, ph)
    fade_h = min(240, ph // 3) if is_photo else min(160, ph // 2)
    mask = Image.new("L", (W, ph), 255)
    md = ImageDraw.Draw(mask)
    for i in range(fade_h):
        md.line([(0, i), (W, i)], fill=int(255 * (i / fade_h) ** 1.4))
    card.paste(bg, (0, photo_top), mask)
    if final_h < H:
        card = card.crop((0, 0, W, final_h))
        # 맨 아래 작은 잎 장식
        sp = make_sprig(90, angle=-50, color=(255, 255, 255))
        card.paste(sp, (W // 2 - sp.width // 2, final_h - 110), sp)

    os.makedirs(OUT_DIR, exist_ok=True)
    if not out_path:
        safe = verse["ref"].replace(":", "_")
        out_path = os.path.join(OUT_DIR, f"{day:03d}일차_{topic}_{safe}.png")
    card.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    verses = json.load(open(os.path.join(BASE, "verses.json"), encoding="utf-8"))
    topic = sys.argv[1] if len(sys.argv) > 1 else "감사"
    idx = int(sys.argv[2]) - 1 if len(sys.argv) > 2 else 0
    day = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    p = make_card(topic, verses[topic][idx], day)
    print("저장:", p)
