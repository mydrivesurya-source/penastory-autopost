"""Content plan 29 (21:30 teaser) - 30 Nov 2026 for @pen_a_story. Fills the gap after plan_nov20_29.py.
Starts serial #2: *The Second Key* (English, 8 episodes, 30 Nov - 7 Dec; outline in README "Serials").
No stats existed yet at planning time (first nightly stats run is 20 Nov after 21:40), so this day follows the
standing mix; photos are reused from the pool with nothing repeated from 27-29 Nov and none repeated across posts on 30 Nov.
Run: python scripts/plan_nov29_30.py  -> writes specs/*.json (new files only)"""
import json, pathlib
S = pathlib.Path(__file__).resolve().parent.parent / "specs"; S.mkdir(exist_ok=True)
def U(i): return f"https://images.unsplash.com/photo-{i}?w=1600&q=90"
P = {
 "auto1": "1626149637281-4e227308da18", "auto2": "1564291886459-a39ad7415125", "auto3": "1626491058156-2daaeea7f578",
 "banyan": "1780886729568-cac46e1d8ed1", "banyan2": "1786468539777-fa9c5eae293d", "road": "1651678938586-affccc71c270",
 "crow": "1682467612877-f9b5e55ff2af", "crow2": "1572608705929-0e245b6fa24d",
 "door": "1653495482648-0cfd8847bb11", "door2": "1583008520412-7ee838891ada", "crkbw": "1706038416284-6c51d61e2f54",
 "openbook": "1476275466078-4007374efbbe", "readsun": "1506880018603-83d5b814b5a6", "bookrow": "1495446815901-a7297e633e8d",
 "gma2": "1560885673-4e2f056f6e2a", "gma3": "1496813146940-1601b02f81a4", "kitch": "1748323123788-87a32949f4b0",
 "chai1": "1792143663827-c77f1c1f2d71", "chai2": "1786161320176-96236ee66981", "rainst": "1576514864427-f0809d2b66eb",
 "tin2": "1763801572504-e7fd828d7bf5",
}
APP = "Daily stories in Telugu & English — free Pen A Story app, link in bio."
APP_EN = "New stories every day on the free Pen A Story app. Link in bio."

def carousel(name, label, frames, end, cap):
    keys = []; slides = []
    for f in frames + [end]:
        if f[0] not in keys: keys.append(f[0])
    for f in frames:
        sl = {"image": keys.index(f[0]), "text": f[1]}
        if len(f) > 2 and f[2]: sl["small"] = f[2]
        slides.append(sl)
    slides.append({"kind": "end", "image": keys.index(end[0]), "text": end[1], "small": end[2]})
    (S / f"{name}.json").write_text(json.dumps({"kind": "carousel", "style": "photo", "label": label, "images": [U(P[k]) for k in keys],
        "slides": slides, "caption": cap}, ensure_ascii=False, indent=1))

def story(name, photo, title, text="", kicker="", cta=""):
    (S / f"{name}.json").write_text(json.dumps({"kind": "story", "style": "photo", "images": [U(P[photo])], "title": title, "text": text,
        "kicker": kicker, "cta": cta}, ensure_ascii=False, indent=1))

def reel(name, beats, end, cap, music=0):
    keys = []
    for b in beats + [end]:
        if b[0] not in keys: keys.append(b[0])
    B = [dict({"image": keys.index(b[0]), "text": b[1], "dur": b[2]}, **({"small": b[3]} if len(b) > 3 else {})) for b in beats]
    E = {"image": keys.index(end[0]), "text": end[1], "small": end[2]}
    (S / f"{name}.json").write_text(json.dumps({"kind": "reel", "style": "photo", "images": [U(P[k]) for k in keys],
        "beats": B, "end": E, "caption": cap, "music": music}, ensure_ascii=False, indent=1))

