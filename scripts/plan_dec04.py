"""Content plan 4 Dec 2026 (all six slots) for @pen_a_story. Fills the 10th day of the queue (25 Nov - 4 Dec).
Virality review (24 Nov run; latest stats = 23 Nov 21:44 IST, the 24 Nov nightly run had not happened yet). 17 system posts measured.
Compared at equal age across the 4 history snapshots (raw scores punish posts <9 h old):
  - format medians: reel 2.35 (4 posts, top), memes 1.8 (1), serial 1.65 (4), nostalgia 1.5 (1), One Line 1.4 (1),
    standalone carousel 1.4 (5 posts, bottom third), author call-out 1.2 (1).
  - standalone carousels are the first format with 5 posts and sit in the bottom third -> fewer slots: the 19:30 Telugu standalone is a
    photo reel again (2nd run of the 3 Dec test). Within standalones the reading/book-centred stories won (library-card 2.6, auto-library 2.4)
    and the general slice-of-life ones lost (tiffin 1.4, cricket 1.2, umbrella 1.1) -> every story today has a book or reading at its core.
  - serial reach at ~9 h keeps falling but flattening: 16 -> 13 -> 11 -> 10. Recap slide (from 3 Dec) stays.
  - reel power-cut: reach only 6 at 3.7 h (earlier reels 35-45) BUT avg watch 12.6 s vs 2.2-3.5 s before. One data point; watch on 24 Nov snapshot.
    It is the first nostalgia/ammamma reel with a book end card -> today's English reel ends on a matching book card to test it again.
  - 16:30: author call-out weakest (1.2, reach 7 at 5 h); memes best. Nostalgia reworked: hook = "ఈ కథ గుర్తుందా?", a "guess the ending" slide
    before the reveal (comments are still 0 on every post), max ~20 words a slide.
  - still 0 shares / 0 saves / 0 comments; followers 461 -> 460 flat.
Language: Telugu 10:30, 16:30, 19:30 · English 13:00, 18:00, 21:30.
Serial #2 The Second Key Ep5 follows the README arc: the last chapter "Lakshmi" -- 1984, Lakshmi leaves on the night train to Bangalore,
Rukmini (ammamma) watched from the platform and never stopped her; last line sets up Ep6 (Ananya calls her mother).
Chrome was not reachable, so photos are reused from the pool: only these 14 were unused on 1-3 Dec; each is used in one post today
(inside one post a photo may return as a deliberate echo). The fresh-photo pool is now exhausted for 5 Dec -> next run needs Chrome or must
relax to a 2-day gap.
Run: python scripts/plan_dec04.py  -> writes specs/*.json (new files only)"""
import json, pathlib
S = pathlib.Path(__file__).resolve().parent.parent / "specs"; S.mkdir(exist_ok=True)
def U(i): return f"https://images.unsplash.com/photo-{i}?w=1600&q=90"
P = {
 "chai2": "1786161320176-96236ee66981", "let2": "1780536890742-a3d937535d66", "st4": "1653494656006-869fdf081d42",
 "water": "1768052271115-3a01d2b042b9", "vwomen": "1759738098462-90ffac98c554", "banyan2": "1786468539777-fa9c5eae293d",
 "openbook": "1476275466078-4007374efbbe", "auto2": "1564291886459-a39ad7415125", "bedread2": "1528436610461-e9be9d1f7d6b",
 "gma3": "1496813146940-1601b02f81a4", "auto1": "1626149637281-4e227308da18", "crow": "1682467612877-f9b5e55ff2af",
 "crow2": "1572608705929-0e245b6fa24d", "clock": "1774904721886-7b3abd03be14",
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


def book(name, cover, title, small):
    f = S / f"{name}.json"; d = json.loads(f.read_text()); d["images"].append(f"assets/covers/{cover}"); i = len(d["images"]) - 1
    if d["kind"] == "reel": d["book"] = {"image": i, "text": title, "small": small}
    else: d["slides"].append({"kind": "book", "image": i, "text": title, "small": small})
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1))

D = "2026-12-04"

# ---- 10:30 STORY (Telugu mood) ----
story(f"{D}-1030-story-am", "chai2", "చలి పొద్దున్న.\nవేడి chai. ఒక్క chapter. ☕📖",
      "ఒక్క chapter అని మొదలుపెట్టి ఎన్ని చదువుతారు?", "MOOD", "")

# ---- 13:00 SERIAL: The Second Key, Episode 5 (English); slide 1 = "Previously" recap ----
SER = "THE SECOND KEY · SERIAL"
carousel(f"{D}-1300-serial-second-key-ep05", SER,
 [("let2", "Previously: ammamma's secret 1984 novel. Page one said \"Read the last chapter first.\" It was called \"Lakshmi.\" Her mother's name.", "Episode 5", 0.3),
  ("st4", "The chapter opened at Kacheguda station. 1984. 11:40 PM. A girl of nineteen, one suitcase, a ticket to Bangalore.", "", 0.3),
  ("let2", "Her father had said: \"If you get on that train, don't come back.\" Lakshmi got on.", "", 0.4),
  ("st4", "Ammamma wrote that she was there too. Behind a pillar. She didn't stop her. She just watched the train go.", "", 0.3)],
 ("let2", "The last line: \"She never knew I came. One day, her daughter will tell her.\"", "Episode 6 · tomorrow 1 PM"),
 "1984. A night train. A mother behind a pillar who never said goodbye. 🚉\n\nThe Second Key · Episode 5. New here? Slide 1 catches you up; Episodes 1-4 are just before this post.\n\n"
 "Should Ananya tell her mother? Yes or no 👇\nSend this to the one who'd wait on a platform for you.\n" + APP_EN
 + "\n\n#penastory #thesecondkey #serialstory #shortstory #hyderabad")

