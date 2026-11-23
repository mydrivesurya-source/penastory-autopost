"""Kalam reel composer: Pen A Story's ink-story format.
intro clip (pen nib writing) -> ink-art scenes with slow camera moves and ink-spread transitions
-> subtitles in ink colour on the paper -> end card. Voice lines drive the timing.
Sound design: nib scratch at the start, soft original music bed, pen-cap click at the end.

spec = {"intro": "path.mp4", "scenes": [{"image": "path.png", "voice": "path.mp3", "text": "subtitle"}...],
        "end": {"title": "...", "sub": "..."}, "out": "path.mp4"}"""
import json, subprocess, sys, os, wave, tempfile, numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
import render
from render import font, wrap, logo, music

W, H, FPS = 1080, 1920, 30
INK = (24, 30, 64); CREAM = (247, 238, 222); RED = (150, 18, 22); XF = 0.6

def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)

def frames_of(path, n=None):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", path, "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    k = len(raw) // (W * H * 3); a = np.frombuffer(raw, np.uint8)[:k * W * H * 3].reshape(k, H, W, 3)
    return [Image.fromarray(f) for f in a]

def big(img, s=1.14):
    im = img.convert("RGB"); sc = max(W * s / im.width, H * s / im.height)
    im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(2, 60, 2))

def cam(b, p, k):
    """Slow push-in (even scenes) or pull-out (odd scenes) with a gentle drift."""
    z = 1.0 + 0.07 * p if k % 2 == 0 else 1.07 - 0.06 * p
    cw = int(b.width / 1.14 / z); ch = int(cw * H / W)
    dx = int((b.width - cw) * (0.5 + (0.15 if k % 3 == 0 else -0.12) * (p - 0.5)))
    dy = int((b.height - ch) * (0.45 + 0.1 * p))
    return b.crop((dx, dy, dx + cw, dy + ch)).resize((W, H), Image.BILINEAR)

_mask_cache = {}
def ink_mask(t, seed):
    """Organic ink-spread reveal mask (0..1) growing from a blot."""
    if seed not in _mask_cache:
        rng = np.random.default_rng(seed)
        n = Image.fromarray((rng.random((60, 34)) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(18))
        yy, xx = np.mgrid[0:H, 0:W]; cx, cy = W * rng.uniform(.35, .65), H * rng.uniform(.35, .6)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / np.hypot(W, H)
        _mask_cache[seed] = d * 1.6 + (np.asarray(n, float) / 255 - .5) * .5
    f = _mask_cache[seed]; edge = t * 1.45 - .1
    return np.clip((edge - f) / .06, 0, 1)[..., None]

def caption(text, sub="", red=False):
    """Main line (Telugu or English) + small English line, ink on a torn-paper strip."""
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); M = 100
    f = font("head", 60, text); lines = wrap(d, text, f, W - 2 * M - 60)
    lh = 60 * 1.45; f2 = font("ital", 38, sub); sl = wrap(d, sub, f2, W - 2 * M - 60) if sub else []
    hgt = len(lines) * lh + (len(sl) * 50 + 14 if sl else 0); y = H * 0.70 - hgt
    wmax = max([d.textlength(l, font=f) for l in lines] + [d.textlength(l, font=f2) for l in sl])
    x0, x1 = (W - wmax) / 2 - 46, (W + wmax) / 2 + 46; y0, y1 = y - 28, y + hgt + 22
    strip = Image.new("L", (W, H), 0); ds = ImageDraw.Draw(strip); rng = np.random.default_rng(len(text))
    pts = [(x0 + rng.uniform(-6, 6), y0 + rng.uniform(-6, 6)), (x1 + rng.uniform(-6, 6), y0 + rng.uniform(-6, 6)),
           (x1 + rng.uniform(-6, 6), y1 + rng.uniform(-6, 6)), (x0 + rng.uniform(-6, 6), y1 + rng.uniform(-6, 6))]
    ds.polygon(pts, fill=225); strip = strip.filter(ImageFilter.GaussianBlur(5))
    paper = Image.new("RGBA", (W, H), CREAM + (0,)); paper.putalpha(strip); L = Image.alpha_composite(L, paper); d = ImageDraw.Draw(L)
    col = RED if red else INK
    for i, l in enumerate(lines): d.text(((W - d.textlength(l, font=f)) / 2, y + i * lh), l, font=f, fill=col + (255,))
    yy = y + len(lines) * lh + 10
    for i, l in enumerate(sl): d.text(((W - d.textlength(l, font=f2)) / 2, yy + i * 50), l, font=f2, fill=(95, 75, 55, 255))
    return L

