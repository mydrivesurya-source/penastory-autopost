"""Ink-on-paper story reel: no stock photos, no AI images, zero cost per reel.
Cream handmade paper, living ink-wash blooms, the story written word by word in indigo ink,
ink-blot page turns, Pen A Story end card, original music bed from assets/music.

spec = {"slides": [{"text": "...", "small": "kicker (optional)"}...], "music": "warm|suspense",
        "end": {"title": "Pen A Story", "sub": "..."}}"""
import sys, os, subprocess, tempfile, json, numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from render import font, wrap, logo
import kalam

W, H, FPS = 1080, 1920, 30
INK = (26, 32, 70); RUST = (150, 60, 30); CREAM = (246, 237, 219)
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def paper(seed=0):
    rng = np.random.default_rng(seed)
    a = np.ones((H, W, 3)) * np.array(CREAM, float)
    n = Image.fromarray((rng.random((H // 6, W // 6)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(3))
    a += (np.asarray(n, float)[..., None] / 255 - .5) * 14
    fib = Image.new("L", (W, H), 0); d = ImageDraw.Draw(fib)
    for _ in range(900):
        x, y = rng.uniform(0, W), rng.uniform(0, H); L = rng.uniform(8, 40); t = rng.uniform(0, np.pi)
        d.line((x, y, x + L * np.cos(t), y + L * np.sin(t)), fill=int(rng.uniform(20, 60)), width=1)
    a -= np.asarray(fib.filter(ImageFilter.GaussianBlur(.6)), float)[..., None] / 255 * 18
    yy, xx = np.mgrid[0:H, 0:W]; d2 = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2)
    a *= np.clip(1.08 - d2 * 0.55, 0.75, 1)[..., None]
    a += rng.normal(0, 3, (H, W, 1))
    return np.clip(a, 0, 255)

def _noise(rng, gw, gh, blur):
    return np.asarray(Image.fromarray((rng.random((gh, gw)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur)), float) / 255

def bloom_field(seed):
    """Watercolour ink washes bleeding in from the corners: fractal edges + pigment granulation."""
    rng = np.random.default_rng(seed)
    n = _noise(rng, 12, 21, 40) * .55 + _noise(rng, 40, 70, 8) * .3 + _noise(rng, 135, 240, 2) * .15
    yy, xx = np.mgrid[0:H, 0:W]
    c = [(W * rng.uniform(-.15, .15), H * rng.uniform(-.08, .1)), (W * rng.uniform(.85, 1.15), H * rng.uniform(.9, 1.08))]
    d = np.minimum(*[np.sqrt((xx - cx) ** 2 + ((yy - cy) * .8) ** 2) for cx, cy in c]) / np.hypot(W, H)
    gran = _noise(rng, 540, 960, .6)
    return d + (n - .5) * .32, gran

def ink_layer(fg, t):
    field, gran = fg
    edge = 0.10 + 0.06 * t
    m = np.clip((edge - field) / 0.035, 0, 1)
    depth = np.clip((edge - field) / 0.25, 0, 1)
    rim = np.clip(1 - np.abs(edge - field) / 0.008, 0, 1) * m
    g = m * (0.45 + 0.25 * (1 - depth)) + rim * 0.35
    g *= 0.8 + 0.4 * gran                                                   # pigment granulation
    return np.clip(g, 0, 0.92)[..., None]

def layout(text, small):
    d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    words = len(text.split()); size = 92 if words <= 8 else 80 if words <= 14 else 68 if words <= 20 else 60
    f = font("head", size, text); lines = wrap(d, text, f, W - 220)
    lh = size * (1.55 if any('ఀ' <= ch <= '౿' for ch in text) else 1.32)
    hgt = len(lines) * lh; top = max(300, H * 0.66 / 2 + 160 - hgt / 2)
    return f, lines, lh, top, size

def text_frame(text, small, p, label=""):
    """p: 0..1 writing progress (word by word)."""
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    f, lines, lh, top, size = layout(text, small)
    if small:
        fs = font("ital", 40, small); w = d.textlength(small, font=fs)
        d.text(((W - w) / 2, top - 110), small, font=fs, fill=RUST + (int(255 * min(1, p * 4)),))
    allw = [(i, w) for i, l in enumerate(lines) for w in l.split(" ")]
    shown = p * (len(allw) + 1.5)
    for i, l in enumerate(lines):
        y = top + i * lh; x = (W - d.textlength(l, font=f)) / 2
        for w in l.split(" "):
            k = next(j for j, (li, ww) in enumerate(allw) if li == i and ww == w and j >= sum(len(lines[q].split(" ")) for q in range(i)))
            a = float(np.clip(shown - k, 0, 1))
            if a > 0: d.text((x, y), w, font=f, fill=INK + (int(255 * a),))
            x += d.textlength(w + " ", font=f)
    if p > 0.95:                                                            # hand-drawn ink stroke under the text
        q = min(1, (p - .95) / .05); y = top + len(lines) * lh + 30; x0 = W / 2 - 90
        pts = [(x0 + 180 * s * q, y + 6 * np.sin(s * 6)) for s in np.linspace(0, 1, 30)]
        d.line(pts, fill=RUST + (220,), width=5)
    return L

def build(spec, out):
    tmp = tempfile.mkdtemp()
    slides = spec["slides"]
    durs = [max(3.0, 1.2 + 0.31 * len(s["text"].split())) for s in slides]
    XF = 0.7; starts = np.concatenate([[0], np.cumsum(durs)[:-1]]); end_t = float(sum(durs)); total = end_t + 3.0
    papers = [paper(i % 3) for i in range(len(slides))]
    fields = [bloom_field(10 + i) for i in range(len(slides))]
    endc = np.asarray(kalam.end_card(spec["end"]["title"], spec["end"]["sub"]).convert("RGB"), float)
    lg = logo(Image.new("RGBA", (W, H), (0, 0, 0, 0)), 90, "tr", 64)
    inkc = np.array([38, 58, 140], float)
    def slide_img(k, t):
        lt = t - starts[k]; g = ink_layer(fields[k], min(1, lt / (durs[k] + XF)))
        base = papers[k] * (1 - g * (1 - inkc / 255))
        write = float(np.clip((lt - 0.25) / max(1.2, durs[k] * 0.55), 0, 1))
        im = Image.fromarray(base.astype(np.uint8)).convert("RGBA")
        im = Image.alpha_composite(im, text_frame(slides[k]["text"], slides[k].get("small", ""), write))
        z = 1 + 0.025 * (lt / durs[k])                                         # slow push-in
        cw, ch = int(W / z), int(H / z)
        return np.asarray(im.convert("RGB").crop(((W - cw) // 2, (H - ch) // 2, (W + cw) // 2, (H + ch) // 2)).resize((W, H)), float)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-maxrate", "7M", "-bufsize", "14M", "-pix_fmt", "yuv420p", f"{tmp}/v.mp4"], stdin=subprocess.PIPE)
    for i in range(int(total * FPS)):
        t = i / FPS
        if t < end_t:
            k = int(np.searchsorted(starts, t, side="right") - 1); fr = slide_img(k, t)
            if k > 0 and t < starts[k] + XF:
                m = kalam.ink_mask((t - starts[k]) / XF, 200 + k); fr = slide_img(k - 1, t) * (1 - m) + fr * m
        else:
            m = kalam.ink_mask(min(1, (t - end_t) / XF), 99); fr = slide_img(len(slides) - 1, end_t - 0.01) * (1 - m) + endc * m
        im = Image.fromarray(np.clip(fr, 0, 255).astype(np.uint8)).convert("RGBA")
        if t < end_t: im = Image.alpha_composite(im, lg)
        ff.stdin.write(im.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    mus = os.path.join(R, "assets", "music", spec.get("music", "warm") + ".mp3")
    af = f"afade=t=in:d=0.6,afade=t=out:st={total - 2.2:.2f}:d=2.2,volume=0.9"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tmp}/v.mp4", "-stream_loop", "-1", "-i", mus, "-filter_complex", f"[1:a]{af}[a]",
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", f"{total:.2f}", "-movflags", "+faststart", out], check=True)
    return total

if __name__ == "__main__":
    print(build(json.load(open(sys.argv[1])), sys.argv[2]))