def book(name, cover, title, small):
    f = S / f"{name}.json"; d = json.loads(f.read_text()); d["images"].append(f"assets/covers/{cover}"); i = len(d["images"]) - 1
    if d["kind"] == "reel": d["book"] = {"image": i, "text": title, "small": small}
    else: d["slides"].append({"kind": "book", "image": i, "text": title, "small": small})
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1))

D = "2026-11-30"

# ---- 29 Nov 21:30: launch teaser for serial #2 (English) ----
story("2026-11-29-2130-story-teaser-second-key", "door2", "New serial: The Second Key",
      "Ammamma's house had eleven doors. Her key fit none of them. Tomorrow, 1 PM 🗝️", "NEW ENGLISH SERIAL", "1 PM")

# ---- 10:30 story (Telugu) ----
story(f"{D}-1030-story-am", "chai2", "Monday: ముందు chai.\nతర్వాతే ప్రపంచం ☕", "కొత్త English serial ఈ రోజు 1 PM 🗝️", "MONDAY MOOD")

# ---- 13:00 SERIAL: The Second Key, Episode 1 (English) ----
SER = "THE SECOND KEY · SERIAL"
carousel(f"{D}-1300-serial-second-key-ep01", SER,
 [("door2", "Old City, Hyderabad. Ammamma's house had been locked for three years. Ananya came to sell it.", "Episode 1"),
  ("crkbw", "The broker wanted the keys by Friday. \"Old houses sell fast, madam. Old memories don't.\""),
  ("openbook", "In ammamma's last book, between pages 88 and 89, she found a small brass key."),
  ("readsun", "Folded around it, a note in ammamma's handwriting: \"Not for the doors you can see.\""),
  ("door", "Ananya counted. Eleven doors. She tried every single lock. The key fit none.")],
 ("door2", "So where is the door this key opens?", "Episode 2 · tomorrow 1 PM"),
 "Ammamma's house had eleven doors. Her key fit none of them. 🗝️\n\nThe Second Key · Episode 1. Our new English serial, a new episode every day at 1 PM. Swipe to the cliffhanger.\n\n"
 "Where do you think the twelfth door is? Guess below 👇\n" + APP_EN + "\n\n#penastory #thesecondkey #serialstory #shortstory #hyderabad")

# ---- 16:30 rotation: nostalgia (Telugu) ----
carousel(f"{D}-1630-nostalgia-tenali-crows", "చిన్నప్పటి కథలు · NOSTALGIA",
 [("crow", "ఒక రోజు Krishnadevaraya court లో ఒక వింత ప్రశ్న అడిగాడు.", "తెనాలి – కాకుల లెక్క"),
  ("banyan", "\"మన Vijayanagara లో ఎన్ని కాకులు ఉన్నాయి? రేపటికల్లా లెక్క చెప్పాలి.\""),
  ("road", "Ministers తలలు పట్టుకున్నారు. Tenali Rama మాత్రం నవ్వుతూ ఇంటికి వెళ్ళాడు."),
  ("crow2", "మర్నాడు: \"ప్రభూ, సరిగ్గా 99,999 కాకులు.\" \"తక్కువ ఉంటే?\" \"కొన్ని చుట్టాల ఇంటికి వెళ్ళాయి.\""),
  ("banyan2", "\"మరి ఎక్కువ ఉంటే?\" \"చుట్టాలు మన ఊరికి వచ్చాయి, ప్రభూ.\" Court అంతా నవ్వులే.")],
 ("crow", "Tenali కథల్లో మీకు ఏది ఎక్కువ నవ్వు తెప్పిస్తుంది?", "Comment చేయండి 😄"),
 "తెనాలి రామకృష్ణ vs కాకుల లెక్క 🐦‍⬛ ఈ కథ గుర్తుందా?\n\nచిన్నప్పుడు అమ్మమ్మ, తాతయ్య, Chandamama చెప్పిన కథలు — మళ్ళీ ఒకసారి.\n\n"
 "Tenali కథల్లో మీ favourite ఏది?\n\nమీ childhood friend ని tag చేయండి — వాళ్ళకీ గుర్తొస్తుంది.\n" + APP + "\n\n#penastory #tenaliramakrishna #telugukathalu #childhoodmemories #nostalgia")

