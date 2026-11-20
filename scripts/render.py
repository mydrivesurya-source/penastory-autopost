"""Pen A Story renderer: carousels (1080x1350), stories (1080x1920) and kinetic story reels (1080x1920, 30fps).
Brand: navy #1B2A4A, gold #D4A017, cream #FFF8EE, charcoal #2C2C2C; night look #0B1426 -> #33456E glow, gold #EEC76A.
Fonts: Playfair Display (headlines), Lato (body), Noto Telugu for any Telugu text. Logo on every asset.
All music is synthesised here (original, copyright-free)."""
import math, re, subprocess, wave, os, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FD = os.path.join(ROOT, "assets", "fonts")
NAVY=(27,42,74); GOLD=(212,160,23); CREAM=(255,248,238); CHAR=(44,44,44)
NIGHT=(11,20,38); GLOW=(51,69,110); GOLD2=(238,199,106); MUTED=(147,163,194); WHITE=(255,255,255)
TE = re.compile(r"[ఀ-౿]")
_fc = {}

def font(kind, size, text=""):
    if TE.search(text or ""):
        name = "NotoSerifTelugu-Bold" if kind in ("head", "bold", "body_serif") else "NotoSansTelugu-Regular"
    else:
        name = {"head": "Playfair-Bold", "ital": "Playfair-Italic", "bold": "Lato-Bold", "body": "Lato-Regular", "body_serif": "Playfair-Regular"}[kind]
    k = (name, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(os.path.join(FD, name + ".ttf"), size)
    return _fc[k]

_cm = {}
def clean(text, f):
    """Drop characters the font cannot draw (emoji, arrows) so nothing renders as a box."""
    from fontTools.ttLib import TTFont
    p = f.path
    if p not in _cm: _cm[p] = set(TTFont(p).getBestCmap())
    out = "".join(ch for ch in text if ord(ch) in _cm[p] or ch in "\n ")
    return " ".join(out.split(" ")).replace("  ", " ").strip() if "\n" not in out else out

def wrap(d, text, f, width):
    text = clean(text, f)
    lines = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f) <= width: cur = t
            else:
                if cur: lines.append(cur)
                cur = w
        lines.append(cur)
    return lines

def fit(d, text, kind, width, maxh, start, minsize=34, spacing=1.25):
    """Largest font size where wrapped text fits width x maxh."""
    s = start
    while s > minsize:
        f = font(kind, s, text); L = wrap(d, text, f, width)
        if len(L) * s * spacing <= maxh: return f, L, s
        s -= 4
    f = font(kind, minsize, text); return f, wrap(d, text, f, width), minsize

def block(d, x, y, lines, f, size, fill, align="left", width=0, spacing=1.25):
    for i, l in enumerate(lines):
        lx = x + (width - d.textlength(l, font=f)) / 2 if align == "center" else x
        d.text((lx, y + i * size * spacing), l, font=f, fill=fill)
    return y + len(lines) * size * spacing

# ---------- backgrounds ----------
_bg = {}
def night(w, h, seed=1):
    k = ("n", w, h, seed)
    if k in _bg: return _bg[k].copy()
    sw, sh = w // 6, h // 6
    yy, xx = np.mgrid[0:sh, 0:sw]
    cx, cy = sw * 0.5, sh * 0.38
    r = np.sqrt(((xx - cx) / sw) ** 2 + ((yy - cy) / sh) ** 2) / 0.62
    t = np.clip(r, 0, 1)[..., None]
    a = np.array(GLOW) * (1 - t) + np.array(NIGHT) * t
    im = Image.fromarray(a.astype(np.uint8)).resize((w, h), Image.BICUBIC)
    rng = np.random.default_rng(seed)
    g = rng.normal(0, 5, (h, w, 1))
    im = Image.fromarray(np.clip(np.asarray(im, float) + g, 0, 255).astype(np.uint8))
    _bg[k] = im; return im.copy()

def cream(w, h, seed=2):
    k = ("c", w, h, seed)
    if k in _bg: return _bg[k].copy()
    rng = np.random.default_rng(seed)
    a = np.ones((h, w, 3)) * np.array(CREAM) + rng.normal(0, 3.5, (h, w, 1))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); _bg[k] = im; return im.copy()

