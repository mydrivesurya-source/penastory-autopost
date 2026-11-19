"""Publish due @pen_a_story posts via the Instagram API with Instagram Login (graph.instagram.com).
Queue files: queue/YYYY-MM-DD-HHMM-<slug>.json (IST date + post time):
  {"type": "image"|"carousel"|"reel"|"story", "caption": str, "media": [url or repo path, ...]}
Posted files move to queue/done/ with the media id and permalink appended to status/posted.jsonl.
Usage: publish.py                -> publish everything whose IST slot has passed (max 3 per run)
       publish.py <prefix>       -> publish queue files starting with <prefix> now
       publish.py --check <prefix> -> build containers and wait until Instagram accepts them, but do NOT publish
"""
import json, os, pathlib, time, urllib.parse, urllib.request, datetime, shutil, sys

G = "https://graph.instagram.com/v21.0"
TOKEN = os.environ["IG_TOKEN"]; IG = os.environ.get("IG_USER_ID") or "17841462284136363"
REPO = os.environ.get("GITHUB_REPOSITORY", "mydrivesurya-source/penastory-autopost")
RAW = f"https://raw.githubusercontent.com/{REPO}/main/"
ROOT = pathlib.Path(__file__).resolve().parent.parent

def call(path, params, method="POST"):
    params = {**params, "access_token": TOKEN}
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f"{G}/{path}?{data.decode()}") if method == "GET" else urllib.request.Request(f"{G}/{path}", data=data, method="POST")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code >= 500 and attempt < 2: time.sleep(15); continue
            raise SystemExit(f"API error {e.code}: {body}")

def url(u): return u if u.startswith("http") else RAW + u.lstrip("/")

def wait_ready(cid, tries=60):
    for _ in range(tries):
        r = call(cid, {"fields": "status_code,status"}, "GET"); s = r.get("status_code")
        if s == "FINISHED": return
        if s == "ERROR": raise SystemExit(f"container {cid} failed: {r}")
        time.sleep(10)
    raise SystemExit(f"container {cid} timed out")

def container(post):
    t, cap, media = post["type"], post.get("caption", ""), [url(m) for m in post["media"]]
    if t == "image":
        cid = call(f"{IG}/media", {"image_url": media[0], "caption": cap})["id"]
    elif t == "reel":
        cid = call(f"{IG}/media", {"media_type": "REELS", "video_url": media[0], "caption": cap, "share_to_feed": "true"})["id"]
    elif t == "story":
        m = media[0]; p = {"media_type": "STORIES"}
        p.update({"video_url": m} if m.lower().endswith(".mp4") else {"image_url": m})
        cid = call(f"{IG}/media", p)["id"]
    elif t == "carousel":
        kids = []
        for m in media[:20]:
            p = {"is_carousel_item": "true"}
            p.update({"media_type": "VIDEO", "video_url": m} if m.lower().endswith(".mp4") else {"image_url": m})
            k = call(f"{IG}/media", p)["id"]; wait_ready(k); kids.append(k)
        cid = call(f"{IG}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": cap})["id"]
    else:
        raise SystemExit(f"unknown type {t}")
    wait_ready(cid); return cid

def log(rec):
    p = ROOT / "status"; p.mkdir(exist_ok=True)
    with open(p / "posted.jsonl", "a") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def main():
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d-%H%M")
    args = [a for a in sys.argv[1:] if a]
    check = "--check" in args; args = [a for a in args if a != "--check"]
    only = args[0] if args else None
    q = ROOT / "queue"; done = q / "done"; done.mkdir(exist_ok=True)
    files = sorted(f for f in q.glob("*.json") if (f.name.startswith(only) if only else f.name[:15] <= now))[:3]
    if not files: print("nothing due at", now); return
    for f in files:
        post = json.loads(f.read_text())
        try:
            cid = container(post)
            if check:
                print("CHECK OK (not published):", f.name, "container", cid); log({"file": f.name, "check": "ok", "at": now}); continue
            mid = call(f"{IG}/media_publish", {"creation_id": cid})["id"]
        except SystemExit as e:
            print("FAILED", f.name, e); log({"file": f.name, "error": str(e)[:400], "at": now}); continue
        link = call(mid, {"fields": "permalink"}, "GET").get("permalink", "")
        print("published", f.name, "->", mid, link)
        log({"file": f.name, "id": mid, "permalink": link, "type": post["type"], "at": now})
        shutil.move(str(f), done / f.name)

if __name__ == "__main__":
    main()
