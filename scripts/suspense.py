"""Original suspense score + sound design for story reels (no licensed audio).
Layers: sub drone, dissonant string pad, clock tick, heartbeat, impact 'braam' hits,
reverse-swell risers, steam-train horn + rumble, sudden silences."""
import numpy as np

SR = 44100

def _lp(x, a):  # one-pole low-pass
    y = np.empty_like(x); s = 0.0
    for i in range(0, len(x), 4096):
        seg = x[i:i + 4096]; out = np.empty_like(seg)
        for j, v in enumerate(seg):
            s += a * (v - s); out[j] = s
        y[i:i + 4096] = out
    return y

def lp(x, cutoff):
    # fast FFT low-pass
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cutoff) ** 4); return np.fft.irfft(X, len(x))

def hp(x, cutoff):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (cutoff / np.maximum(f, 1)) ** 4); return np.fft.irfft(X, len(x))

def reverb(x, decay=1.8, mix=0.35, seed=0):
    n = int(decay * SR); t = np.arange(n) / SR
    ir = np.random.default_rng(seed).normal(0, 1, n) * np.exp(-t * 6.9 / decay)
    ir = lp(ir, 4000); ir /= np.abs(ir).sum() / 40
    N = len(x) + n; L = 1 << (N - 1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(x, L) * np.fft.rfft(ir, L), L)[:len(x)]
    return x * (1 - mix) + wet * mix

def saw(f, t, rng):
    ph = rng.uniform(0, 1)
    return 2 * ((f * t + ph) % 1) - 1

def drone(n, root=36.7, seed=0):
    rng = np.random.default_rng(seed); t = np.arange(n) / SR
    x = sum(saw(root * d, t, rng) for d in (1, 1.004, 0.996, 2.002)) / 4
    x = lp(x, 160) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.11 * t))
    return x

def pad(n, freqs, seed=1):
    """Dissonant string-like pad (minor 2nd clusters) with slow swell."""
    rng = np.random.default_rng(seed); t = np.arange(n) / SR; x = np.zeros(n)
    for f in freqs:
        for d in (0.997, 1.0, 1.003):
            vib = 1 + 0.003 * np.sin(2 * np.pi * rng.uniform(4.5, 5.5) * t + rng.uniform(0, 6))
            x += saw(f * d, t * vib, rng)
    x = lp(x / (3 * len(freqs)), 1400)
    return x

def tick(seed=0):
    n = int(0.05 * SR); t = np.arange(n) / SR; r = np.random.default_rng(seed)
    return (r.normal(0, 1, n) * np.exp(-t * 300) + np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 250) * 0.6) * 0.5

def heartbeat():
    def thump(f, a):
        n = int(0.22 * SR); t = np.arange(n) / SR
        return np.sin(2 * np.pi * f * t * (1 - t * 1.5)) * np.exp(-t * 22) * a
    b = np.zeros(int(0.6 * SR)); a = thump(58, 1.0); b[:len(a)] += a
    s = int(0.19 * SR); c = thump(50, 0.7); b[s:s + len(c)] += c
    return b

def braam(dur=2.6, f=41.2, seed=3):
    """Cinematic low brass-like impact."""
    n = int(dur * SR); t = np.arange(n) / SR; rng = np.random.default_rng(seed)
    x = sum(saw(f * m * d, t, rng) for m in (1, 1.5, 2) for d in (0.995, 1.005))
    env = np.minimum(1, t / 0.02) * np.exp(-t * 1.3)
    x = lp(x / 6, 900) * env
    sub = np.sin(2 * np.pi * 32 * t * (1 - 0.15 * t)) * np.exp(-t * 2.5) * 1.2
    noise = lp(rng.normal(0, 1, n), 2500) * np.exp(-t * 18) * 0.6
    return reverb(x + sub + noise, 2.5, 0.4, seed)

