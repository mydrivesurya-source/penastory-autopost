"""Publish today's queued Instagram posts for @pen_a_story via the Instagram Graph API.
Queue files: queue/YYYY-MM-DD-HHMM-<slug>.json  (IST date + earliest IST post time). Fields:
  type: "image" | "carousel" | "reel" | "story"
  caption: str
  media: [url, ...]   (public URLs; for files in this repo use media/<name>)
Posted files are moved to queue/done/.
"""
import json, os, pathlib, time, urllib.parse, urllib.request, datetime, shutil, sys

G = "https://graph.facebook.com/v21.0"
TOKEN = os.environ["IG_TOKEN"]; IG = os.environ["IG_USER_ID"]
REPO = os.environ.get("GITHUB_REPOSITORY", "")
RAW = f"https://raw.githubusercontent.com/{REPO}/main/"

def call(path, params, method="POST"):
    params = {**params, "access_token": TOKEN}
    data = urllib.parse.urlencode(params).encode()
    if method == "GET":
        req = urllib.request.Request(f"{G}/{path}?{data.decode()}")
    else:
        req = urllib.request.Request(f"{G}/{path}", data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"API error {e.code}: {e.read().decode()}")

def url(u): return u if u.startswith("http") else RAW + u.lstrip("/")

def wait_ready(cid, tries=60):
    for _ in range(tries):
        s = call(cid, {"fields": "status_code"}, "GET").get("status_code")
        if s == "FINISHED": return
        if s == "ERROR": raise SystemExit(f"container {cid} failed: {call(cid, {'fields': 'status'}, 'GET')}")
        time.sleep(10)
    raise SystemExit(f"container {cid} timed out")

def publish(post):
    t, cap, media = post["type"], post.get("caption", ""), [url(m) for m in post["media"]]
    if t == "image":
        cid = call(f"{IG}/media", {"image_url": media[0], "caption": cap})["id"]
    elif t == "reel":
        cid = call(f"{IG}/media", {"media_type": "REELS", "video_url": media[0], "caption": cap, "share_to_feed": "true"})["id"]
    elif t == "story":
        m = media[0]
        p = {"media_type": "STORIES"}
        p.update({"video_url": m} if m.lower().endswith(".mp4") else {"image_url": m})
        cid = call(f"{IG}/media", p)["id"]
    elif t == "carousel":
        kids = []
        for m in media[:10]:
            p = {"is_carousel_item": "true"}
            p.update({"media_type": "VIDEO", "video_url": m} if m.lower().endswith(".mp4") else {"image_url": m})
            k = call(f"{IG}/media", p)["id"]; wait_ready(k); kids.append(k)
        cid = call(f"{IG}/media", {"media_type": "CAROUSEL", "children": ",".join(kids), "caption": cap})["id"]
    else:
        raise SystemExit(f"unknown type {t}")
    wait_ready(cid)
    return call(f"{IG}/media_publish", {"creation_id": cid})["id"]

def main():
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d-%H%M")
    only = sys.argv[1] if len(sys.argv) > 1 else None
    q = pathlib.Path("queue"); done = q / "done"; done.mkdir(exist_ok=True)
    # due = slot time already passed (catches missed slots too); at most 2 per run to stay natural
    files = sorted(f for f in q.glob("*.json") if (f.name.startswith(only) if only else f.name[:15] <= now))[:3]
    if not files: print("nothing due at", now); return
    for f in files:
        try:
            mid = publish(json.loads(f.read_text()))
        except SystemExit as e:
            print("API error on", f.name, e); continue
        print("published", f.name, "->", mid)
        shutil.move(str(f), done / f.name)

if __name__ == "__main__":
    main()
