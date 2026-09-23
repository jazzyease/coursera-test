"""Render the reel's physical props (passport, stamp, documents, envelope papers) to PNG.

Deterministic (fixed seeds) and offline. Re-run after edits:
    python tools/make_assets.py        (needs pillow, numpy, scipy, fonttools, brotli)

Inputs: assets/fonts/*.woff2, tools/.portrait-cut.png (subject cutout from the source clip at
4.8s via `hyperframes remove-background`). Outputs: assets/props/*.png at 2x display size.
"""

import math
import os

import numpy as np
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "props")
FONTS = os.path.join(ROOT, "tools", ".fonts")
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
os.makedirs(OUT, exist_ok=True)
os.makedirs(FONTS, exist_ok=True)


def ttf(name):
    path = os.path.join(FONTS, name + ".ttf")
    if not os.path.exists(path):
        f = TTFont(os.path.join(ROOT, "assets", "fonts", name + ".woff2"))
        f.flavor = None
        f.save(path)
    return path


def archivo(size, wght=600, wdth=100):
    f = ImageFont.truetype(ttf("Archivo-Variable"), size)
    f.set_variation_by_axes([wght, wdth])
    return f


def mono(size):
    return ImageFont.truetype(MONO, size)


# ---------------------------------------------------------------- texture helpers
def noise(h, w, sigma, seed):
    n = np.random.default_rng(seed).standard_normal((h, w)).astype(np.float32)
    n = ndimage.gaussian_filter(n, sigma)
    return (n - n.mean()) / (n.std() + 1e-6)


def paper(h, w, base, seed, grain=5.0, blotch=4.0):
    """Off-white paper: fine grain + soft blotches + faint fibres. base = (r, g, b)."""
    rgb = np.ones((h, w, 3), np.float32) * np.array(base, np.float32)
    tone = noise(h, w, 0.6, seed) * grain + noise(h, w, 40, seed + 1) * blotch
    rng = np.random.default_rng(seed + 2)
    fib = np.zeros((h, w), np.float32)
    for _ in range(int(h * w / 9000)):
        y, x = rng.integers(0, h), rng.integers(0, w)
        ang, ln = rng.uniform(0, math.pi), rng.integers(8, 30)
        for t in range(ln):
            yy, xx = int(y + math.sin(ang) * t), int(x + math.cos(ang) * t)
            if 0 <= yy < h and 0 <= xx < w:
                fib[yy, xx] = 1
    fib = ndimage.gaussian_filter(fib, 0.5) * -10
    return np.clip(rgb + (tone + fib)[..., None], 0, 255)


def leather(h, w, base, seed):
    """Pebbled leather lit from top-left (height-map normals, Lambert + soft spec)."""
    hgt = noise(h, w, 1.6, seed) * 0.6 + noise(h, w, 4, seed + 1) * 0.4
    gy, gx = np.gradient(hgt)
    nx, ny, nz = -gx * 2.2, -gy * 2.2, np.ones_like(hgt)
    ln = np.sqrt(nx**2 + ny**2 + nz**2)
    lx, ly, lz = -0.45, -0.55, 0.7
    lam = (nx * lx + ny * ly + nz * lz) / ln
    spec = np.clip(lam, 0, 1) ** 18 * 38
    rgb = np.array(base, np.float32)[None, None, :] * (0.72 + 0.34 * lam[..., None]) + spec[..., None]
    return np.clip(rgb, 0, 255)


def to_img(rgb, alpha=None):
    a = np.full(rgb.shape[:2], 255, np.uint8) if alpha is None else np.clip(alpha, 0, 255).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb.astype(np.uint8), a]), "RGBA")


def rounded_mask(w, h, r, ss=4):
    m = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], r * ss, fill=255)
    return np.asarray(m.resize((w, h), Image.LANCZOS), np.float32)


