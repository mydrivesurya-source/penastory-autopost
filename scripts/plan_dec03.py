"""Content plan 3 Dec 2026 (all six slots) for @pen_a_story. Fills the 10th day of the queue (24 Nov - 3 Dec).
Virality review (23 Nov run; latest stats = 22 Nov 21:41 IST, the 23 Nov nightly run had not happened yet). 13 system posts measured.
Raw scores are age-biased (posts <9 h old score ~1.1-1.9), so formats were also compared at the SAME age across the 3 history snapshots:
  - reels: reach 35 / 45 / 42 at ~4 h and 85 / 107 at ~28 h; carousels 5-16 at the same ages -> reels keep a steady 3-6x reach.
    Avg watch 2.4 s -> 3.0 s -> 2.9 s since the short hook. Median virality: reels 2.2 (top), serial 2.0, standalone 1.85,
    memes 1.8, nostalgia 1.5, One Line 1.3 (bottom). No format has 5+ posts yet, so nothing is cut.
  - serial Platform No. 3 is losing readers episode to episode: reach at ~9 h 16 -> 13 -> 11 (virality 1.8 -> 1.9 -> 1.2).
  - 16:30 rotation at ~5 h: memes 1.8 > nostalgia 1.3 = One Line 1.3.
  - Telugu standalone carousels: auto-library 2.4 (reach 17) vs tiffin-note 1.3 (14); every post still has 0 shares / 0 saves / 0 comments.
  - language: Telugu posts median 1.75, English 2.0, but English is mostly reels; carousel-only it is Telugu 1.75 vs English 1.55. 50/50 unchanged.
Decisions applied here:
  (1) serial episodes open with a one-line "Previously" recap on slide 1 so new viewers can join mid-serial (reach falls each episode);
  (2) reels get one more slot as a test: the 19:30 Telugu standalone is told as a Telugu photo reel (5 beats + question);
      if it beats the Telugu carousel median on 4-5 Dec, the 19:30 Telugu standalone becomes a reel on alternate days;
  (3) the 16:30 rotation picks reader memes (best of the rotation at equal age); nostalgia / One Line stay but get no extra slots;
  (4) keep: <=8-word hook in a 2.8 s first beat, twist in the last beat, one "send this to <person>" line per caption.
Language: Telugu 10:30, 16:30, 19:30 · English 13:00, 18:00, 21:30.
Serial #2 The Second Key Ep4 follows the README arc: the trunk opens, the 1984 novel, "Read the last chapter first", Sitara = ammamma (Rukmini);
the last chapter is named "Lakshmi", Ananya's mother (set-up for Ep5).
Chrome was not reachable, so photos are reused from the pool: nothing used on 1-2 Dec (last use <= 30 Nov), none repeated across posts
on 3 Dec (inside one post a photo may return as a deliberate echo).
QC swaps: openbook dropped (cream text on a white page; the note moved into the end slide); bookrow and gma2 get "shade"
(new per-slide darkening in render.photo_slide) because the text sat on bright spines / a light sari. tin3 (train door, never used) carries the Ep5 teaser.
Run: python scripts/plan_dec03.py  -> writes specs/*.json (new files only)"""
import json, pathlib
S = pathlib.Path(__file__).resolve().parent.parent / "specs"; S.mkdir(exist_ok=True)
def U(i): return f"https://images.unsplash.com/photo-{i}?w=1600&q=90"
P = {
 "rainst": "1576514864427-f0809d2b66eb", "door": "1653495482648-0cfd8847bb11", "bookrow": "1495446815901-a7297e633e8d",
 "gma2": "1560885673-4e2f056f6e2a", "readsun": "1506880018603-83d5b814b5a6",
 "lib3": "1524995997946-a1c2e315a42f", "chai1": "1792143663827-c77f1c1f2d71", "auto3": "1626491058156-2daaeea7f578",
 "kitch": "1748323123788-87a32949f4b0", "crkbw": "1706038416284-6c51d61e2f54", "market": "1787044050216-19d30c0aeaf5",
 "char1": "1696941515998-d83f24967aca", "char2": "1750834115164-8c2658f18dd0", "road": "1651678938586-affccc71c270",
 "girl": "1623211270083-5743da6c67ec", "banyan": "1780886729568-cac46e1d8ed1", "diya": "1794550399755-2e72c031cca2",
 "tin3": "1791989642952-32b89c0d9bbf",
}
APP = "Daily stories in Telugu & English — free Pen A Story app, link in bio."
APP_EN = "New stories every day on the free Pen A Story app. Link in bio."