# ---- 16:30 rotation: nostalgia (Telugu mix), reworked hook + guess slide ----
carousel(f"{D}-1630-nostalgia-birbal-well", "కథ గుర్తుందా? · AKBAR-BIRBAL",
 [("water", "ఈ కథ గుర్తుందా? 🪣\nబావి అమ్మేశాడు. కానీ నీళ్ళు అమ్మలేదట!", "Akbar-Birbal"),
  ("vwomen", "ఒక రైతు పక్కింటి వాడి దగ్గర బావి కొన్నాడు. మర్నాడు నీళ్ళు తోడబోతే: \"బావి నీది. నీళ్ళు నావి!\""),
  ("banyan2", "గొడవ Akbar దర్బారు దాకా వెళ్ళింది. అందరూ Birbal వైపు చూశారు.", "", 0.3),
  ("vwomen", "Birbal ఏమన్నాడో guess చేయండి. Next slide కి ముందే comment లో చెప్పండి 👇")],
 ("water", "\"నీళ్ళు నీవైతే, నా బావిలో ఉంచినందుకు అద్దె కట్టు. లేదా ఈరోజే తీసుకెళ్ళు!\"", "మీకు ఇష్టమైన Birbal కథ ఏది?"),
 "బావి అమ్మేశాడు, నీళ్ళు కాదట! 😂 ఈ కథ గుర్తుందా?\n\nBirbal answer చూసే ముందు మీ guess comment చేయండి.\nChandamama కథలు గుర్తున్న మీ friend కి send చేయండి.\n" + APP
 + "\n\n#penastory #akbarbirbal #telugukathalu #childhoodstories #nostalgia")

# ---- 18:00 REEL (English): <=8-word hook 2.8 s, twist last beat, book card test ----
reel(f"{D}-1800-reel-ticket-bookmark",
 [("openbook", "The bookmark was a train ticket. 1999.", 2.8, "A story"),
  ("auto2", "Abids Sunday book market. ₹40 for a worn copy of amma's favourite novel.", 3.4),
  ("bedread2", "Page 112: a Vizag to Hyderabad ticket. 14 February 1999. Never used.", 3.6),
  ("openbook", "On the back, in appa's handwriting: \"Didn't go. Stayed for her.\"", 3.6),
  ("bedread2", "Amma sold her old books in 2001. This was her copy. She never knew the ticket was in it.", 4.0, "Some love stories wait on page 112.")],
 ("openbook", "Strangest thing you found inside an old book?", "Tell us below 👇"),
 "The bookmark was a train ticket from 1999. It was never used. 🎟️\n\n"
 "What's the strangest thing you've found inside an old book? Tell us 👇\nSend this to the one who stayed.\n\n" + APP_EN
 + "\n\n#penastory #shortstory #hyderabad #bookstagramindia #lovestory", music=0)
book(f"{D}-1800-reel-ticket-bookmark", "love-that-lasts.png", "The Secret to Love That Lasts", "Sukanya Biswas · on the Pen A Story app")

# ---- 19:30 STANDALONE as a Telugu REEL (2nd run of the 3 Dec test), reading at the core ----
reel(f"{D}-1930-reel-ammamma-english",
 [("gma3", "డెబ్భై ఏళ్ళకి అమ్మమ్మ English నేర్చుకుంది.", 2.8, "ఒక్క కథ"),
  ("auto1", "ప్రతి రోజు 4 గంటలకి auto ఎక్కి library కి వెళ్ళేది. ఎందుకో ఎవ్వరికీ చెప్పలేదు.", 3.8),
  ("crow", "పొద్దున్నే కాకులకి అన్నం పెట్టి, dictionary పట్టుకుని verandah లో కూర్చునేది.", 3.8),
  ("crow2", "ఒక రోజు ఆమె మంచం పక్కన నా first novel కనిపించింది. English లో. ప్రతి page లో pencil తో తెలుగు అర్థాలు.", 4.2),
  ("gma3", "చివరి page లో: \"అర్థమైంది రా. బాగా రాశావ్.\" 212 pages. ఒక్క ఏడాది.", 4.2)],
 ("auto1", "మీ కోసం ఇంత కష్టపడింది ఎవరు?", "Comment చేయండి 👇"),
 "డెబ్భై ఏళ్ళకి అమ్మమ్మ English నేర్చుకుంది. ఎందుకో చివరి beat లో తెలుస్తుంది. 📖\n\n"
 "మీ కోసం ఇంత కష్టపడింది ఎవరు? Comment చేయండి.\nమీ అమ్మమ్మని గుర్తు చేసే వాళ్ళకి send చేయండి.\n" + APP
 + "\n\n#penastory #telugustories #ammamma #shortstory #tenglish", music=2)

# ---- 21:30 teaser for Episode 6 (English) ----
story(f"{D}-2130-story-teaser-second-key-ep06", "clock", "The Second Key · Episode 6",
      "11:40 PM. Ananya dials Bangalore. Forty years of silence, one phone call. 🗝️", "TOMORROW", "1 PM")
print("plan 4 Dec written")