def guilloche(w, h, color, seed, ss=2, kind="waves", cx=0.5, cy=0.5, alpha=70, lines=26):
    """Fine security-print linework, supersampled for hairline anti-aliasing."""
    im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(seed)
    col = tuple(color) + (alpha,)
    if kind == "waves":
        f1, f2, ph = rng.uniform(2.5, 4), rng.uniform(7, 11), rng.uniform(0, 6)
        for k in range(lines):
            pts = []
            for i in range(0, w * ss + 1, 3):
                x = i / (w * ss)
                y = (k + 0.5) / lines + 0.05 * math.sin(x * math.pi * f1 + k * 0.33 + ph) + 0.012 * math.sin(x * math.pi * f2 + k)
                pts.append((i, y * h * ss))
            d.line(pts, fill=col, width=ss)
    else:
        R = min(w, h) * ss * 0.46
        petals = int(rng.integers(9, 14))
        for k in range(lines):
            pts = []
            for i in range(721):
                th = i / 720 * 2 * math.pi
                r = R * (0.45 + 0.5 * k / lines) + R * 0.09 * math.sin(th * petals + k * 0.45)
                pts.append((cx * w * ss + math.cos(th) * r, cy * h * ss + math.sin(th) * r))
            d.line(pts, fill=col, width=ss)
    return im.resize((w, h), Image.LANCZOS)


def text_lines(d, x, y, width, rows, gap, h, color, seed, last_short=True):
    """Fine print: seeded pseudo-words set in Archivo at cap-height ~h. Too small to read at
    video scale, so it reads as real printing without adding invented copy."""
    rng = np.random.default_rng(seed)
    f = archivo(max(8, int(h * 1.45)), 500 if h < 11 else 650, 100)
    letters = "etaoinshrdlucmfwypvbgk"
    for r in range(rows):
        lim = x + width * (rng.uniform(0.45, 0.7) if (last_short and r == rows - 1) else rng.uniform(0.92, 1.0))
        words, xx = [], x
        while True:
            wd = "".join(rng.choice(list(letters), int(rng.integers(2, 10))))
            if not words and r == 0:
                wd = wd.capitalize()
            wlen = d.textlength(wd + " ", font=f)
            if xx + wlen > lim:
                break
            words.append(wd)
            xx += wlen
        d.text((x, y + r * gap - h * 0.35), " ".join(words), font=f, fill=color)


