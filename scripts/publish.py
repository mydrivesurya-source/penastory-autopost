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

import subprocess
def git(*a, check=True):
    return subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, check=check)

def sync():
    """Bring the checkout to the newest main before deciding anything (never act on a stale snapshot)."""
    git("fetch", "-q", "origin", "main"); git("reset", "-q", "--hard", "origin/main")

def ledger():
    f = ROOT / "status" / "posted.jsonl"
    return {json.loads(l)["file"] for l in f.read_text().splitlines() if l.strip() and '"id"' in l} if f.exists() else set()

def save(msg, tries=6):
    """Commit + push right away; rebase and retry if someone else pushed first."""
    git("add", "-A", "queue", "status"); 
    if git("diff", "--cached", "--quiet", check=False).returncode == 0: return True
    git("-c", "user.name=pas-bot", "-c", "user.email=bot@users.noreply.github.com", "commit", "-qm", msg)
    for i in range(tries):
        if git("push", "-q", "origin", "HEAD:main", check=False).returncode == 0: return True
        git("pull", "-q", "--rebase", "origin", "main", check=False); time.sleep(3 + 3 * i)
    raise SystemExit("could not save posted state - stopping to avoid duplicates")

def recent_captions():
    try:
        d = call(f"{IG}/media", {"fields": "caption,timestamp", "limit": 25}, "GET").get("data", [])
    except SystemExit: return set()
    cut = datetime.datetime.utcnow() - datetime.timedelta(hours=24)
    return {(m.get("caption") or "").strip()[:120] for m in d
            if m.get("caption") and datetime.datetime.strptime(m["timestamp"][:19], "%Y-%m-%dT%H:%M:%S") > cut}

def log(rec):
    p = ROOT / "status"; p.mkdir(exist_ok=True)
    with open(p / "posted.jsonl", "a") as f: f.write(json.dumps(rec, ensure_ascii=False) + "\n")

def main():
    args = [a for a in sys.argv[1:] if a]
    check = "--check" in args; args = [a for a in args if a != "--check"]
    only = args[0] if args else None
    if not check: sync()
    now = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime("%Y-%m-%d-%H%M")
    q = ROOT / "queue"; done = q / "done"; done.mkdir(exist_ok=True)
    files = sorted(f for f in q.glob("*.json") if (f.name.startswith(only) if only else f.name[:15] <= now))[:3]
    if not files: print("nothing due at", now); return
    posted = ledger(); caps = None
    for f in files:
        if not check:
            sync()                                             # re-check the newest state before EVERY post
            if not f.exists() or f.name in ledger(): print("already posted, skip", f.name); continue
        post = json.loads(f.read_text())
        if f.name in posted:                                   # posted earlier but not moved: just move it
            shutil.move(str(f), done / f.name); save(f"Mark posted {f.name}"); continue
        cap = (post.get("caption") or "").strip()[:120]
        if cap and not check:
            caps = recent_captions() if caps is None else caps
            if cap in caps:                                    # Instagram already has this exact post
                print("duplicate caption on Instagram, skip", f.name); log({"file": f.name, "id": "dup-skip", "at": now})
                shutil.move(str(f), done / f.name); save(f"Skip duplicate {f.name}"); continue
        try:
            cid = container(post)
            if check:
                print("CHECK OK (not published):", f.name, "container", cid); continue
            mid = call(f"{IG}/media_publish", {"creation_id": cid})["id"]
        except SystemExit as e:
            print("FAILED", f.name, e); log({"file": f.name, "error": str(e)[:400], "at": now}); save(f"Failed {f.name}"); continue
        shutil.move(str(f), done / f.name)                    # mark first, then fetch the link
        log({"file": f.name, "id": mid, "type": post["type"], "at": now}); save(f"Posted {f.name}")
        try: link = call(mid, {"fields": "permalink"}, "GET").get("permalink", "")
        except SystemExit: link = ""
        print("published", f.name, "->", mid, link)
        if link: log({"file": f.name, "id": mid, "permalink": link, "type": post["type"], "at": now}); save(f"Link {f.name}")
        caps = None

if __name__ == "__main__":
    main()
