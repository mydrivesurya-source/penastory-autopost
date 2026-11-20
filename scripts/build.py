"""Build specs/*.json into media/ + queue/ for @pen_a_story.
Spec file name: YYYY-MM-DD-HHMM-<slug>.json (IST date + post time). A spec is built once (skipped if its
queue file or queue/done file exists). Kinds:
  carousel: {"kind":"carousel","series":"Six Frames","images":[url],"slides":[{kind,title,lines,n,image}],"caption":..}
  reel:     {"kind":"reel","beats":[{text,dur,style,gold}],"title":..,"end_line":..,"cta":..,"images":[cover url],"caption":..}
  story:    {"kind":"story","kicker":..,"title":..,"text":..,"cta":..,"images":[url]}  or {"kind":"story","video":"media/<reel>.mp4"}
  image:    {"kind":"image", ... same fields as a one-slide carousel}
  video:    {"kind":"video","video":"inbox/<file>.mp4","caption":..}   (Surya's own clip -> logo + 9:16 + posted as a reel)
Captions: value first, max 5 hashtags (Instagram limit), no "less screen time" claims."""
import json, pathlib, hashlib, urllib.request, tempfile, sys, os
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import render

R = pathlib.Path(__file__).resolve().parent.parent
SPECS, MEDIA, Q, CACHE = R / "specs", R / "media", R / "queue", R / ".cache"
for p in (MEDIA, Q, Q / "done", CACHE): p.mkdir(parents=True, exist_ok=True)

def fetch(u):
    if not u.startswith("http"): return Image.open(R / u).convert("RGB")
    f = CACHE / (hashlib.md5(u.encode()).hexdigest() + ".img")
    if not f.exists():
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        f.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    return Image.open(f).convert("RGB")

def check_caption(c):
    tags = [w for w in c.split() if w.startswith("#")]
    if len(tags) > 5: raise SystemExit(f"caption has {len(tags)} hashtags (max 5)")
    if "screen time" in c.lower(): raise SystemExit("caption mentions screen time")

def build(spec_path):
    stem = spec_path.stem
    if (Q / f"{stem}.json").exists() or (Q / "done" / f"{stem}.json").exists(): return False
    if any((R / "hold").rglob(f"{stem}.json")): return False          # held / paused posts are never rebuilt
    s = json.loads(spec_path.read_text()); k = s["kind"]; cap = s.get("caption", "")
    if k != "story": check_caption(cap)
    imgs = [fetch(u) for u in s.get("images", [])]
    if k in ("carousel", "image"):
        slides = s["slides"] if k == "carousel" else [s]
        media = []
        for i, sl in enumerate(slides):
            out = MEDIA / f"{stem}-{i + 1}.jpg"
            if s.get("style") == "photo":
                render.photo_slide(sl, imgs, i, len(slides), s.get("label", "")).save(out, quality=93)
            else:
                render.slide(sl, imgs, i, len(slides), s.get("series", ""), s.get("ep", 0)).save(out, quality=92)
            media.append(f"media/{out.name}")
        post = {"type": "carousel" if len(media) > 1 else "image", "caption": cap, "media": media}
    elif k == "reel":
        out = MEDIA / f"{stem}.mp4"
        with tempfile.TemporaryDirectory() as tmp:
            (render.photo_reel if s.get("style") == "photo" else render.reel)(s, imgs, str(out), tmp)
        post = {"type": "reel", "caption": cap, "media": [f"media/{out.name}"]}
        if s.get("cover_frame") is not False:
            pass
    elif k == "video":
        # a video Surya shared: fit to 1080x1920 (blurred fill, never cropped), Pen A Story logo top-right, keep its audio
        out = MEDIA / f"{stem}.mp4"; src = str(R / s["video"]); lg = str(R / "assets" / "logo.png")
        fc = ("[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:2[bg];"
              "[0:v]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[b];"
              "[1:v]scale=130:130[l];[b][l]overlay=W-w-60:60,format=yuv420p[v]")
        import subprocess
        has_audio = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip()
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", lg, "-filter_complex", fc, "-map", "[v]"]
        cmd += (["-map", "0:a", "-c:a", "aac", "-b:a", "160k"] if has_audio else [])
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30", "-t", "90", "-movflags", "+faststart", str(out)]
        subprocess.run(cmd, check=True)
        post = {"type": "reel", "caption": cap, "media": [f"media/{out.name}"]}
    elif k == "story":
        if s.get("video"):
            post = {"type": "story", "media": [s["video"]]}
        else:
            out = MEDIA / f"{stem}.jpg"
            (render.photo_story(s, imgs) if s.get("style") == "photo" else render.story(s, imgs)).save(out, quality=92)
            post = {"type": "story", "media": [f"media/{out.name}"]}
    else:
        raise SystemExit(f"unknown kind {k}")
    (Q / f"{stem}.json").write_text(json.dumps(post, ensure_ascii=False, indent=1))
    print("built", stem); return True

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    for p in sorted(SPECS.glob("*.json")):
        if p.name.startswith(only):
            try: build(p)
            except Exception as e: print("FAILED", p.name, e)