# ---- 18:00 REEL (English) ----
reel(f"{D}-1800-reel-meter-down",
 [("rainst", "2 AM. Rain. A man running down Koti road, waving at every auto.", 3.4, "A story"),
  ("auto3", "Only Salim stopped. In the back seat, the man's wife. In labour.", 3.4),
  ("auto2", "Salim drove through the empty city like it was his own family. He never switched the meter on.", 3.8),
  ("auto1", "Twenty-four years later, a young doctor waved down his auto outside the hospital.", 3.6),
  ("chai1", "\"You won't remember me, uncle. You drove me here before I was born.\"", 3.8, "Some fares get paid back late.")],
 ("auto3", "Who's the stranger your family still talks about?", "Tell us below 👇"),
 "2 AM. Rain. One auto driver who never switched the meter on. 🛺\n\nWho's the stranger your family still talks about? Tell us 👇\n\n" + APP_EN
 + "\n\n#penastory #shortstory #storytelling #hyderabad #readersofinstagram", music=1)

# ---- 19:30 STANDALONE (Telugu) ----
carousel(f"{D}-1930-story-ammamma-reading", "PEN A STORY · ఒక్క కథ",
 [("gma2", "అమ్మమ్మకి 82. కళ్ళు సరిగ్గా కనిపించవు. అయినా ప్రతి సాయంత్రం Ramayana పుస్తకం ఒళ్ళో పెట్టుకుంటుంది.", "ఒక్క కథ · ఆమె చదవని పుస్తకం"),
  ("readsun", "అందుకే రోజూ 6 గంటలకి నేను చదువుతాను. ఆమె కళ్ళు మూసుకుని వింటుంది."),
  ("kitch", "ఒక రోజు cricket match ఉందని ఒక page skip చేశాను. ఎవరికీ తెలియదు అనుకున్నా."),
  ("gma3", "అమ్మమ్మ నవ్వింది: \"Hanuman ఇంకా సముద్రం దాటలేదు రా. ఒక page వెనక్కి వెళ్ళు.\""),
  ("bookrow", "అప్పుడు తెలిసింది — ఆ పుస్తకం మొత్తం ఆమెకి కంఠతా వచ్చు. 60 years నుంచి."),
  ("gma2", "\"మరి నన్ను ఎందుకు చదవమన్నావు?\" \"నువ్వు రోజూ ఒక గంట నా పక్కన కూర్చోవాలని.\"")],
 ("readsun", "మీ అమ్మమ్మ, తాతయ్యలతో మీ daily ritual ఏది?", "Comment చేయండి 📖"),
 "అమ్మమ్మకి కళ్ళు కనిపించవు. అయినా రోజూ ఒక పుస్తకం ఒళ్ళో పెట్టుకుంటుంది. ఎందుకు? 📖\n\nఒక్క post లో పూర్తి కథ — చివరి వరకు swipe చేయండి.\n\n"
 "మీ అమ్మమ్మ, తాతయ్యలతో మీ daily ritual ఏది? Comment చేయండి.\n\nఈ కథ ఎవరికైనా గుర్తు చేస్తే, వాళ్ళకి send చేయండి.\n" + APP
 + "\n\n#penastory #telugustories #shortstory #ammamma #tenglish")
book(f"{D}-1930-story-ammamma-reading", "ramayana.jpg", "Ramayana", "Vamsi Krishna Dasari · అమ్మమ్మ కథలు, పిల్లల కోసం బొమ్మలతో")

# ---- 21:30 teaser for Episode 2 (English); Episode 2 opens on the tin2 photo (Jaffer uncle) ----
story(f"{D}-2130-story-teaser-second-key-ep02", "tin2", "The Second Key · Episode 2",
      "The old man next door knew something. Tomorrow, 1 PM 🔔", "TOMORROW", "1 PM")
print("plan 29-30 Nov written")