# ---------------------------------------------------------------- passport spread
def passport():
    PW, PH, M = 640, 880, 34  # page size and cover margin (2x display)
    W, H = PW * 2 + M * 2, PH + M * 2
    cover_a = rounded_mask(W, H, 44)
    canvas = to_img(leather(H, W, (30, 40, 72), 11), cover_a)

    # Page block edges peeking out (several sheets, each slightly inset).
    d = ImageDraw.Draw(canvas)
    for i, inset in enumerate([6, 4, 2]):
        c = (226 - i * 6, 221 - i * 6, 208 - i * 6, 255)
        d.rounded_rectangle([M - 8 + inset, M - 4 + inset, W - M + 8 - inset, H - M + 10 - inset], 18, fill=c)

    def page(seed, tint):
        rgb = paper(PH, PW, tint, seed, grain=3.5, blotch=3)
        im = to_img(rgb)
        im.alpha_composite(guilloche(PW, PH, (95, 160, 160), seed + 5, kind="waves", alpha=54, lines=34))
        im.alpha_composite(guilloche(PW, PH, (205, 140, 160), seed + 6, kind="rosette", cx=0.52, cy=0.46, alpha=40, lines=22))
        return im

    left, right = page(21, (238, 241, 231)), page(31, (242, 236, 232))

    # --- data page (left)
    dl = ImageDraw.Draw(left)
    lab, val = archivo(15, 500, 100), archivo(21, 600, 100)
    ph_box = (44, 150, 44 + 230, 150 + 296)
    photo_bg = Image.new("RGBA", (230, 296), (214, 222, 228, 255))
    cut = Image.open(os.path.join(ROOT, "tools", ".portrait-cut.png")).convert("RGBA")
    cut = cut.resize((int(cut.width * 296 / cut.height * 1.18), int(296 * 1.18)), Image.LANCZOS)
    photo_bg.alpha_composite(cut, ((230 - cut.width) // 2, 8))
    g = photo_bg.convert("L").convert("RGBA")  # passport data-page photos are greyscale
    g = Image.blend(g, photo_bg, 0.18)
    left.alpha_composite(g, ph_box[:2])
    dl.rectangle(ph_box, outline=(60, 70, 80, 110), width=2)
    # ghost image (small, faint)
    ghost = g.resize((92, 118), Image.LANCZOS)
    ghost.putalpha(ghost.getchannel("A").point(lambda a: a * 0.28))
    left.alpha_composite(ghost, (500, 520))
    fields = [(150, "Surname"), (212, "Given names"), (274, "Nationality"), (336, "Date of birth"), (398, "Sex"), (460, "Date of expiry")]
    for y, name in fields:
        dl.text((306, y), name, font=lab, fill=(70, 86, 98, 255))
        dl.text((306, y + 18), "XXXXXXXX" if name != "Sex" else "X", font=val, fill=(28, 30, 38, 255))
    dl.text((44, 70), "PASSPORT", font=archivo(30, 800, 118), fill=(34, 44, 76, 255))
    dl.text((44, 104), "Type P", font=lab, fill=(70, 86, 98, 255))
    mz = mono(26)
    dl.text((36, 736), "P<XXXXXXXXX<<XXXXXXX<<<<<<<<<<<<<<<", font=mz, fill=(24, 26, 32, 255))
    dl.text((36, 790), "X000000000XXX0000000X0000000<<<<<<<", font=mz, fill=(24, 26, 32, 255))

    # --- visa sticker (right page)
    VW, VH = 560, 700
    ys = np.linspace(0, 1, VH)[:, None]
    xs = np.linspace(0, 1, VW)[None, :]
    c1, c2, c3 = np.array([248, 226, 214]), np.array([226, 222, 244]), np.array([214, 238, 228])
    tmix = (xs * 0.55 + ys * 0.45)[..., None]
    grad = np.where(tmix < 0.5, c1 + (c2 - c1) * (tmix / 0.5), c2 + (c3 - c2) * ((tmix - 0.5) / 0.5))
    grad = grad + noise(VH, VW, 0.6, 41)[..., None] * 3
    sticker = to_img(np.clip(grad, 0, 255), rounded_mask(VW, VH, 14))
    sticker.alpha_composite(guilloche(VW, VH, (150, 110, 180), 43, kind="rosette", cx=0.66, cy=0.4, alpha=60, lines=30))
    sticker.alpha_composite(guilloche(VW, VH, (90, 150, 140), 44, kind="waves", alpha=40, lines=40))
    ds = ImageDraw.Draw(sticker)
    ds.text((34, 30), "VISA", font=archivo(58, 800, 118), fill=(52, 40, 88, 255))
    small = archivo(14, 500, 100)
    ds.text((36, 100), "Type / Category", font=small, fill=(80, 76, 100, 255))
    ph2 = g.resize((150, 193), Image.LANCZOS)
    sticker.alpha_composite(ph2, (36, 150))
    ds.rectangle([36, 150, 186, 343], outline=(70, 60, 90, 120), width=2)
    for i, name in enumerate(["Valid from", "Valid until", "Entries", "Duration of stay", "Issued at"]):
        y = 150 + i * 44
        ds.text((214, y), name, font=small, fill=(80, 76, 100, 255))
        ds.text((214, y + 17), ["XX XXX XXXX", "XX XXX XXXX", "XX", "XXX", "XXXXXXXX"][i], font=archivo(19, 600), fill=(40, 36, 56, 235))
    # hologram patch: iridescent foil with fine diffraction rings
    hw, hh = 116, 116
    yy, xx = np.mgrid[0:hh, 0:hw].astype(np.float32)
    ang = np.arctan2(yy - hh / 2, xx - hw / 2)
    hue = (ang / (2 * np.pi) + 0.5 + xx / hw * 0.4) % 1.0
    holo = np.stack([0.5 + 0.5 * np.cos(2 * np.pi * (hue + o)) for o in (0, 0.33, 0.66)], -1)
    holo = (0.74 + 0.2 * holo) * 255
    holo = holo * (0.94 + 0.06 * np.sin(np.hypot(xx - hw / 2, yy - hh / 2) * 1.4))[..., None]
    sticker.alpha_composite(to_img(np.clip(holo, 0, 255), rounded_mask(hw, hh, 58) * 0.75), (VW - hw - 30, 28))
    ds.rectangle([0, VH - 130, VW, VH - 128], fill=(90, 80, 120, 90))
    vz = mono(22)
    ds.text((30, VH - 110), "V<XXXXXXXXX<<XXXXXXX<<<<<<<<<<<<<", font=vz, fill=(30, 28, 44, 255))
    ds.text((30, VH - 64), "X000000000XXX0000000X000000<<<<<<", font=vz, fill=(30, 28, 44, 255))
    # sticker sits on the page with a hairline shadow
    sh = Image.new("RGBA", (VW + 20, VH + 20), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([10, 12, VW + 10, VH + 12], 14, fill=(0, 0, 0, 60))
    right.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)), (30, 70))
    right.alpha_composite(sticker, (40, 80))
    ImageDraw.Draw(right).text((44, 810), "Page 12", font=archivo(15, 500), fill=(90, 96, 104, 200))

    # --- gutter curvature: pages dip toward the spine (per-column vertical squeeze + shading)
    def bend(im, side):
        a = np.asarray(im, np.float32)
        h, w = a.shape[:2]
        x = np.arange(w, dtype=np.float32)
        dist = (w - 1 - x) if side == "left" else x
        k = np.exp(-((dist / 110.0) ** 2))
        sy = 1 - 0.028 * k
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        src_y = (yy - h / 2) / sy[None, :] + h / 2 - 6 * k[None, :]
        out = np.stack([ndimage.map_coordinates(a[..., c], [src_y, xx], order=1, cval=0) for c in range(4)], -1)
        shade = 1 - 0.34 * np.exp(-((dist / 70.0) ** 2)) - 0.05 * np.exp(-((dist / 260.0) ** 2))
        edge = 1 + 0.04 * np.exp(-(((w - 1 - dist) / 30.0) ** 2))
        out[..., :3] *= (shade * edge)[None, :, None]
        return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGBA")

    lm = rounded_mask(PW, PH, 16)
    for pg in (left, right):
        pg.putalpha(Image.fromarray(np.minimum(np.asarray(pg.getchannel("A"), np.float32), lm).astype(np.uint8)))
    canvas.alpha_composite(bend(left, "left"), (M, M))
    canvas.alpha_composite(bend(right, "right"), (M + PW, M))
    d = ImageDraw.Draw(canvas)
    d.line([(M + PW, M + 4), (M + PW, H - M - 4)], fill=(60, 56, 50, 110), width=2)  # spine crease

    # global light falloff (key light top-left), baked
    a = np.asarray(canvas, np.float32).copy()
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    light = 1.04 - 0.10 * ((xx / W) * 0.6 + (yy / H) * 0.4)
    a[..., :3] *= light[..., None]
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA").save(os.path.join(OUT, "passport-spread.png"), optimize=True)
    return W, H


