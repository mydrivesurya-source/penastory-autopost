"""Nightly stats for @pen_a_story -> status/stats.json (latest) + status/history/YYYY-MM-DD.json (daily snapshot).
Per post: views, reach, likes, comments, saves, shares, follows, profile visits, plus rates per reach.
A 'virality score' ranks posts: shares and saves weigh most (they drive reach), then comments, follows, likes."""
import json, os, pathlib, urllib.request, urllib.parse, datetime
G = "https://graph.instagram.com/v21.0"; T = os.environ["IG_TOKEN"]; IG = os.environ.get("IG_USER_ID") or "17841462284136363"
def get(path, **p):
    p["access_token"] = T
    try: return json.load(urllib.request.urlopen(f"{G}/{path}?{urllib.parse.urlencode(p)}", timeout=60))
    except Exception as e: return {"error": str(e)[:200]}
def insights(mid):
    out = {}
    for m in ["views", "reach", "saved", "shares", "total_interactions", "follows", "profile_visits", "ig_reels_avg_watch_time"]:
        d = get(f"{mid}/insights", metric=m)          # one metric per call: unsupported ones just get skipped
        for x in d.get("data", []): out[x["name"]] = x["values"][0]["value"] if x.get("values") else x.get("total_value", {}).get("value")
    return out
posted = {}
pf = pathlib.Path(__file__).resolve().parent.parent / "status" / "posted.jsonl"
if pf.exists():
    for line in pf.read_text().splitlines():
        try:
            r = json.loads(line)
            if r.get("permalink"): posted[r["permalink"].rstrip("/").split("/")[-1]] = r["file"]
        except Exception: pass
out = {"at": datetime.datetime.utcnow().isoformat() + "Z", "profile": get(IG, fields="username,followers_count,media_count"), "posts": []}
for m in get(f"{IG}/media", fields="id,caption,media_type,media_product_type,timestamp,permalink,like_count,comments_count", limit=40).get("data", []):
    i = insights(m["id"]); reach = max(1, i.get("reach") or 0)
    m["insights"] = i; m["caption"] = (m.get("caption") or "")[:80]
    m["spec"] = posted.get(m.get("permalink", "").rstrip("/").split("/")[-1], "")
    m["rates"] = {k: round((i.get(v) or 0) / reach * 100, 2) for k, v in [("share_rate", "shares"), ("save_rate", "saved"), ("follow_rate", "follows")]}
    m["virality"] = round(3 * (i.get("shares") or 0) + 2 * (i.get("saved") or 0) + 1.5 * (m.get("comments_count") or 0) + 3 * (i.get("follows") or 0) + 0.5 * (m.get("like_count") or 0) + 0.01 * (i.get("views") or 0), 1)
    out["posts"].append(m)
p = pf.parent; (p / "history").mkdir(parents=True, exist_ok=True)
txt = json.dumps(out, ensure_ascii=False, indent=1)
(p / "stats.json").write_text(txt); (p / "history" / f"{datetime.date.today()}.json").write_text(txt)
print("stats saved", len(out["posts"]))