def _new(name):
    f = S / f"{name}.json"
    if f.exists(): raise SystemExit(f"refusing to overwrite {f.name}")
    return f

def carousel(name, label, frames, end, cap):
    keys = []; slides = []
    for f in frames + [end]:
        if f[0] not in keys: keys.append(f[0])
    for f in frames:
        sl = {"image": keys.index(f[0]), "text": f[1]}
        if len(f) > 2 and f[2]: sl["small"] = f[2]
        if len(f) > 3: sl["shade"] = f[3]
        slides.append(sl)
    slides.append({"kind": "end", "image": keys.index(end[0]), "text": end[1], "small": end[2]})
    _new(name).write_text(json.dumps({"kind": "carousel", "style": "photo", "label": label, "images": [U(P[k]) for k in keys],
        "slides": slides, "caption": cap}, ensure_ascii=False, indent=1))

def story(name, photo, title, text="", kicker="", cta=""):
    _new(name).write_text(json.dumps({"kind": "story", "style": "photo", "images": [U(P[photo])], "title": title, "text": text,
        "kicker": kicker, "cta": cta}, ensure_ascii=False, indent=1))

def reel(name, beats, end, cap, music=0):
    keys = []
    for b in beats + [end]:
        if b[0] not in keys: keys.append(b[0])
    B = [dict({"image": keys.index(b[0]), "text": b[1], "dur": b[2]}, **({"small": b[3]} if len(b) > 3 else {})) for b in beats]
    E = {"image": keys.index(end[0]), "text": end[1], "small": end[2]}
    _new(name).write_text(json.dumps({"kind": "reel", "style": "photo", "images": [U(P[k]) for k in keys],
        "beats": B, "end": E, "caption": cap, "music": music}, ensure_ascii=False, indent=1))

D = "2026-12-03"

# ---- 10:30 STORY (Telugu mood) ----
story(f"{D}-1030-story-am", "rainst", "బయట వర్షం.\nలోపల ఒక కథ. 🌧️📖",
      "ఇంకేం కావాలి? మీ rainy-day book ఏది?", "MOOD", "")

# ---- 13:00 SERIAL: The Second Key, Episode 4 (English); slide 1 = "Previously" recap (decision 1) ----
SER = "THE SECOND KEY · SERIAL"
carousel(f"{D}-1300-serial-second-key-ep04", SER,
 [("door", "Previously: behind a plastered wall, a hidden twelfth room. Twelve years of rejection letters to a writer called \"Sitara.\"", "Episode 4"),
  ("door", "Under the desk, a tin trunk with a brass lock. Ananya held up ammamma's key. It turned like it had been waiting forty years."),
  ("bookrow", "No saris. No gold. Four hundred handwritten pages, tied with a sari border. On top, a title: The Second Key. 1984.", "", 0.5),
  ("gma2", "Ananya knew that handwriting. Grocery lists, birthday cards, every letter to Bangalore. Sitara was ammamma.", "", 0.45)],
 ("readsun", "Page one said: \"Read the last chapter first.\" It was called \"Lakshmi.\" Her mother's name.", "Episode 5 · tomorrow 1 PM"),
 "The key finally fits. And the novel inside has a name Ananya knows too well. 🗝️\n\nThe Second Key · Episode 4. New here? Slide 1 catches you up; Episodes 1-3 are just before this post.\n\n"
 "Would you read the last chapter first? Tell us 👇\nSend this to the friend who always reads the ending first.\n" + APP_EN
 + "\n\n#penastory #thesecondkey #serialstory #shortstory #hyderabad")