def end_card(title, sub):
    bg = Image.new("RGB", (W, H), CREAM); a = np.asarray(bg, float)
    a += np.random.default_rng(3).normal(0, 4, (H, W, 1)); bg = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    logo(bg, 260, "tl", 0); lg = bg.crop((0, 0, 260, 260)); bg.paste(Image.new("RGBA", (260, 260), CREAM + (255,)), (0, 0))
    bg = Image.new("RGBA", (W, H), CREAM + (255,)); bg.paste(lg, ((W - 260) // 2, 560), lg)
    d = ImageDraw.Draw(bg)
    f = font("head", 78, title); tw = d.textlength(title, font=f); d.text(((W - tw) / 2, 880), title, font=f, fill=INK)
    d.line(((W - tw) / 2, 990, (W + tw) / 2, 990), fill=INK, width=3)
    f2 = font("ital", 46, sub); L = wrap(d, sub, f2, W - 220)
    for i, l in enumerate(L): d.text(((W - d.textlength(l, font=f2)) / 2, 1030 + i * 60), l, font=f2, fill=(90, 70, 50))
    return bg

def sfx_scratch(sr, n):
    rng = np.random.default_rng(5); t = np.arange(n) / sr
    x = rng.normal(0, 1, n); x = np.convolve(x, np.ones(6) / 6, "same")                     # paper grain
    env = (0.35 + 0.65 * np.abs(np.sin(2 * np.pi * 3.1 * t))) * np.minimum(1, t * 8) * np.exp(-t * 0.35)
    return x * env * 0.12

def sfx_click(sr):
    n = int(0.12 * sr); t = np.arange(n) / sr
    return (np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 90) + np.random.default_rng(1).normal(0, .5, n) * np.exp(-t * 160)) * 0.5

_vig = None
def grade(fr, t, hits):
    global _vig
    if _vig is None:
        yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W / 2) / (W * .62)) ** 2 + ((yy - H * .42) / (H * .62)) ** 2)
        _vig = np.clip(1.15 - d * 0.75, 0.35, 1)[..., None]
    a = np.asarray(fr, np.float32)
    fl = 0.93 + 0.05 * np.sin(t * 23.0) * np.sin(t * 7.3) + 0.02 * np.sin(t * 61)          # lamp flicker
    a = a * _vig * fl
    g = a.mean(2, keepdims=True); a = g + (a - g) * 0.85                                       # slight desaturation
    a[..., 2] *= 1.04; a[..., 0] *= 0.97                                                       # cold night tint
    a += np.random.default_rng(int(t * 30)).normal(0, 6, (H // 4, W // 4, 1)).repeat(4, 0).repeat(4, 1)   # film grain
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    for h in hits:                                                                             # impact shake
        dt = t - h
        if 0 <= dt < 0.45:
            amp = 18 * (1 - dt / 0.45) * (1.8 if h == hits[-1] else 1)
            r = np.random.default_rng(int(t * 1000))
            dx, dy = int(r.uniform(-amp, amp)), int(r.uniform(-amp, amp))
            im = im.transform((W, H), Image.AFFINE, (1, 0, dx, 0, 1, dy), Image.BILINEAR).resize((W, H))
            z = 1.04; cw, ch = int(W / z), int(H / z); im = im.crop(((W - cw) // 2, (H - ch) // 2, (W + cw) // 2, (H + ch) // 2)).resize((W, H))
    return im

def build(spec):
    tmp = tempfile.mkdtemp()
    intro = frames_of(spec["intro"]); intro_d = len(intro) / FPS
    sc = spec["scenes"]
    for s_ in sc:                                                           # trim lead/tail silence and long inner pauses
        o = f"{tmp}/{os.path.basename(s_['voice'])}.wav"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", s_["voice"], "-af",
                        "silenceremove=start_periods=1:start_threshold=-40dB:stop_periods=-1:stop_duration=0.7:stop_threshold=-40dB,apad=pad_dur=0.15",
                        "-ar", "44100", o], check=True)
        s_["voice"] = o
    vd = [dur(s["voice"]) for s in sc]
    # timeline: scene 0's voice starts over the intro; each later scene lasts its voice + 0.5 s
    intro = intro[:int(min(intro_d, 2.8) * FPS)]; intro_d = len(intro) / FPS        # keep the nib intro short
    starts = [intro_d - XF]; seg = [max(vd[0] - (intro_d - 0.3) + 0.5, 3.4)]
    voice_at = [0.3]
    for i in range(1, len(sc)):
        starts.append(starts[-1] + seg[-1]); voice_at.append(starts[-1] + spec.get('lead', 0.25)); seg.append(vd[i] + spec.get('lead', 0.25) + spec.get('tail', 0.1))
    end_t = starts[-1] + seg[-1]; total = end_t + 3.4
    ri = spec.get("reveal_scene", 3); reveal_t = voice_at[ri] + vd[ri] * spec.get("reveal_frac", 0.55)
    imgs = [big(Image.open(s["image"])) for s in sc]
    caps = [caption(s["text"], s.get("sub", ""), s.get("red", False)) for s in sc]
    endc = end_card(spec["end"]["title"], spec["end"]["sub"])
    lg = logo(Image.new("RGBA", (W, H), (0, 0, 0, 0)), 90, "tr", 64)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-maxrate", "7M", "-bufsize", "14M", "-pix_fmt", "yuv420p", f"{tmp}/v.mp4"], stdin=subprocess.PIPE)
    def scene_frame(k, t):
        p = min(1, max(0, (t - starts[k]) / (seg[k] + XF)))
        return cam(imgs[k], p, k)
    for i in range(int(total * FPS)):
        t = i / FPS
        if t < starts[0]:
            fr = intro[min(i, len(intro) - 1)]
        elif t < starts[0] + XF:                                            # intro -> scene 0 ink reveal
            m = ink_mask((t - starts[0]) / XF, 0)
            a = np.asarray(intro[min(i, len(intro) - 1)], float); b = np.asarray(scene_frame(0, t), float)
            fr = Image.fromarray((a * (1 - m) + b * m).astype(np.uint8))
        elif t < end_t:
            k = max(j for j in range(len(sc)) if starts[j] <= t)
            fr = scene_frame(k, t)
            if k > 0 and t < starts[k] + XF:                                # ink reveal from previous scene
                m = ink_mask((t - starts[k]) / XF, k)
                a = np.asarray(scene_frame(k - 1, t), float); b = np.asarray(fr, float)
                fr = Image.fromarray((a * (1 - m) + b * m).astype(np.uint8))
        else:                                                               # end card ink reveal
            a = np.asarray(scene_frame(len(sc) - 1, t), float); m = ink_mask(min(1, (t - end_t) / XF), 99)
            fr = Image.fromarray((a * (1 - m) + np.asarray(endc.convert("RGB"), float) * m).astype(np.uint8))
        if t < end_t:
            fr = grade(fr, t, [starts[j] for j in range(len(sc))] + [reveal_t])
        fr = fr.convert("RGBA")
        if t < end_t:
            k = max([j for j in range(len(sc)) if voice_at[j] - 0.2 <= t] or [0])
            if t >= voice_at[0] - 0.2:
                lt = t - (voice_at[k] - 0.2); a = min(1, lt / 0.35)
                C = caps[k] if a >= 1 else Image.fromarray((np.asarray(caps[k]) * np.array([1, 1, 1, a])).astype(np.uint8))
                fr = Image.alpha_composite(fr, C)
            fr = Image.alpha_composite(fr, lg)
        ff.stdin.write(fr.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    # audio
    import suspense
    sr = 44100; N = int(total * sr)
    sfx = suspense.score(total, starts[1:], reveal_t, voice_at[-1] - 0.25, end_t)[:N]
    voice = np.zeros(N)
    for k, sp in enumerate(sc):
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", sp["voice"], "-ac", "1", "-ar", str(sr), "-af",
                              "acompressor=threshold=-20dB:ratio=3,equalizer=f=3000:t=q:w=1:g=-2,aecho=0.8:0.5:40|75:0.18|0.10", "-f", "s16le", "-"], capture_output=True).stdout
        v = np.frombuffer(raw, np.int16).astype(float) / 32768; a = int(voice_at[k] * sr)
        e = min(N, a + len(v)); voice[a:e] += v[:e - a]
    voice = voice / max(1e-6, np.abs(voice).max())
    if spec.get("score"):
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", spec["score"], "-ac", "1", "-ar", str(sr), "-f", "s16le", "-"], capture_output=True).stdout
        mus = np.frombuffer(raw, np.int16).astype(float) / 32768
        # line the music's biggest hit (between 40% and 80% of the track) up with the story reveal
        env = np.convolve(np.abs(mus), np.ones(2205) / 2205, "same"); lo, hi = int(len(mus) * .4), int(len(mus) * .8)
        hit = (lo + int(np.argmax(np.diff(env[lo:hi:441])) * 441)) / sr
        off = int(np.clip(reveal_t - hit, -6, 3) * sr); m = np.zeros(N); print('music hit', round(hit,1), 'reveal', round(reveal_t,1))
        src = mus[max(0, -off):]; dst = max(0, off); L = min(N - dst, len(src)); m[dst:dst + L] = src[:L]
        if dst > 0: m[:dst] = 0
        # if the track ends before the reel, bring its opening melody back for the outro
        tenv = np.convolve(np.abs(m), np.ones(4410) / 4410, "same"); live = np.where(tenv > tenv.max() * 0.05)[0]
        tend = live[-1] if len(live) else N
        if tend < N - sr:
            st = max(0, tend - int(1.5 * sr)); need = N - st; rep = mus[int(0.3 * sr):int(0.3 * sr) + need] * 0.8
            xf = int(1.5 * sr); g = np.ones(len(rep)); g[:xf] = np.linspace(0, 1, xf)[:len(g)]
            m[st:st + len(rep)] += rep * g
        fade = int(1.5 * sr); m[N - fade:] *= np.linspace(1, 0, fade)
        m /= max(1e-6, np.abs(m).max())
        venv = np.convolve(np.abs(voice), np.ones(4410) / 4410, "same"); duck = 1 - np.clip(venv * 3, 0, 0.25)
        mix = m * 0.85 * duck + sfx / max(1e-6, np.abs(sfx).max()) * 0.22 + voice * spec.get("voice_level", 0.5)
    else:
        venv = np.convolve(np.abs(voice), np.ones(4410) / 4410, "same"); duck = 1 - np.clip(venv * 6, 0, 0.45)
        mix = sfx * 0.55 * duck + voice * 0.9
    c = sfx_click(sr); a = int((end_t + 1.8) * sr); mix[a:a + len(c)] += c * 0.5
    mix = np.tanh(mix * 1.1) * 0.95
    with wave.open(f"{tmp}/a.wav", "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{tmp}/v.mp4", "-i", f"{tmp}/a.wav", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", spec["out"]], check=True)
    return total

if __name__ == "__main__":
    print(build(json.load(open(sys.argv[1]))))