# ---------------------------------------------------------------- rubber stamp
def stamp(name, word, w, h, seed):
    ss = 3
    m = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(m)
    b = 7 * ss
    d.rounded_rectangle([b, b, w * ss - b, h * ss - b], 16 * ss, outline=255, width=7 * ss)
    d.rounded_rectangle([b + 13 * ss, b + 13 * ss, w * ss - b - 13 * ss, h * ss - b - 13 * ss], 9 * ss, outline=255, width=3 * ss)
    f = archivo(int(h * 0.44) * ss, 800, 72)
    tw = d.textlength(word, font=f)
    box = d.textbbox((0, 0), word, font=f)
    d.text(((w * ss - tw) / 2, (h * ss - (box[3] + box[1])) / 2), word, font=f, fill=255)
    m = np.asarray(m.resize((w, h), Image.LANCZOS), np.float32) / 255
    # ink: uneven pressure, dropped specks, voids, rough bled edges
    press = 0.78 + 0.22 * np.clip(noise(h, w, 18, seed), -1.5, 1.5) / 1.5
    specks = (noise(h, w, 1.1, seed + 1) > 1.25).astype(np.float32)
    voids = (noise(h, w, 7, seed + 2) > 1.35).astype(np.float32)
    rough = ndimage.gaussian_filter(m, 0.9) + noise(h, w, 0.8, seed + 3) * 0.12
    ink = np.clip((rough - 0.42) * 3.2, 0, 1) * press * (1 - 0.85 * specks) * (1 - 0.7 * voids)
    rgb = np.zeros((h, w, 3), np.float32) + np.array([176, 26, 38], np.float32)
    img = to_img(rgb, ink * 235).rotate(-7, resample=Image.BICUBIC, expand=True)
    img.save(os.path.join(OUT, name), optimize=True)


