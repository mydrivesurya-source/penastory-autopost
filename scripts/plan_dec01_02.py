"""Content plan 1 Dec 2026 (+ the 2 Dec 10:30 quiz-answer story) for @pen_a_story. Fills the gap after plan_nov29_30.py.
Virality review (21 Nov run, latest stats = 20 Nov 21:47 IST, only 5 system posts measured, all < 1 day old):
  - the reel (last-customer) reached 35 vs 7-16 for the four carousels -> reels get 2-5x the distribution;
    but its average watch was 2.2 s, so the first beat must hook inside 2 s (short first line, 2.8 s first beat).
  - account history: the big hits were Telugu and emotional/tribute (teacher tribute 26 shares, Telugu cyclist 4.5k interactions).
  - too few posts per format (<5) to cut or boost any format yet; mix stays, Telugu share stays at 50%.
Serial #2 *The Second Key* Episode 2 (English) follows the README arc: Jaffer uncle, the twelfth door plastered over in 1984
(tied to the summer Ananya's mother left, setting up Ep5). Pen name "Sitara" is NOT revealed yet (Ep3).
Chrome was not reachable, so photos are reused from the pool: nothing used on 29-30 Nov, nothing repeated across 1 Dec posts,
except tin2 (opening Ep2, as promised by the 30 Nov teaser), let3 (Ep3 teaser echoes Ep2's last frame) and jungle
(the 2 Dec quiz answer reuses the quiz cover). QC swaps: clock/bedread2 dropped (text over clock face; off-texture model).
Run: python scripts/plan_dec01_02.py  -> writes specs/*.json (new files only)"""
import json, pathlib
S = pathlib.Path(__file__).resolve().parent.parent / "specs"; S.mkdir(exist_ok=True)
def U(i): return f"https://images.unsplash.com/photo-{i}?w=1600&q=90"
P = {
 "tin2": "1763801572504-e7fd828d7bf5", "twin2": "1599557832120-a73f36b8f37a", "clock": "1774904721886-7b3abd03be14",
 "let3": "1528458965990-428de4b1cb0d", "lib2": "1481627834876-b7833e8f5570", "lib": "1507842217343-583bb7270b66",
 "jungle": "1694614360428-608d018bb054", "fall": "1754903272366-f92a6b23f18e", "hillroad": "1619260584294-8a4e63f5ade5",
 "stream": "1685293080597-5d3526faf88e", "bench2": "1750513538756-46e040ad48b7", "cofbk2": "1474366521946-c3d4b507abf2",
 "teabk": "1763908161557-dffe1780dda5", "twin1": "1726747062988-cd0b86c814e0", "tin1": "1779635279571-988a2e63b549",
 "chai3": "1787399087896-fff638c01a2b", "st3": "1764705448662-f74992067ff7", "bench": "1771308134963-9ffb3abb2471",
 "bedread2": "1528436610461-e9be9d1f7d6b", "torch": "1560259344-7b4ca2f09ef9", "crk1": "1706102005390-2d1f41fdddcd", "monk2": "1505221594957-3931cba3a090",
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

D = "2026-12-01"

# ---- 10:30 story (Telugu): reader mood + quiz tease ----
story(f"{D}-1030-story-am", "torch", "Blanket + torch + కథ.\n\"అమ్మ వస్తోంది!\" 🔦",
      "Story Quiz #2 ఈ రోజు 4:30 PM 🔍", "90s KIDS")

# ---- 13:00 SERIAL: The Second Key, Episode 2 (English) ----
SER = "THE SECOND KEY · SERIAL"
carousel(f"{D}-1300-serial-second-key-ep02", SER,
 [("tin2", "Next morning, the old man from next door was waiting on her steps. \"You have Rukmini's eyes.\"", "Episode 2"),
  ("twin2", "Jaffer uncle. Fifty-one years next door. He made chai the way ammamma did: half glass, extra ginger."),
  ("chai3", "Ananya showed him the brass key. His glass stopped halfway. \"I haven't seen that since 1984.\""),
  ("lib2", "\"Your ammamma's house never had eleven doors, beta. It had twelve.\""),
  ("let3", "\"The summer your mother left for Bangalore, she had a mason plaster one over. Upstairs. She never climbed those stairs again.\"")],
 ("let3", "Would you break the wall?", "Episode 3 · tomorrow 1 PM"),
 "Eleven doors. One key that fits none. And a neighbour who remembers a twelfth. 🗝️\n\nThe Second Key · Episode 2. Missed Episode 1? It's one post back.\n\n"
 "Would you break the wall, or leave it alone? Tell us 👇\n" + APP_EN + "\n\n#penastory #thesecondkey #serialstory #shortstory #hyderabad")

# ---- 16:30 rotation: Story Quiz #2 (Telugu), answer 2 Dec 10:30 ----
carousel(f"{D}-1630-quiz-guess-story-2", "STORY QUIZ · కథ కనుక్కోండి",
 [("jungle", "3 clues. ఒక్క కథ. Guess చేయగలరా?", "Story Quiz #2"),
  ("fall", "Clue 1: ఒక అడవి. ఒక గర్వం ఉన్న రాజు. రోజుకో జంతువు అతని దగ్గరికి వెళ్ళాలి."),
  ("hillroad", "Clue 2: ఒక రోజు ఒక చిన్న జంతువు కావాలనే ఆలస్యంగా వెళ్ళింది."),
  ("stream", "Clue 3: \"ప్రభూ, ఆ బావిలో మీకంటే పెద్ద రాజు ఉన్నాడు.\"")],
 ("jungle", "ఏ కథ? Comment చేయండి", "Answer రేపు story లో"),
 "3 clues. ఒక్క కథ. 🔍\n\nగర్వం ఉన్న రాజు. ఆలస్యంగా వచ్చిన చిన్న జంతువు. ఒక బావి.\n\nఏ కథో comment చేయండి — answer రేపు 10:30 story లో. Panchatantra fans కి easy 😉\n"
 + APP + "\n\n#penastory #storyquiz #panchatantra #telugukathalu #childhoodmemories")

# ---- 18:00 REEL (English): hook inside 2 s (review: 2.2 s avg watch on 20 Nov) ----
reel(f"{D}-1800-reel-library-fine",
 [("lib", "31 years late.\nFine: Rs 4,380.", 2.8, "A story"),
  ("bench2", "1995. The night before his train to Delhi, he borrowed one book. He never returned it.", 3.8),
  ("crk1", "That book got him through hostel, two failed exams and his first job.", 3.4),
  ("lib", "Today he came back to pay. The librarian, now 74, didn't take his money.", 3.6),
  ("teabk", "She stamped the book RETURNED, and slid a new card across. \"Next one's due in two weeks.\"", 3.8, "Some teachers don't stand in classrooms.")],
 ("teabk", "Which book would you never give back?", "Tell us below 👇"),
 "31 years late. Rs 4,380 in fines. And a librarian who wouldn't take a rupee. 📚\n\nWhich book would you never give back? Tell us 👇\n\n" + APP_EN
 + "\n\n#penastory #shortstory #booklovers #librarylove #readersofinstagram", music=2)
book(f"{D}-1800-reel-library-fine", "unseen-curriculum.jpg", "The Unseen Curriculum", "Vibhuti Vaid · what great teachers teach without a syllabus")

# ---- 19:30 STANDALONE (Telugu), twist ending ----
carousel(f"{D}-1930-story-last-chapter", "PEN A STORY · ఒక్క కథ",
 [("twin1", "Godavari Express. రాత్రి 11. S4 coach లో అందరూ నిద్రపోతున్నారు — నేను, ఎదురు seat లో ఒక తాతగారు తప్ప.", "ఒక్క కథ · చివరి chapter"),
  ("tin1", "నా చేతిలో ఒక పాత Telugu novel. ఆయన చాలాసేపు దాన్నే చూస్తున్నారు."),
  ("twin1", "Rajahmundry దగ్గర chai తాగుతూ అడిగారు: \"అమ్మా, కళ్ళద్దాలు మర్చిపోయాను. చివరి chapter గట్టిగా చదువుతావా?\""),
  ("st3", "చదివాను. చివరి page కి వచ్చేసరికి ఆయన కళ్ళలో నీళ్ళు. Samalkot లో దిగిపోయారు, ఒక్క మాట కూడా లేకుండా."),
  ("bench", "ఆయన seat మీద ఒక చిన్న కాగితం: \"ఎవరైనా నా కథ చదువుతుంటే వినడం — 40 ఏళ్ళలో ఇదే మొదటిసారి.\""),
  ("cofbk2", "ఇంటికి వచ్చి back cover తిప్పాను. Author photo. అదే ముఖం — 40 ఏళ్ళు చిన్నది.")],
 ("tin1", "మీ favourite రచయిత ఎదురుగా కూర్చుంటే, ఏం చెప్తారు?", "Comment చేయండి 📖"),
 "రాత్రి train. ఒక తాతగారు. \"చివరి chapter గట్టిగా చదువుతావా?\" 🚆\n\nఒక్క post లో పూర్తి కథ — చివరి slide వరకు swipe చేయండి.\n\n"
 "మీ favourite రచయిత ఎదురుగా కూర్చుంటే, ఏం చెప్తారు? Comment చేయండి.\n\nTrain లో కథలు ఇష్టపడే friend కి send చేయండి.\n" + APP
 + "\n\n#penastory #telugustories #shortstory #tenglish #trainstories")

# ---- 21:30 teaser for Episode 3 (English) ----
story(f"{D}-2130-story-teaser-second-key-ep03", "let3", "The Second Key · Episode 3",
      "Behind the plaster: a room nobody has opened since 1984. Tomorrow, 1 PM 🔨", "TOMORROW", "1 PM")

# ---- 2 Dec 10:30: quiz answer (Telugu); the rest of 2 Dec is written by the next run ----
story("2026-12-02-1030-story-am", "jungle", "Quiz answer: సింహం – కుందేలు 🦁🐇",
      "బావిలో కనిపించింది సింహం నీడే. చిన్న కుందేలు, పెద్ద బుద్ధి. ఎంతమంది correct చెప్పారు? 👏", "ANSWER")
print("plan 1-2 Dec written")