def dust(im, n=60, seed=3, t=0.0):
    rng = np.random.default_rng(seed); d = ImageDraw.Draw(im, "RGBA")
    w, h = im.size
    for i in range(n):
        x = (rng.uniform(0, w) + t * rng.uniform(-30, 30)) % w
        y = (rng.uniform(0, h) - t * rng.uniform(10, 50)) % h
        r = rng.uniform(1, 3.2); a = int(rng.uniform(40, 150) * (0.6 + 0.4 * math.sin(t * 2 + i)))
        d.ellipse((x - r, y - r, x + r, y + r), fill=GOLD2 + (max(0, a),))
    return im

_logo = None
def logo(im, size=120, pos="tr", margin=48):
    global _logo
    if _logo is None: _logo = Image.open(os.path.join(ROOT, "assets", "logo.png")).convert("RGBA")
    L = _logo.resize((size, size), Image.LANCZOS)
    m = Image.new("L", (size, size), 0); ImageDraw.Draw(m).ellipse((0, 0, size - 1, size - 1), fill=255)
    a = np.minimum(np.asarray(L.split()[3]), np.asarray(m)); L.putalpha(Image.fromarray(a))
    w, h = im.size
    x = w - size - margin if pos[1] == "r" else margin
    y = margin if pos[0] == "t" else h - size - margin
    im.paste(L, (x, y), L); return im

def cover_card(img, maxw, maxh, border=0, shadow=True):
    c = img.copy(); c.thumbnail((maxw, maxh), Image.LANCZOS)
    pad = 60
    out = Image.new("RGBA", (c.width + pad * 2, c.height + pad * 2), (0, 0, 0, 0))
    if shadow:
        s = Image.new("RGBA", out.size, (0, 0, 0, 0))
        ImageDraw.Draw(s).rectangle((pad + 10, pad + 22, pad + c.width + 10, pad + c.height + 22), fill=(0, 0, 0, 150))
        out = Image.alpha_composite(out, s.filter(ImageFilter.GaussianBlur(22)))
    out.paste(c, (pad, pad)); return out