# ---------------------------------------------------------------- documents
def sheet(name, seed, key_line=None):
    W, H = 540, 730
    im = to_img(paper(H, W, (246, 244, 238), seed, grain=3, blotch=2.5), rounded_mask(W, H, 10))
    d = ImageDraw.Draw(im)
    d.rectangle([48, 52, 92, 96], fill=(34, 44, 76, 255))
    text_lines(d, 108, 56, 220, 2, 22, 12, (34, 44, 76, 235), seed + 1, last_short=True)
    d.line([(48, 124), (W - 48, 124)], fill=(34, 44, 76, 120), width=2)
    text_lines(d, 48, 150, W - 96, 3 if key_line is not None else 5, 26, 10, (58, 58, 64, 215), seed + 2)
    ty = 310
    for r in range(6):
        d.line([(48, ty + r * 34), (W - 48, ty + r * 34)], fill=(150, 150, 156, 150), width=1)
        text_lines(d, 56, ty + r * 34 + 12, 180, 1, 0, 9, (70, 70, 78, 200), seed + 10 + r, last_short=False)
        text_lines(d, W - 170, ty + r * 34 + 12, 110, 1, 0, 9, (70, 70, 78, 200), seed + 20 + r, last_short=False)
    text_lines(d, 48, 530, W - 96, 3, 26, 10, (58, 58, 64, 215), seed + 3)
    pts = []
    for i in range(160):
        t = i / 159
        pts.append((70 + t * 170, 660 + math.sin(t * 19) * 10 * (1 - t) - t * 14 + math.sin(t * 5) * 6))
    d.line(pts, fill=(28, 34, 70, 230), width=3, joint="curve")
    d.line([(60, 684), (260, 684)], fill=(120, 120, 128, 150), width=1)
    if key_line is not None:
        text_lines(d, 48, key_line, W - 150, 1, 0, 12, (30, 30, 36, 240), seed + 99, last_short=False)
    im.save(os.path.join(OUT, name), optimize=True)


def papers():
    to_img(paper(580, 880, (232, 228, 219), 71, grain=4, blotch=4)).save(os.path.join(OUT, "env-paper.png"), optimize=True)
    W, H = 784, 524
    im = to_img(paper(H, W, (248, 247, 242), 81, grain=3, blotch=2))
    d = ImageDraw.Draw(im)
    d.rectangle([40, 38, 80, 78], fill=(34, 44, 76, 255))
    text_lines(d, 96, 42, 220, 2, 20, 11, (34, 44, 76, 235), 82)
    d.line([(40, 104), (W - 40, 104)], fill=(34, 44, 76, 110), width=2)
    text_lines(d, 40, 330, W - 80, 6, 26, 10, (60, 60, 66, 215), 83)
    im.save(os.path.join(OUT, "letter.png"), optimize=True)


# ---------------------------------------------------------------- statement of purpose page
# Layout in 2x px (display = /2). The HTML markup canvas uses these coordinates, keep in sync:
#   goals paragraph lines 1-2 underline at y 222 / 248, x 56..544 (display 111/124)
#   copied lines 2-3 at y 366 / 392 (display 183/196)
#   empty "story" block 470..600 (display 235..300)
SOP_W, SOP_H = 600, 800


def sop_page():
    W, H = SOP_W, SOP_H
    im = to_img(paper(H, W, (247, 245, 239), 131, grain=3, blotch=2.5), rounded_mask(W, H, 10))
    d = ImageDraw.Draw(im)
    d.text((56, 52), "Statement of Purpose", font=archivo(40, 700, 100), fill=(28, 36, 66, 255))
    text_lines(d, 56, 116, 260, 1, 0, 11, (90, 94, 104, 230), 132, last_short=False)
    d.line([(56, 146), (W - 56, 146)], fill=(28, 36, 66, 140), width=2)
    text_lines(d, 56, 186, W - 112, 5, 26, 10, (56, 56, 62, 220), 133)
    text_lines(d, 56, 330, W - 112, 4, 26, 10, (56, 56, 62, 220), 134)
    # a gray section heading followed by an intentionally empty block (the missing story)
    d.rounded_rectangle([56, 446, 196, 458], 6, fill=(120, 122, 132, 200))
    text_lines(d, 56, 630, W - 112, 3, 26, 10, (56, 56, 62, 220), 135)
    pts = []
    for i in range(160):
        t = i / 159
        pts.append((70 + t * 170, 740 + math.sin(t * 19) * 10 * (1 - t) - t * 14 + math.sin(t * 5) * 6))
    d.line(pts, fill=(28, 34, 70, 230), width=3, joint="curve")
    im.save(os.path.join(OUT, "sop-page.png"), optimize=True)


if __name__ == "__main__":
    print("passport", passport())
    stamp("stamp-rejected.png", "REJECTED", 560, 190, 5)
    for i in range(5):
        sheet("sheet-%d.png" % i, 100 + i * 7, key_line=236 if i == 2 else None)
    papers()
    sop_page()
    print("done ->", OUT)