def riser(dur=2.0, seed=4):
    n = int(dur * SR); t = np.arange(n) / SR; p = t / dur; rng = np.random.default_rng(seed)
    nz = rng.normal(0, 1, n)
    X = np.fft.rfft(nz); fr = np.fft.rfftfreq(n, 1 / SR); X *= np.exp(-((np.log(fr + 1) - np.log(800)) ** 2) / 2)
    x = np.fft.irfft(X, n) * 6 * p ** 3
    tone = np.sin(2 * np.pi * (200 * t + 900 * t ** 2 / dur)) * p ** 4 * 0.25
    return x + tone

def train_horn(dur=2.4, seed=5):
    n = int(dur * SR); t = np.arange(n) / SR; rng = np.random.default_rng(seed)
    env = np.minimum(1, t / 0.15) * np.minimum(1, (dur - t) / 0.6)
    x = sum(saw(f * (1 + 0.004 * np.sin(2 * np.pi * 5 * t)), t, rng) for f in (277.2, 349.2, 415.3))
    x = lp(x / 3, 1600) * env * 0.5
    return reverb(x, 3.5, 0.55, seed)

def rumble(n, seed=6):
    t = np.arange(n) / SR; r = np.random.default_rng(seed)
    x = lp(r.normal(0, 1, n), 120) * 3
    chug = (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 2.2 * t)))
    return x * chug

def place(mix, clip, at, gain=1.0):
    a = int(at * SR)
    if a >= len(mix): return
    e = min(len(mix), a + len(clip)); mix[a:e] += clip[:e - a] * gain

def score(total, cuts, reveal_at, silence_at, end_at):
    """cuts: scene-change times (impacts); reveal_at: the big line; silence_at: drop-out moment; end_at: end card."""
    n = int(total * SR); t = np.arange(n) / SR; mix = np.zeros(n)
    # tension bed grows over time
    grow = np.clip(t / max(reveal_at, 1), 0, 1)
    mix += drone(n) * (0.35 + 0.35 * grow)
    mix += pad(n, [110, 116.5, 164.8]) * (0.05 + 0.18 * grow)
    mix += hp(pad(n, [659.3, 698.5], 7), 400) * np.clip((t - reveal_at + 6) / 6, 0, 1) * 0.05   # high violin tension near reveal
    # clock ticks, speeding up toward the reveal
    k, tt = 0, 0.4
    while tt < reveal_at:
        place(mix, tick(k), tt, 0.35); k += 1
        tt += max(0.38, 1.0 - 0.6 * tt / reveal_at)
    # heartbeat in the back half
    tt = reveal_at - 7
    while tt < end_at - 0.5:
        if tt > 0: place(mix, heartbeat(), tt, 0.9)
        tt += 0.75 if tt < reveal_at else 0.62
    # impacts on scene cuts, big one on reveal
    for c in cuts: place(mix, braam(1.8, 55, int(c * 10)) , c - 0.02, 0.45)
    place(mix, riser(2.2), reveal_at - 2.2, 0.55)
    place(mix, braam(3.5, 41.2, 99), reveal_at, 1.0)
    # train: distant horn at start, rumble + horn at the end
    place(mix, train_horn(2.6), 0.2, 0.35)
    place(mix, rumble(int((end_at - silence_at + 3) * SR)), silence_at - 1, 0.45)
    place(mix, train_horn(3.0, 8), end_at - 2.6, 0.55)
    # sudden silence just before the final question (everything but voice drops)
    s = int(silence_at * SR); g = np.ones(n)
    g[s:s + int(0.12 * SR)] = np.linspace(1, 0.08, int(0.12 * SR))[:len(g[s:s + int(0.12 * SR)])]
    g[s + int(0.12 * SR):] = 0.08
    ret = int((silence_at + 1.6) * SR); m = min(n, ret + int(0.8 * SR))
    if ret < n: g[ret:m] = np.linspace(0.08, 0.7, m - ret); g[m:] = 0.7
    mix *= g
    place(mix, braam(4.0, 36.7, 77), end_at, 0.7)
    return mix