def rule(d, cx, y, w=120, fill=GOLD):
    d.line((cx - w // 2, y, cx + w // 2, y), fill=fill, width=4)

# ---------- carousel slides (1080x1350) ----------
CW, CH_ = 1080, 1350

PALETTES = [((27, 42, 74), (238, 199, 106)), ((86, 20, 36), (232, 190, 120)), ((20, 54, 44), (226, 196, 120)),
            ((48, 28, 64), (236, 196, 140)), ((12, 58, 70), (240, 205, 130))]
INK = (34, 30, 28)

def paper(w, h, seed=4):
    k = ("p", w, h, seed)
    if k in _bg: return _bg[k].copy()
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w]
    v = 1 - 0.07 * (((xx - w / 2) / w) ** 2 + ((yy - h / 2) / h) ** 2) * 4          # soft vignette
    base = np.array([250, 244, 232])[None, None, :] * v[..., None]
    fib = Image.fromarray(np.clip(rng.normal(128, 7, (h // 2, w // 2)), 0, 255).astype(np.uint8)).resize((w, h)).filter(ImageFilter.GaussianBlur(1.2))
    a = base + (np.asarray(fib, float)[..., None] - 128) * np.array([1, 1, 0.9]) + rng.normal(0, 2.5, (h, w, 1))
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); _bg[k] = im; return im.copy()

def solid(w, h, col, seed=5):
    rng = np.random.default_rng(seed)
    yy = np.linspace(0, 1, h)[:, None, None]
    a = np.array(col)[None, None, :] * (1.12 - 0.3 * yy) + rng.normal(0, 4, (h, w, 1))
    return dust(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), 40, seed)

def inset(d, w, h, col, m=46):
    d.rectangle((m, m, w - m, h - m), outline=col, width=2)
    d.rectangle((m + 10, m + 10, w - m - 10, h - m - 10), outline=col, width=1)

def ornament(d, cx, y, col, w=150):
    d.line((cx - w // 2, y, cx - 14, y), fill=col, width=2); d.line((cx + 14, y, cx + w // 2, y), fill=col, width=2)
    d.polygon([(cx, y - 8), (cx + 8, y), (cx, y + 8), (cx - 8, y)], fill=col)

def slide(s, imgs, idx, total, series="", ep=0):
    """Editorial look. kind: hook (cover page, episode colour) | frame (book page with drop cap)
    | twist (last frame, episode colour) | book (cover on paper) | cta | question | text"""
    k = s.get("kind", "text"); col, acc = PALETTES[ep % len(PALETTES)]
    dark = k in ("hook", "twist", "question") or s.get("dark")
    im = solid(CW, CH_, col, idx + 3) if dark else paper(CW, CH_)
    d = ImageDraw.Draw(im)
    fg = (250, 244, 232) if dark else INK; sub = (214, 206, 190) if dark else (96, 88, 80); ac = acc if dark else col
    inset(d, CW, CH_, acc if dark else (*col,), 46)
    M = 130; Wt = CW - 2 * M
    if series:
        f = font("bold", 24, series); t = series.upper(); d.text(((CW - d.textlength(t, font=f)) / 2, 96), t, font=f, fill=ac)
    if k == "book" and s.get("image") is not None and imgs:
        card = cover_card(imgs[s["image"]], 500, 620); im.paste(card, ((CW - card.width) // 2, 140), card)
        y = 140 + card.height - 20
        f, L, sz = fit(d, s["title"], "head", Wt, 160, 62); y = block(d, M, y, L, f, sz, col, "center", Wt) + 6
        ornament(d, CW // 2, int(y + 14), col, 120)
        if s.get("lines"):
            t = "\n".join(s["lines"]); f, L, sz = fit(d, t, "ital", Wt, CH_ - y - 170, 38, 28, 1.4)
            block(d, M, y + 40, L, f, sz, (80, 72, 66), "center", Wt, 1.4)
    elif k == "frame":
        title = s.get("title", ""); body = "\n".join(s.get("lines", []))
        te = bool(TE.search(title))
        f1, L1, s1 = fit(d, title, "head" if te else "body_serif", Wt, 760, 74 if te else 82, 40, 1.42)
        hgt = len(L1) * s1 * 1.42 + (130 if body else 0)
        y = (CH_ - hgt) / 2
        if not te and title[:1].isalpha():
            # drop cap: first letter big in episode colour, first two lines indented
            dc = font("head", int(s1 * 2.5)); cap = title[0]; cw_ = d.textlength(cap, font=dc) + 18
            rest = title[1:]
            f1 = font("body_serif", s1)
            Lr = wrap(d, rest, f1, Wt - cw_); first = Lr[:2]; more = wrap(d, " ".join(Lr[2:]), f1, Wt) if len(Lr) > 2 else []
            d.text((M, y - s1 * 0.32), cap, font=dc, fill=col)
            for i, l in enumerate(first): d.text((M + cw_, y + i * s1 * 1.42), l, font=f1, fill=INK)
            y2 = block(d, M, y + len(first) * s1 * 1.42, more, f1, s1, INK, "left", Wt, 1.42)
        else:
            y2 = block(d, M, y, L1, f1, s1, INK, "left", Wt, 1.42)
        if body:
            ornament(d, CW // 2, int(y2 + 40), col, 120)
            f2, L2, s2 = fit(d, body, "ital", Wt, 200, 44, 30, 1.35); block(d, M, y2 + 70, L2, f2, s2, col, "center", Wt, 1.35)
        f = font("ital", 30); t = f"~ {s.get('n', idx)} ~"; d.text(((CW - d.textlength(t, font=f)) / 2, CH_ - 125), t, font=f, fill=(120, 110, 100))
    else:
        title = s.get("title", ""); body = "\n".join(s.get("lines", []))
        start = {"hook": 92, "twist": 74, "question": 80}.get(k, 66)
        f1, L1, s1 = fit(d, title, "head", Wt, 560, start)
        f2, L2, s2 = fit(d, body, "ital" if k in ("hook", "twist") else "body", Wt, 380, 42, 28, 1.4) if body else (None, [], 0)
        hgt = len(L1) * s1 * 1.25 + (70 + len(L2) * s2 * 1.4 if L2 else 0)
        y = (CH_ - hgt) / 2
        y = block(d, M, y, L1, f1, s1, fg, "center", Wt)
        if L2:
            ornament(d, CW // 2, int(y + 30), ac, 140)
            block(d, M, y + 62, L2, f2, s2, sub, "center", Wt, 1.4)
        if k == "hook" and total > 1:
            f = font("bold", 26); t = "SWIPE TO READ  >>"; d.text(((CW - d.textlength(t, font=f)) / 2, CH_ - 132), t, font=f, fill=ac)
    logo(im, 84, "br", 74)
    return im.convert("RGB")

# ---------- story image (1080x1920) ----------
def story(spec, imgs):
    W, H = 1080, 1920
    im = night(W, H, 11); im = dust(im, 70, 5); d = ImageDraw.Draw(im); M = 100
    y = 300
    if spec.get("kicker"):
        f = font("bold", 34, spec["kicker"]); t = spec["kicker"].upper()
        d.text(((W - d.textlength(t, font=f)) / 2, 230), t, font=f, fill=GOLD2)
    if imgs:
        card = cover_card(imgs[0], 600, 760); im.paste(card, ((W - card.width) // 2, 300), card); y = 300 + card.height + 10
    f, L, s = fit(d, spec.get("title", ""), "head", W - 2 * M, 420 if imgs else 700, 84 if imgs else 110)
    y = block(d, M, y, L, f, s, WHITE, "center", W - 2 * M) + 20
    if spec.get("text"):
        f, L, s = fit(d, spec["text"], "body", W - 2 * M, H - y - 380, 46, 30, 1.4)
        block(d, M, y + 20, L, f, s, (220, 226, 240), "center", W - 2 * M, 1.4)
    if spec.get("cta"):
        f = font("bold", 40, spec["cta"]); tw = d.textlength(spec["cta"], font=f)
        bx = (W - tw) / 2 - 50; d.rounded_rectangle((bx, H - 330, bx + tw + 100, H - 230), 50, fill=GOLD)
        d.text(((W - tw) / 2, H - 312), spec["cta"], font=f, fill=NIGHT)
    logo(im, 130, "tr", 60)
    return im.convert("RGB")

# ---------- music: original warm storytelling bed ----------
def music(dur, sr=44100, bpm=78, seed=0):
    n = int(dur * sr); t = np.arange(n) / sr; out = np.zeros(n)
    beat = 60 / bpm; bar = beat * 4
    prog = [[[220, 261.6, 329.6], [174.6, 220, 261.6], [261.6, 329.6, 392], [196, 246.9, 293.7]],   # Am F C G
            [[146.8, 174.6, 220], [233.1, 293.7, 349.2], [174.6, 220, 261.6], [164.8, 207.7, 246.9]]][seed % 2]  # Dm Bb F E
    for i, b in enumerate(np.arange(0, dur, bar)):
        s = int(b * sr); e = min(n, int((b + bar) * sr)); k = np.arange(e - s) / sr
        env = np.minimum(1, k * 1.5) * np.minimum(1, (bar - k) * 2)
        for f in prog[i % 4]:
            out[s:e] += 0.05 * (np.sin(2 * np.pi * f * k) + 0.3 * np.sin(2 * np.pi * f * 2 * k)) * env
        root = prog[i % 4][0] / 2
        out[s:e] += 0.07 * np.sin(2 * np.pi * root * k) * np.exp(-k * 1.2)
    rng = np.random.default_rng(seed)
    for b in np.arange(0, dur, beat / 2):                     # soft plucked arpeggio
        s = int(b * sr); e = min(n, s + int(0.9 * sr)); k = np.arange(e - s) / sr
        ch = prog[int(b // bar) % 4]; f = ch[rng.integers(0, 3)] * 2
        out[s:e] += 0.045 * np.sin(2 * np.pi * f * k) * np.exp(-k * 4)
    for b in np.arange(0, dur, beat):                          # heartbeat pulse
        s = int(b * sr); e = min(n, s + int(0.25 * sr)); k = np.arange(e - s) / sr
        out[s:e] += 0.18 * np.sin(2 * np.pi * (48 + 40 * np.exp(-k * 30)) * k) * np.exp(-k * 14)
    out /= max(1e-6, np.abs(out).max()); f = int(0.8 * sr); out[:f] *= np.linspace(0, 1, f); out[-f:] *= np.linspace(1, 0, f)
    return out

def ease(t): t = max(0., min(1., t)); return 1 - (1 - t) ** 3

# ---------- kinetic story reel ----------
def reel(spec, imgs, out, tmp):
    """spec.beats: [{"text": str, "dur": sec, "style": "big|line|small"}]; then an end card with the book cover,
    title, spec.end_line and spec.cta. Background: night glow with drifting dust and a slow push-in."""
    W, H, FPS = 1080, 1920, 30
    beats = spec["beats"]; end = float(spec.get("end_dur", 4.5))
    times = [0]; [times.append(times[-1] + float(b.get("dur", 2.6))) for b in beats]
    total = times[-1] + end
    base = night(W + 120, H + 210, 21)
    cover = imgs[0] if imgs else None
    bgimg = None
    if cover is not None and spec.get("cover_bg", True):
        BW, BH = W + 120, H + 210
        sc = max(BW / cover.width, BH / cover.height)
        b = cover.resize((int(cover.width * sc) + 1, int(cover.height * sc) + 1))
        b = b.crop(((b.width - BW) // 2, (b.height - BH) // 2, (b.width - BW) // 2 + BW, (b.height - BH) // 2 + BH))
        b = b.filter(ImageFilter.GaussianBlur(28))
        bgimg = Image.blend(b, base, 0.62)
        vg = night(BW, BH, 21)  # darken bottom/top for text contrast
        yy = np.linspace(-1, 1, BH)[:, None, None]; m = np.clip(np.abs(yy) * 0.9, 0, 0.75)
        bgimg = Image.fromarray((np.asarray(bgimg, float) * (1 - m) + np.asarray(vg, float) * m).astype(np.uint8))
    # pre-render text layers
    layers = []
    for b in beats:
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        st = b.get("style", "line"); M = 110
        kind, start = {"big": ("head", 118), "line": ("head", 84), "small": ("ital", 60)}[st]
        f, ls, s = fit(d, b["text"], kind, W - 2 * M, 900, start, 40)
        hgt = len(ls) * s * 1.25; y = (H - hgt) / 2 - 60
        for i, l in enumerate(ls):
            x = (W - d.textlength(l, font=f)) / 2
            d.text((x + 3, y + i * s * 1.25 + 4), l, font=f, fill=(0, 0, 0, 120))
            d.text((x, y + i * s * 1.25), l, font=f, fill=GOLD2 + (255,) if b.get("gold") else WHITE + (255,))
        layers.append(L)
    # end card
    E = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(E); y = 300
    if cover is not None:
        c = cover_card(cover, 560, 760); E.paste(c, ((W - c.width) // 2, 260), c); y = 260 + c.height
    f, ls, s = fit(d, spec.get("title", ""), "head", W - 200, 220, 72)
    y = block(d, 100, y, ls, f, s, WHITE, "center", W - 200) + 10
    if spec.get("end_line"):
        f, ls, s = fit(d, spec["end_line"], "body", W - 200, 160, 42, 30, 1.35)
        y = block(d, 100, y, ls, f, s, (220, 226, 240), "center", W - 200, 1.35) + 20
    cta = spec.get("cta", "Read it on the Pen A Story app")
    f = font("bold", 42, cta); tw = d.textlength(cta, font=f); bx = (W - tw) / 2 - 50; by = y + 30
    d.rounded_rectangle((bx, by, bx + tw + 100, by + 100), 50, fill=GOLD); d.text(((W - tw) / 2, by + 20), cta, font=f, fill=NIGHT)
    nfr = int(total * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", f"{tmp}/v.mp4"], stdin=subprocess.PIPE)
    lg = logo(Image.new("RGBA", (W, H), (0, 0, 0, 0)), 130, "tr", 60)
    src = bgimg if bgimg is not None else base
    for i in range(nfr):
        t = i / FPS; z = 1 + 0.06 * t / total
        cw, chh = int((W + 120) / z), int((H + 210) / z); ox, oy = ((W + 120) - cw) // 2, ((H + 210) - chh) // 2
        fr = src.crop((ox, oy, ox + cw, oy + chh)).resize((W, H), Image.BILINEAR)
        if i % 2 == 0 or i == 0: fr = dust(fr, 55, 9, t)
        fr = fr.convert("RGBA")
        if t < times[-1]:
            j = max(k for k in range(len(beats)) if times[k] <= t); lt = t - times[j]; dur = times[j + 1] - times[j]
            a = min(ease(lt / 0.45), ease((dur - lt) / 0.35)); dy = int(40 * (1 - ease(lt / 0.5)))
            L = layers[j]
            if dy: L = L.transform(L.size, Image.AFFINE, (1, 0, 0, 0, 1, -dy))
            if a < 1: L = Image.fromarray((np.asarray(L) * np.array([1, 1, 1, a])).astype(np.uint8))
            fr = Image.alpha_composite(fr, L)
        else:
            lt = t - times[-1]; a = ease(lt / 0.6); sc = 0.94 + 0.06 * ease(lt / 0.8)
            L = E.resize((int(W * sc), int(H * sc))); P = Image.new("RGBA", (W, H), (0, 0, 0, 0)); P.paste(L, ((W - L.width) // 2, (H - L.height) // 2))
            if a < 1: P = Image.fromarray((np.asarray(P) * np.array([1, 1, 1, a])).astype(np.uint8))
            fr = Image.alpha_composite(fr, P)
        fr = Image.alpha_composite(fr, lg)
        ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    sr = 44100; a = music(total, sr, bpm=spec.get("bpm", 78), seed=spec.get("music", 0)) * 0.55
    with wave.open(f"{tmp}/a.wav", "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((a * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tmp}/v.mp4", "-i", f"{tmp}/a.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    return total

# ---------- photo story slides (editorial, real photography) ----------
def grade(img, w=1080, h=1350, warm=1.0, dark=0.0):
    """Cover-crop, then a soft film grade: lifted blacks, warm highlights, gentle fade, grain, vignette."""
    sc = max(w / img.width, h / img.height)
    im = img.resize((int(img.width * sc) + 1, int(img.height * sc) + 1), Image.LANCZOS)
    im = im.crop(((im.width - w) // 2, (im.height - h) // 2, (im.width - w) // 2 + w, (im.height - h) // 2 + h))
    a = np.asarray(im, float) / 255
    a = 0.06 + a * 0.90                                     # lifted blacks / soft highlights
    a[..., 0] *= 1 + 0.05 * warm; a[..., 2] *= 1 - 0.07 * warm
    lum = a.mean(axis=2, keepdims=True); a = lum + (a - lum) * 0.85   # slight desaturation
    yy, xx = np.mgrid[0:h, 0:w]; v = 1 - 0.35 * ((((xx - w / 2) / w) ** 2 + ((yy - h / 2) / h) ** 2) * 2.2)
    a *= v[..., None] * (1 - dark)
    a += np.random.default_rng(1).normal(0, 0.018, (h, w, 1))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

def photo_slide(s, imgs, idx, total, label=""):
    """Full-bleed graded photo, text low on the frame over a soft shadow gradient. s: image, text, small, kind(end)"""
    W, H = 1080, 1350; end = s.get("kind") == "end"
    if s.get("kind") == "book":
        return book_card(imgs[s["image"]], s.get("text", ""), s.get("small", ""), W, H, label)
    im = grade(imgs[s.get("image", 0)], W, H, dark=0.35 if end else 0.0).convert("RGBA")
    g = np.zeros((H, W, 4), np.uint8); t = np.clip((np.arange(H) - H * 0.38) / (H * 0.62), 0, 1) ** 1.4
    g[..., 3] = (t * (235 if not end else 200))[:, None]; im = Image.alpha_composite(im, Image.fromarray(g))
    d = ImageDraw.Draw(im); M = 92; Wt = W - 2 * M
    if label:
        f = font("bold", 26, label); d.text((M, 84), clean(label, f), font=f, fill=(255, 244, 220, 230))
    text = s.get("text", ""); small = s.get("small", "")
    kind = "head" if s.get("big") or idx == 0 or end else "body_serif"
    f1, L1, s1 = fit(d, text, kind, Wt, 520, 76 if (idx == 0 or end) else 58, 34, 1.36)
    f2, L2, s2 = fit(d, small, "ital", Wt, 160, 36, 26, 1.35) if small else (None, [], 0)
    hgt = len(L1) * s1 * 1.36 + (len(L2) * s2 * 1.35 + 34 if L2 else 0)
    y = (H - hgt) / 2 if end else H - 150 - hgt
    y = block(d, M, y, L1, f1, s1, (255, 250, 240), "center" if end else "left", Wt, 1.36)
    if L2:
        block(d, M, y + 30, L2, f2, s2, (232, 208, 150), "center" if end else "left", Wt, 1.35)
    if total > 1 and not end:
        f = font("body", 24); tt = f"{idx + 1} / {total}"; d.text((W - M - d.textlength(tt, font=f), 88), tt, font=f, fill=(255, 244, 220, 200))
    logo(im, 70, "br", 56)
    return im.convert("RGB")

def photo_story(spec, imgs):
    """1080x1920 story: graded full-bleed photo, one big line (meme or teaser), optional small line and a pill CTA."""
    W, H = 1080, 1920
    im = grade(imgs[0], W, H, dark=0.15).convert("RGBA")
    g = np.zeros((H, W, 4), np.uint8); t = np.clip((np.arange(H) - H * 0.30) / (H * 0.7), 0, 1) ** 1.2
    g[..., 3] = (t * 225)[:, None]; im = Image.alpha_composite(im, Image.fromarray(g)); d = ImageDraw.Draw(im); M = 96
    if spec.get("kicker"):
        f = font("bold", 32, spec["kicker"]); d.text((M, 150), clean(spec["kicker"], f), font=f, fill=(255, 238, 200))
    f1, L1, s1 = fit(d, spec.get("title", ""), "head", W - 2 * M, 700, 86, 40, 1.3)
    f2, L2, s2 = fit(d, spec.get("text", ""), "ital", W - 2 * M, 300, 44, 30, 1.35) if spec.get("text") else (None, [], 0)
    hgt = len(L1) * s1 * 1.3 + (len(L2) * s2 * 1.35 + 40 if L2 else 0)
    y = H - 430 - hgt
    y = block(d, M, y, L1, f1, s1, (255, 250, 240), "left", W - 2 * M, 1.3)
    if L2: block(d, M, y + 30, L2, f2, s2, (232, 208, 150), "left", W - 2 * M, 1.35)
    if spec.get("cta"):
        f = font("bold", 38, spec["cta"]); tw = d.textlength(spec["cta"], font=f)
        d.rounded_rectangle((M, H - 330, M + tw + 80, H - 240), 45, fill=(232, 196, 110)); d.text((M + 40, H - 314), spec["cta"], font=f, fill=(20, 20, 24))
    logo(im, 96, "tr", 120)
    return im.convert("RGB")

# ---------- cinematic photo reel ----------
def photo_reel(spec, imgs, out, tmp):
    """spec.beats: [{"image": i, "text": str, "dur": sec, "small": str?}]; spec.end: {"image","text","small"}.
    Each beat: graded photo, slow push-in/drift, 0.6s crossfade, text rises in on the lower third. Original music bed."""
    W, H, FPS, XF = 1080, 1920, 30, 0.6
    beats = spec["beats"] + [dict(spec["end"], end=True, dur=spec["end"].get("dur", 4.0))]
    big = []
    if spec.get("book"):
        bk = spec["book"]; beats.append({"image": bk["image"], "text": "", "dur": 3.6, "bookcard": True, "end": True})
    for b in beats:   # graded frame at 116% so we can move inside it
        if b.get("bookcard"):
            bk = spec["book"]; g = book_card(imgs[bk["image"]], bk["text"], bk.get("small", ""), int(W * 1.16), int(H * 1.16), showlogo=False)
        else:
            g = grade(imgs[b["image"]], int(W * 1.16), int(H * 1.16), dark=0.45 if b.get("end") else 0.08)
        big.append(g)
    def text_layer(b):
        if b.get("bookcard"): return Image.new("RGBA", (W, H), (0, 0, 0, 0))
        L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = np.zeros((H, W, 4), np.uint8)
        t = np.clip((np.arange(H) - H * 0.30) / (H * 0.55), 0, 1) ** 1.3; g[..., 3] = (np.minimum(t, 1) * 215)[:, None]
        L = Image.alpha_composite(L, Image.fromarray(g)); d = ImageDraw.Draw(L); M = 90; MR = 190   # keep clear of IG buttons
        end = b.get("end")
        f1, L1, s1 = fit(d, b["text"], "head", W - M - MR, 640 if end else 520, 84 if end else (74 if b.get("first") else 64), 38, 1.32)
        f2, L2, s2 = fit(d, b.get("small", ""), "ital", W - M - MR, 200, 44, 28, 1.3) if b.get("small") else (None, [], 0)
        hgt = len(L1) * s1 * 1.32 + (len(L2) * s2 * 1.3 + 30 if L2 else 0)
        y = (H - hgt) / 2 if end else H - 600 - hgt                     # above IG caption zone
        al = "center" if end else "left"
        for i, l in enumerate(L1):
            x = M if al == "left" else (W - d.textlength(l, font=f1)) / 2
            d.text((x + 2, y + i * s1 * 1.32 + 3), l, font=f1, fill=(0, 0, 0, 140)); d.text((x, y + i * s1 * 1.32), l, font=f1, fill=(255, 250, 240, 255))
        y2 = y + len(L1) * s1 * 1.32 + 24
        for i, l in enumerate(L2):
            x = M if al == "left" else (W - d.textlength(l, font=f2)) / 2
            d.text((x, y2 + i * s2 * 1.3), l, font=f2, fill=(236, 206, 140, 255))
        return L
    beats[0]["first"] = True
    layers = [text_layer(b) for b in beats]
    lg = logo(Image.new("RGBA", (W, H), (0, 0, 0, 0)), 100, "tr", 70)
    starts = [0.0]
    for b in beats[:-1]: starts.append(starts[-1] + float(b.get("dur", 3.2)))
    total = starts[-1] + float(beats[-1]["dur"])
    def frame_of(k, t):
        b = big[k]; dur = float(beats[k].get("dur", 3.2)); p = min(1, max(0, t / (dur + XF)))
        z = 1.0 + 0.10 * p if k % 2 == 0 else 1.10 - 0.08 * p            # alternate push-in / pull-out
        cw, ch = int(b.width / 1.16 * (1.16 / z)), int(b.height / 1.16 * (1.16 / z))
        dx = int((b.width - cw) * (0.5 + (0.18 if k % 3 == 0 else -0.18) * (p - 0.5))); dy = (b.height - ch) // 2
        return b.crop((dx, dy, dx + cw, dy + ch)).resize((W, H), Image.BILINEAR)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p", f"{tmp}/v.mp4"], stdin=subprocess.PIPE)
    for i in range(int(total * FPS)):
        t = i / FPS; k = max(j for j in range(len(beats)) if starts[j] <= t); lt = t - starts[k]
        fr = frame_of(k, lt).convert("RGBA")
        if k + 1 < len(beats) and t > starts[k + 1] - XF:          # crossfade into next beat
            a = (t - (starts[k + 1] - XF)) / XF
            fr = Image.blend(fr, frame_of(k + 1, 0).convert("RGBA"), a)
        dur = float(beats[k]["dur"]); ta = min(ease((lt - 0.15) / 0.5), 1 if beats[k].get("end") else ease((dur - XF - lt) / 0.35))
        if ta > 0:
            L = layers[k]; dy = int(26 * (1 - ease((lt - 0.15) / 0.6)))
            if dy: L = L.transform(L.size, Image.AFFINE, (1, 0, 0, 0, 1, -dy))
            if ta < 1: L = Image.fromarray((np.asarray(L) * np.array([1, 1, 1, ta])).astype(np.uint8))
            fr = Image.alpha_composite(fr, L)
        fr = Image.alpha_composite(fr, lg)
        ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    sr = 44100; a = music(total, sr, bpm=spec.get("bpm", 72), seed=spec.get("music", 0)) * 0.6
    with wave.open(f"{tmp}/a.wav", "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((a * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tmp}/v.mp4", "-i", f"{tmp}/a.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    return total


def book_card(cover, title, small, W, H, label="", showlogo=True):
    """Real Pen A Story cover on a blurred, darkened copy of itself + one line + 'read on the app'."""
    bg = grade(cover, W, H, dark=0.55).filter(ImageFilter.GaussianBlur(26)).convert("RGBA")
    d = ImageDraw.Draw(bg); M = 90
    if label:
        f = font("bold", 26, label); d.text((M, 84), clean(label, f), font=f, fill=(255, 244, 220, 230))
    c = cover_card(cover, int(W * 0.56), int(H * 0.50)); bg.paste(c, ((W - c.width) // 2, int(H * 0.10)), c)
    y = int(H * 0.10) + c.height - 10
    f1, L1, s1 = fit(d, title, "head", W - 2 * M, 200, 58, 34, 1.3); y = block(d, M, y, L1, f1, s1, (255, 250, 240), "center", W - 2 * M, 1.3)
    if small:
        f2, L2, s2 = fit(d, small, "ital", W - 2 * M, 120, 36, 26, 1.3); y = block(d, M, y + 12, L2, f2, s2, (236, 206, 140), "center", W - 2 * M, 1.3)
    t = "Read it on the Pen A Story app"; f = font("bold", 34, t); tw = d.textlength(t, font=f)
    by = min(H - 200, y + 34); d.rounded_rectangle(((W - tw) / 2 - 40, by, (W + tw) / 2 + 40, by + 80), 40, fill=(232, 196, 110))
    d.text(((W - tw) / 2, by + 18), t, font=f, fill=(20, 20, 24))
    if showlogo: logo(bg, 70, "br", 56)
    return bg.convert("RGB")
