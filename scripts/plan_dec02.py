"""Content plan 2 Dec 2026 (13:00-21:30; 10:30 was written by plan_dec01_02.py) for @pen_a_story.
Virality review (22 Nov run; latest stats = 21 Nov 21:49 IST, the 22 Nov nightly run had not happened yet). 9 system posts measured:
  - every post: 0 shares, 0 saves, 0 comments. Reach: reels 45-85, carousels 6-28. Reels keep the 2-5x distribution edge.
  - top: serial ep1 (3.0), reel last-customer (3.0), library-card standalone (2.5). Bottom: tiffin-note standalone (1.1),
    thirsty-crow nostalgia (1.3), reel window-seat (1.6, but its avg watch rose to 3.5 s from 2.3 s).
  - Telugu carousels median 2.15 vs English 1.8; no format has 5+ posts yet, so nothing is cut or boosted.
Decisions applied here: (1) zero shares -> every caption carries one concrete "send this to <specific person>" line;
(2) reels: <=8-word hook in a 2.8 s first beat AND a twist in the last beat, so the payoff makes people re-watch/share;
(3) mix and 50/50 language split unchanged (3 Telugu: 10:30, 16:30, 19:30; 3 English: 13:00, 18:00, 21:30).
Serial #2 The Second Key Ep3 follows the README arc (the twelfth room, rejection letters to "Sitara"); the trunk is only teased (Ep4).
QC swaps: clock (text over the clock face), let2/let4 as text slides (cream text on handwriting; let4 kept only for the big end line), st4 (a Japanese station), bedread2 (off-texture model).
Chrome was not reachable, so photos are reused from the pool: nothing used on 30 Nov-1 Dec (last use 28-29 Nov), none repeated across posts on 2 Dec
(within a carousel a photo may return as a deliberate echo).
Run: python scripts/plan_dec02.py  -> writes specs/*.json (new files only)"""
import json, pathlib
S = pathlib.Path(__file__).resolve().parent.parent / "specs"; S.mkdir(exist_ok=True)
def U(i): return f"https://images.unsplash.com/photo-{i}?w=1600&q=90"
P = {
 "rain1": "1470432581262-e7880e8fe79a", "door2": "1583008520412-7ee838891ada", "watch": "1509048191080-d2984bad6ae5", "cofbk": "1544716278-ca5e3f4abd8c",
 "let1": "1779729739456-be9369745290", "let2": "1780536890742-a3d937535d66", "let4": "1561812938-f6e60cbf95e3",
 "moon": "1522030299830-16b8d3d049fe", "moon2": "1532767153582-b1a0e5145009", "monk": "1751963442555-38e8d2ddcddd", "monk2": "1505221594957-3931cba3a090",
 "st1": "1763688653741-bcc54bea7c26", "st2": "1743947830042-52acbb973f2d", "st4": "1653494656006-869fdf081d42", "rain2": "1511634829096-045a111727eb",
 "oldph": "1783534784717-0843229c4f89", "bwph": "1649339035455-1b0ab8a37d49",
 "gma1": "1533128361669-69c065857a13", "kitch2": "1596450513856-250e5f5c46cc", "bedread2": "1528436610461-e9be9d1f7d6b",
 "hills": "1567960699877-b134ad1caef8", "diya2": "1605292356183-a77d0a9c9d1d", "bdoor": "1524228529766-4d7fe5dc55ca",
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

D = "2026-12-02"

# ---- 13:00 SERIAL: The Second Key, Episode 3 (English) ----
SER = "THE SECOND KEY · SERIAL"
carousel(f"{D}-1300-serial-second-key-ep03", SER,
 [("rain1", "Midnight. Rain on the window. Ananya stood upstairs with Jaffer uncle's old hammer.", "Episode 3"),
  ("door2", "Third swing, the plaster cracked. Behind it, a narrow wooden door. Nobody had touched it since 1984."),
  ("door2", "She tried the brass key. It didn't fit. The door wasn't even locked."),
  ("let1", "Inside: one desk, one chair, and dozens of letters. Every one began: \"Dear Madam, we regret to inform you…\" Twelve years of rejections.")],
 ("let4", "All addressed to a writer called \"Sitara.\" Who was she?", "Episode 4 · tomorrow 1 PM"),
 "Behind the plaster: a door. Behind the door: twelve years of rejection letters. 🗝️\n\nThe Second Key · Episode 3. New here? Episodes 1 and 2 are just before this post.\n\n"
 "Who do you think Sitara was? Guess in the comments 👇\nSend this to the friend who's been following the serial with you.\n" + APP_EN
 + "\n\n#penastory #thesecondkey #serialstory #shortstory #hyderabad")

# ---- 16:30 rotation: nostalgia (Telugu), the monkeys who tried to save the moon ----
carousel(f"{D}-1630-nostalgia-moon-in-well", "మనం చిన్నప్పుడు విన్న కథ",
 [("moon", "\"చందమామ బావిలో పడిపోయింది!\"", "కోతులు – చందమామ"),
  ("monk2", "ఒక రాత్రి ఒక చిన్న కోతి నీళ్ళు తాగడానికి బావి దగ్గరికి వెళ్ళింది. లోపల చూసి గట్టిగా అరిచింది."),
  ("moon2", "\"చందమామ నీళ్ళలో పడిపోయింది! ఇక రాత్రులన్నీ చీకటే!\" అడవి అంతా పరుగెత్తుకొచ్చింది."),
  ("monk", "పెద్ద కోతి plan వేసింది: ఒకరి తోక ఇంకొకరు పట్టుకుని, chain లా బావిలోకి దిగుదాం."),
  ("moon2", "చివరి కోతి నీళ్ళు తాకగానే చందమామ ముక్కలైపోయింది. బరువుకి కొమ్మ విరిగింది. అందరూ బావిలో! 💦"),
  ("monk2", "తడిసిన కోతులు పైకి చూశాయి. చందమామ ఆకాశంలో నవ్వుతోంది. Moral: చూసింది నమ్మే ముందు ఒక్కసారి ఆలోచించు.")],
 ("moon", "ఈ కథ మీకు ఎవరు చెప్పారు?", "Comment చేయండి 🌕"),
 "చందమామ బావిలో పడిపోయింది! 🌕🐒\n\nఈ కథ విని నవ్వని 90s kid ఉన్నారా? చివరి slide వరకు swipe చేయండి.\n\n"
 "ఈ కథ మీకు మొదట ఎవరు చెప్పారు — అమ్మమ్మ, తాతయ్య, Chandamama book? Comment చేయండి.\nమీ childhood friend కి send చేయండి 😄\n" + APP
 + "\n\n#penastory #telugukathalu #childhoodmemories #90skids #moralstories")

# ---- 18:00 REEL (English): hook under 8 words in a 2.8 s first beat; twist in the last beat ----
reel(f"{D}-1800-reel-two-minute-delay",
 [("st1", "The night the train refused to leave.", 2.8, "A story"),
  ("watch", "Ramaiah. Station master at a small junction for 38 years. He knew every regular by their chai order.", 3.8),
  ("st2", "His last shift. The 11:40 passenger pulled in. Two-minute halt, as always.", 3.4),
  ("rain2", "But it didn't move. In every window, a face. In every hand, a paper cup of chai, raised to him.", 3.8),
  ("oldph", "Next day the guard's log read: \"Delay: 2 min. Reason: thank you.\"", 3.8, "Ramaiah framed that page.")],
 ("bwph", "Which stranger from your daily route would you miss?", "Tell us below 👇"),
 "38 years. One small station. And a train that wouldn't leave without saying thank you. 🚆\n\n"
 "Which stranger from your daily route would you miss the most? Tell us 👇\nSend this to someone who takes the same train every day.\n\n" + APP_EN
 + "\n\n#penastory #shortstory #indianrailways #trainstories #readersofinstagram", music=3)
book(f"{D}-1800-reel-two-minute-delay", "2min-stories.jpg", "2Min Stories", "Surya Teja · small stories about ordinary people")

# ---- 19:30 STANDALONE (Telugu), twist ending ----
carousel(f"{D}-1930-story-wrong-number", "PEN A STORY · ఒక్క కథ",
 [("gma1", "ప్రతి ఆదివారం రాత్రి 7 గంటలకి అమ్మమ్మ phone మోగేది. \"అమ్మా, తిన్నావా?\"", "ఒక్క కథ · Wrong Number"),
  ("kitch2", "Bangalore నుంచి ఒక అబ్బాయి. Wrong number. మొదటి call లోనే అమ్మమ్మకి అర్థమైంది. కానీ ఎప్పుడూ correct చేయలేదు."),
  ("cofbk", "నేను అడిగాను: \"తెలియని వాడితో గంటసేపు ఏం మాట్లాడతావు అమ్మమ్మా?\""),
  ("hills", "\"వాడి గొంతులో ఆకలి ఉంది రా. అన్నం ఆకలి కాదు. మాట్లాడే మనిషి ఆకలి.\""),
  ("diya2", "ఒక సంవత్సరం తర్వాత అమ్మమ్మ వెళ్ళిపోయింది. ఆ ఆదివారం 7 గంటలకి phone మోగింది. నేను ఎత్తాను."),
  ("gma1", "విషయం చెప్పాను. చాలాసేపు silence. తర్వాత: \"Wrong number అని నాకు మొదటి రోజే తెలుసు. మా అమ్మ పోయిన రెండో వారం అది.\"")],
 ("hills", "మీ జీవితంలో అలాంటి \"wrong number\" ఎవరైనా ఉన్నారా?", "Comment చేయండి 📞"),
 "ప్రతి ఆదివారం 7 గంటలకి ఒక wrong number. అమ్మమ్మ ఎప్పుడూ correct చేయలేదు. 📞\n\nఒక్క post లో పూర్తి కథ — చివరి slide వరకు swipe చేయండి.\n\n"
 "మీ జీవితంలో అలాంటి \"wrong number\" ఎవరైనా ఉన్నారా? Comment చేయండి.\nమీ అమ్మమ్మని గుర్తు చేసే వాళ్ళకి send చేయండి.\n" + APP
 + "\n\n#penastory #telugustories #shortstory #ammamma #tenglish")

# ---- 21:30 teaser for Episode 4 (English) ----
story(f"{D}-2130-story-teaser-second-key-ep04", "bdoor", "The Second Key · Episode 4",
      "Under Sitara's desk: a trunk with a brass lock. Tomorrow, the key finally fits. 🗝️", "TOMORROW", "1 PM")
print("plan 2 Dec written")
