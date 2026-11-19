"""Write status/stats.json: followers + per-post numbers for the latest 30 posts (used by the daily report)."""
import json, os, pathlib, urllib.request, urllib.parse, datetime
G = "https://graph.instagram.com/v21.0"; T = os.environ["IG_TOKEN"]; IG = os.environ.get("IG_USER_ID") or "17841462284136363"
def get(path, **p):
    p["access_token"] = T
    try: return json.load(urllib.request.urlopen(f"{G}/{path}?{urllib.parse.urlencode(p)}", timeout=60))
    except Exception as e: return {"error": str(e)[:200]}
out = {"at": datetime.datetime.utcnow().isoformat() + "Z", "profile": get(IG, fields="username,followers_count,media_count"), "posts": []}
for m in get(f"{IG}/media", fields="id,caption,media_type,timestamp,permalink,like_count,comments_count", limit=30).get("data", []):
    ins = get(f"{m['id']}/insights", metric="reach,views,saved,shares,total_interactions")
    m["insights"] = {d["name"]: d["values"][0]["value"] for d in ins.get("data", [])}
    m["caption"] = (m.get("caption") or "")[:80]; out["posts"].append(m)
p = pathlib.Path(__file__).resolve().parent.parent / "status"; p.mkdir(exist_ok=True)
(p / "stats.json").write_text(json.dumps(out, ensure_ascii=False, indent=1)); print("stats saved", len(out["posts"]))