# ---- 16:30 rotation: reader memes #2 (Telugu mix), decision 3 ----
carousel(f"{D}-1630-memes-readers-2", "READER PROBLEMS",
 [("lib3", "Library కి \"ఒక్క book\" కోసం వెళ్ళాను.\nబయటికి వచ్చేసరికి: 4 books, 2 గంటలు 🙂", "Reader problems 2", 0.35),
  ("chai1", "Book లో climax.\nఅమ్మ: \"టీ చల్లారిపోతోంది!\"\nటీ: already చల్లారిపోయింది ☕"),
  ("auto3", "Auto లో ఒక్క page అనుకుని చదువుతూ, stop దాటి next area కి వెళ్ళిపోవడం 🛺"),
  ("kitch", "అమ్మమ్మ: \"ఎప్పుడూ ఆ phone లోనే!\"\nనేను: అమ్మమ్మా, ఇది novel. 600 pages 📖")],
 ("lib3", "ఇందులో మీరు ఏ number? 1, 2, 3 or 4?", "Comment చేయండి 😂"),
 "\"ఒక్క book\" అని library కి వెళ్ళాం… 😂\n\nఇందులో మీరు ఏ number? Comment చేయండి.\nమీ ఇంట్లో ఎప్పుడూ book పట్టుకుని ఉండే వాళ్ళకి send చేయండి 😂\n" + APP
 + "\n\n#penastory #telugumemes #readermemes #booklovers #tenglish")

# ---- 18:00 REEL (English): <=8-word hook, 2.8 s; twist in the last beat ----
reel(f"{D}-1800-reel-chapter-ten",
 [("crkbw", "He read one chapter a week. Standing up.", 2.8, "A story"),
  ("market", "Near Charminar, a footpath book stall. Every Sunday a boy read one chapter, then put the book back. He couldn't afford it.", 3.8),
  ("char1", "Nine Sundays. Nine chapters. The old seller never said a word. He just never sold that book.", 3.6),
  ("road", "The tenth Sunday, the boy didn't come. Or the next. Or the one after that.", 3.4),
  ("crkbw", "Twenty years later, a parcel reached the stall: a new novel, signed \"For the man who kept chapter ten for me.\"", 4.0, "The author's name was the boy's.")],
 ("char2", "Who kept a book for you?", "Tell us below 👇"),
 "Nine Sundays, nine chapters, one book that was never sold. 📚\n\n"
 "Who kept a book aside for you: a seller, a librarian, an older cousin? Tell us 👇\nSend this to the person who gave you your first book.\n\n" + APP_EN
 + "\n\n#penastory #shortstory #hyderabad #bookstagramindia #readersofinstagram", music=1)

# ---- 19:30 STANDALONE as a Telugu REEL (decision 2 test), twist ending ----
reel(f"{D}-1930-reel-thatha-notebook",
 [("girl", "తాతయ్యకి చదవడం రాదు.", 2.8, "ఒక్క కథ"),
  ("banyan", "అందుకే ప్రతి సాయంత్రం మర్రిచెట్టు కింద నేను ఆయనకి ఒక కథ చదివి వినిపించేవాణ్ణి.", 4.0),
  ("road", "పదేళ్ళు. వందల కథలు. తర్వాత నేను Hyderabad కి job కి వెళ్ళిపోయాను. కథలు ఆగిపోయాయి.", 4.0),
  ("diya", "తాతయ్య వెళ్ళిపోయాక నాన్నమ్మ ఒక పాత notebook ఇచ్చింది. \"నీ కోసం దాచాడు రా.\"", 4.0),
  ("girl", "లోపల వంకర అక్షరాలు. డెబ్భై ఏళ్ళ వయసులో అక్షరాలు నేర్చుకున్నాడు. మొదటి page: \"ఈసారి కథ నేను చెప్తా.\"", 4.4)],
 ("banyan", "మీకు మొదట కథలు చెప్పింది ఎవరు?", "Comment చేయండి 👇"),
 "తాతయ్యకి చదవడం రాదు. అందుకే నేను చదివి వినిపించేవాణ్ణి. 🌳\n\nచివరి beat వరకు చూడండి.\n\n"
 "మీకు మొదట కథలు చెప్పింది ఎవరు — తాతయ్య, అమ్మమ్మ, అమ్మ? Comment చేయండి.\nమీ తాతయ్యని గుర్తు చేసే వాళ్ళకి send చేయండి.\n" + APP
 + "\n\n#penastory #telugustories #thathayya #shortstory #tenglish", music=2)

# ---- 21:30 teaser for Episode 5 (English) ----
story(f"{D}-2130-story-teaser-second-key-ep05", "tin3", "The Second Key · Episode 5",
      "1984. A night train to Bangalore. What ammamma never told anyone about the day Lakshmi left. 🗝️", "TOMORROW", "1 PM")
print("plan 3 Dec written")
