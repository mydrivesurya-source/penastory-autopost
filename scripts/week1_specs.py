import json, pathlib
S = pathlib.Path("/home/claude/penastory-autopost/specs")
C = {
 "cyclist": "https://penastory.com/wp-content/uploads/2025/07/indian-cyclist.jpg",
 "ramayana": "https://penastory.com/wp-content/plugins/penastory-ramayana/assets/cover-front.jpg",
 "winter": "https://penastory.com/wp-content/uploads/2017/08/Screenshot-2024-12-03-151323.png",
 "heroes": "https://penastory.com/wp-content/uploads/2026/02/unforgotten-book.jpeg",
 "twomin": "https://penastory.com/wp-content/uploads/2017/08/2minReadbookcover-1-683x1024.jpg",
 "boots": "https://penastory.com/wp-content/uploads/2017/08/Where-are-my-boots-.png",
}
APP_EN = "📲 Free Pen A Story app: link in bio (Android + iPhone)"
APP_TE = "📲 Pen A Story యాప్ ఉచితం: లింక్ బయోలో ఉంది (Android + iPhone)"

def put(name, d):
    (S / f"{name}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1))

def six(date, slug, ep, lang, hook, frames, book, title, line, ask, tags):
    slides = [{"kind": "hook", "title": hook, "lines": [ "6 frames. 60 seconds." if lang == "en" else "6 ఫ్రేములు. ఒక్క నిమిషం."]}]
    slides += [{"kind": "frame" if i < 5 else "twist", "n": i + 1, "title": f[0], "lines": [f[1]] if len(f) > 1 else []} for i, f in enumerate(frames)]
    slides += [({"kind": "book", "image": 0, "title": title, "lines": [line]} if book else {"kind": "text", "title": title, "lines": [line]}),
               {"kind": "cta", "title": ask, "lines": ["Comment below 👇" if lang == "en" else "కామెంట్‌లో చెప్పండి 👇"]}]
    cap = (f"{hook}\n\n" + ("A complete story in 6 frames. Swipe to the end.\n\n" if lang == "en" else "6 ఫ్రేముల్లో ఒక పూర్తి కథ. చివరి వరకు స్వైప్ చేయండి.\n\n")
           + f"{ask}\n\n" + ((f"If this one stayed with you, {title} will too. " if lang == "en" else f"ఈ కథ నచ్చితే, {title} కూడా నచ్చుతుంది. ") if book else ("A new Six Frames story every day at 1 PM. " if lang == "en" else "ప్రతి రోజు మధ్యాహ్నం 1 గంటకు కొత్త కథ. "))
           + "\n" + (APP_EN if lang == "en" else APP_TE) + "\n\n" + " ".join(tags[:5]))
    put(f"{date}-1300-sixframes-{slug}", {"kind": "carousel", "ep": ep - 1, "series": f"Six Frames · Ep {ep:02d}", "images": [C[book]] if book else [], "slides": slides, "caption": cap})

def reel(date, slug, beats, book, title, end_line, cta, cap, music=0):
    d = {"kind": "reel", "beats": beats, "title": title, "end_line": end_line, "cta": cta, "caption": cap, "music": music}
    d["images"] = [C[book]] if book else []
    put(f"{date}-1930-reel-{slug}", d)
    put(f"{date}-2130-story-reshare-{slug}", {"kind": "story", "video": f"media/{date}-1930-reel-{slug}.mp4"})

def am(date, slug, kicker, title, text, cta, book):
    put(f"{date}-1030-story-{slug}", {"kind": "story", "kicker": kicker, "title": title, "text": text, "cta": cta, "images": [C[book]] if book else []})

# ---------- Fri 21 Nov ----------
am("2026-11-21", "cyclist-te", "ఈ రోజు రాత్రి 7:30కి", "28 దేశాలు. ఒక సైకిల్.", "ఒక తెలుగు వ్యక్తి ప్రయాణం, ఇప్పుడు మన భాషలో.", "రీల్ కోసం చూడండి", "cyclist")
six("2026-11-21", "last-customer", 1, "en", "The bookshop was closing for good. One customer refused to leave.",
    [("Mr. Rao had run the shop for 41 years. Tonight was the last night.",),
     ("At 9 PM, a girl in a school uniform was still sitting in the corner, reading.",),
     ("\"We're closing, beta.\" She didn't look up. \"Can I finish this chapter?\"",),
     ("He waited. One chapter became three. He made two cups of tea.",),
     ("At midnight she closed the book and asked, \"Who decides the ending of a shop?\"",),
     ("Mr. Rao looked at the empty shelves. Then he took the closing sign off the door.", "Some stories refuse to end.")],
    None, "A new story every day.", "Six Frames, 1 PM daily. More stories in the free Pen A Story app.",
    "Should Mr. Rao have kept the shop open?", ["#penastory", "#shortstory", "#bookstagramindia", "#readersofinstagram", "#microfiction"])
reel("2026-11-21", "cyclist-28-countries",
     [{"text": "28 దేశాలు.", "dur": 1.6, "style": "big"}, {"text": "ఒక సైకిల్.", "dur": 1.5, "style": "big"},
      {"text": "ఆకాశమే పైకప్పుగా గడిపిన రాత్రులు.", "dur": 2.6}, {"text": "అపరిచితులే ఆత్మీయులైన క్షణాలు.", "dur": 2.6, "gold": True},
      {"text": "మీరు అడిగారు: \"తెలుగులో కావాలి.\"", "dur": 2.4, "style": "small"}],
     "cyclist", "ది ఇండియన్ సైక్లిస్ట్", "ఇప్పుడు తెలుగులో — Pen A Story యాప్‌లో", "యాప్ లింక్ బయోలో",
     "28 దేశాలు. ఒక సైకిల్. ఒక భారతీయుడి నిజమైన ప్రయాణం. 🚴‍♂️\n\nఆకాశమే పైకప్పుగా గడిపిన రాత్రులు, అపరిచితులే ఆత్మీయులైన క్షణాలు — అన్నీ ఒకే పుస్తకంలో, ఇప్పుడు మన తెలుగులో.\n\nమీరు సైకిల్‌పై వెళ్ళాలనుకునే ఒక దేశం ఏది? కామెంట్ చేయండి 👇\n\n"
     + APP_TE + "\n\n#penastory #theindiancyclist #telugubooks #cycling #telugureels", music=1)

# ---------- Sat 22 Nov ----------
am("2026-11-22", "twomin", "For parents", "Bedtime in 2 minutes, not 20.", "Short stories for ages 3–8. Read one tonight.", "Free on the app", "twomin")
six("2026-11-22", "amma-dabba", 2, "te", "అమ్మ టిఫిన్ డబ్బాలో ఒక చిన్న కాగితం ఉండేది.",
    [("ప్రతి రోజు స్కూల్‌లో డబ్బా తెరిస్తే, అన్నం పైన ఒక చిన్న చీటీ.",), ("\"నీళ్ళు తాగు.\" \"భయపడకు.\" \"నువ్వు చేయగలవు.\"",),
     ("పదో తరగతిలో నేను చీటీలు చదవకుండానే పారేసేవాడిని.",), ("ఇప్పుడు నాకు ముప్పై ఐదు. అమ్మ దూరంగా ఉంది.",),
     ("నిన్న నా కూతురి డబ్బాలో అన్నం పెడుతూ ఆగిపోయాను.",), ("ఒక కాగితం తీసి రాశాను: \"భయపడకు.\"", "కొన్ని అలవాట్లు ప్రేమ రూపంలో తిరిగి వస్తాయి.")],
    "twomin", "2 Minute Stories", "పిల్లలకు నిద్రకు ముందు చదివే చిన్న కథలు — ఒక్కొక్కటి 2 నిమిషాలు.",
    "మీ అమ్మ మీకు చెప్పిన ఒక మాట ఏది?", ["#penastory", "#telugustories", "#amma", "#telugu", "#shortstory"])
reel("2026-11-22", "ramayana-why",
     [{"text": "Your child can name 20 YouTubers.", "dur": 2.2}, {"text": "Can they tell you why Ram chose the forest over a throne?", "dur": 3.0},
      {"text": "Every story they hear becomes the person they grow into.", "dur": 2.8, "style": "small"},
      {"text": "Give them one worth growing into.", "dur": 2.2, "gold": True}],
     "ramayana", "Ramayana", "A Story of Courage, Love & Dharma — illustrated, for young readers", "App link in bio",
     "Your child can name 20 YouTubers. Can they tell you why Ram chose the forest over a throne?\n\nThe stories kids hear early become the values they carry. Ramayana on Pen A Story is illustrated, simple and written for young readers, so you can read it together at bedtime.\n\nWhich Ramayana character did you love most as a kid? 👇\n\n"
     + APP_EN + "\n\n#penastory #ramayana #kidsbooks #parentingindia #bedtimestories")

# ---------- Sun 23 Nov ----------
am("2026-11-23", "oneline", "New game · 1 PM today", "We write line one. You write line two.", "The best lines get featured in our Story.", "Play at 1 PM", None)
put("2026-11-23-1300-oneline-ep01", {"kind": "carousel", "ep": 3, "series": "One Line. Your Turn. · Ep 01", "images": [], "slides": [
    {"kind": "hook", "title": "The letter arrived on a Tuesday. It was postmarked next year.", "lines": ["Line one is ours. Line two is yours."]},
    {"kind": "text", "title": "How to play", "lines": ["1. Write the next line of the story in the comments.", "2. One or two sentences. Any language.", "3. Like the lines you'd want to read next."]},
    {"kind": "cta", "title": "The top lines get featured in our Story on Friday.", "lines": ["Your words. Your name. On Pen A Story."]}],
    "caption": "The letter arrived on a Tuesday. It was postmarked next year. ✉️\n\nLine one is ours. Line two is yours: write what happens next in the comments (English, Telugu, Hindi, any language).\n\nThe most-liked lines get featured in our Story on Friday, with your name on them.\n\n#penastory #onelineyourturn #writingprompt #storytelling #writersofinstagram"})
reel("2026-11-23", "hanuman-fear",
     [{"text": "భయం గట్టిగా మాట్లాడే రాత్రులు ఉంటాయి.", "dur": 2.6}, {"text": "అప్పుడు ఒక పేరు గుర్తొస్తుంది.", "dur": 2.2},
      {"text": "జై హనుమాన్.", "dur": 1.8, "style": "big", "gold": True},
      {"text": "40 శ్లోకాలు. 40 జీవిత పాఠాలు.", "dur": 2.6}, {"text": "ఇది ప్రార్థన మాత్రమే కాదు. జీవించే విధానం.", "dur": 2.8, "style": "small"}],
     None, "Hanuman Chalisa — Life Lessons", "త్వరలో Pen A Story యాప్‌లో", "Follow for the launch",
     "భయం గట్టిగా మాట్లాడే రాత్రులు ఉంటాయి. అప్పుడు ఒక పేరు గుర్తొస్తుంది. 🔥 జై హనుమాన్.\n\n40 శ్లోకాలు, 40 జీవిత పాఠాలు — ధైర్యం, సేవ, భక్తి. \"Hanuman Chalisa — Life Lessons\" త్వరలో Pen A Story యాప్‌లో.\n\nమీకు బలం ఇచ్చే చౌపాయి ఏది? కామెంట్ చేయండి 👇\n\n#penastory #hanumanchalisa #jaihanuman #telugu #spirituality", music=1)

# ---------- Mon 24 Nov ----------
am("2026-11-24", "winter", "Mystery night", "Could you solve a case in 10 seconds?", "Tonight's reel will test you.", "7:30 PM", None)
six("2026-11-24", "cycle-bell", 3, "te", "నాన్న సైకిల్ బెల్ వినిపిస్తే, ఇల్లంతా పరుగెత్తేది.",
    [("ప్రతి సాయంత్రం ఆరు గంటలకు ఒకే శబ్దం: ట్రింగ్ ట్రింగ్.",), ("ఆ బెల్ అంటే జిలేబీ పొట్లం. లేదా కొత్త పెన్సిల్.",),
     ("నేను పెద్దయ్యాక నాన్నకు బైక్ కొనిచ్చాను.",), ("సైకిల్ మూలన పడింది. బెల్ తుప్పు పట్టింది.",),
     ("నిన్న నా కొడుకు అడిగాడు: \"నాన్నా, ఈ బెల్ ఎలా మోగుతుంది?\"",), ("నేను మోగించాను. వంటింట్లోంచి అమ్మ పరుగెత్తుకొచ్చింది.", "కొన్ని శబ్దాలు ఎప్పటికీ పాతబడవు.")],
    "cyclist", "ది ఇండియన్ సైక్లిస్ట్", "ఒక సైకిల్, 28 దేశాలు — ఇప్పుడు తెలుగులో.",
    "మీ చిన్ననాటి ఏ శబ్దం ఇంకా గుర్తుంది?", ["#penastory", "#telugustories", "#nanna", "#childhoodmemories", "#telugu"])
reel("2026-11-24", "winter-solve",
     [{"text": "Solve this in 10 seconds.", "dur": 2.0, "style": "big"},
      {"text": "The power went out at 11 PM. The whole street went dark.", "dur": 3.0},
      {"text": "At 2 AM, the safe was empty.", "dur": 2.2},
      {"text": "The guard says: \"I was reading by the window all night. I saw no one.\"", "dur": 3.2},
      {"text": "Who's lying?", "dur": 1.8, "style": "big", "gold": True},
      {"text": "Answer in the comments. Mysteries like this live in one book.", "dur": 2.6, "style": "small"}],
     None, "Solve the Case", "A new mystery every Tuesday", "Follow @pen_a_story",
     "Solve this in 10 seconds 🕯️\n\nThe power went out at 11 PM. At 2 AM, the safe was empty. The guard says he was reading by the window all night and saw no one.\n\nWho's lying, and how do you know? Drop your answer 👇 (we'll pin the first correct one)\n\nNew case every Tuesday. Follow so you don't miss it.\n\n#penastory #mystery #solvethecase #thriller #bookstagramindia")

# ---------- Tue 25 Nov ----------
am("2026-11-25", "answer", "Last night's mystery", "The guard was lying.", "He was \"reading by the window\" in a total blackout. You can't read in the dark.", "New case at 1 PM", None)
put("2026-11-25-1300-case-01", {"kind": "carousel", "ep": 4, "series": "Solve the Case · #01", "images": [], "slides": [
    {"kind": "hook", "title": "Three suspects. One stolen ring. Only one detail gives the thief away.", "lines": ["Read every slide carefully."]},
    {"kind": "frame", "n": 1, "title": "Meera, the cook: \"I was in the kitchen. The milk boiled over at 8:15, I was cleaning it.\""},
    {"kind": "frame", "n": 2, "title": "Arjun, the driver: \"I was washing the car. It was so sunny, I finished by 8.\""},
    {"kind": "frame", "n": 3, "title": "Sita, the neighbour: \"I came at 9 for sugar. The ring was already missing.\""},
    {"kind": "frame", "n": 4, "title": "The ring vanished between 8 and 8:30 PM.", "lines": ["One statement can't be true."]},
    {"kind": "cta", "title": "Who did it? Comment the name.", "lines": ["Answer revealed in tomorrow's Story."]}],
    "caption": "Three suspects. One stolen ring. One detail gives the thief away. 🔍\n\nSwipe through every statement, then comment the name of the thief. Answer in tomorrow's Story.\n\nSave this to test a friend 🔖\n\n" + APP_EN + "\n\n#penastory #solvethecase #mystery #puzzle #detective"})
reel("2026-11-25", "ramayana-te",
     [{"text": "ఒక రాజ్యం ఇవ్వబోతున్నారు.", "dur": 2.2}, {"text": "కానీ ఆయన ఒక మాట కోసం అడవికి వెళ్ళాడు.", "dur": 2.8},
      {"text": "పధ్నాలుగు సంవత్సరాలు.", "dur": 2.0, "style": "big", "gold": True},
      {"text": "మన పిల్లలకు ఈ కథ ఎవరు చెబుతారు?", "dur": 2.6}, {"text": "మనమే.", "dur": 1.6, "style": "big"}],
     "ramayana", "రామాయణం", "పిల్లల కోసం బొమ్మలతో — Pen A Story యాప్‌లో", "యాప్ లింక్ బయోలో",
     "ఒక రాజ్యం ఇవ్వబోతున్నారు. కానీ ఆయన ఒక మాట కోసం అడవికి వెళ్ళాడు. 🏹\n\nమన పిల్లలకు ఈ కథ ఎవరు చెబుతారు? మనమే. బొమ్మలతో, సులభమైన భాషలో రామాయణం — రాత్రి నిద్రకు ముందు కలిసి చదవండి.\n\nచిన్నప్పుడు మీకు రామాయణం ఎవరు చెప్పారు? 👇\n\n" + APP_TE + "\n\n#penastory #ramayanam #telugu #kidsbooks #teluguparents", music=1)

# ---------- Wed 26 Nov ----------
am("2026-11-26", "case-answer", "Solve the Case #01", "Arjun did it.", "He said it was \"so sunny\" while washing the car at 8 PM. The sun had set by 6.", "New case next week", None)
six("2026-11-26", "grandfathers-watch", 4, "en", "My grandfather's watch stopped at 4:17. He never let anyone fix it.",
    [("For 50 years it sat on his wrist. Always 4:17.",), ("Strangers would tell him: \"Sir, your watch is wrong.\" He'd smile: \"No. It's right.\"",),
     ("When he passed, we found an old letter in his drawer.",), ("1971. A railway station. A bomb. He had pulled 12 people off a burning coach.",),
     ("The letter was from one of them. \"You saved us at 4:17. We will never forget.\"",), ("He never told anyone. He just kept the time.", "Some heroes don't want medals. Only memory.")],
    "heroes", "The Unforgotten Heroes", "Stories of ordinary people who showed extraordinary courage.",
    "Is there a quiet hero in your family?", ["#penastory", "#shortstory", "#unsungheroes", "#bookstagramindia", "#microfiction"])
reel("2026-11-26", "bedtime-2min",
     [{"text": "\"One more story, please.\"", "dur": 2.0, "style": "big"},
      {"text": "It's 9:47 PM. You have zero energy left.", "dur": 2.4},
      {"text": "Here's a secret: it doesn't have to be a long one.", "dur": 2.6},
      {"text": "2 minutes. A real story. A happy kid.", "dur": 2.4, "gold": True}],
     "twomin", "2 Minute Stories", "Quick bedtime reads for ages 3–8", "App link in bio",
     "\"One more story, please.\" 🌙 It's 9:47 PM and you have nothing left.\n\nIt doesn't have to be long. 2 Minute Stories is a collection of short, warm stories for ages 3–8, made for exactly this moment.\n\nTag a parent who hears \"one more story\" every night 👇\n\n" + APP_EN + "\n\n#penastory #bedtimestories #parentingindia #kidsbooks #momlife")

# ---------- Thu 27 Nov ----------
am("2026-11-27", "boots", "Kids' pick", "Where are my boots?", "A funny story about Kutti, his family, his dog and one lost pair of boots.", "Read tonight", "boots")
six("2026-11-27", "hanuman-exam", 5, "te", "పరీక్ష ముందు రాత్రి, నాకు ఏమీ గుర్తు రాలేదు.",
    [("ఇంటర్ ఫైనల్స్. మ్యాథ్స్ పేపర్. రాత్రి ఒంటి గంట.",), ("పుస్తకం తెరిచాను. అక్షరాలు అన్నీ ఒకేలా కనిపించాయి.",),
     ("తాతయ్య గదిలోంచి నెమ్మదిగా హనుమాన్ చాలీసా వినిపించింది.",), ("\"భూత పిశాచ నికట నహి ఆవై…\" ఆయన గొంతు స్థిరంగా ఉంది.",),
     ("నేను కళ్ళు మూసుకుని ఆయనతో పాటు అన్నాను. గుండె నెమ్మదించింది.",), ("ఆ రాత్రి నేర్చుకున్నది లెక్కలు కాదు. భయాన్ని ఎదుర్కోవడం.", "ధైర్యం కూడా నేర్చుకునే విద్యే.")],
    None, "Hanuman Chalisa — Life Lessons", "40 శ్లోకాలు, 40 జీవిత పాఠాలు — త్వరలో యాప్‌లో.",
    "మీకు భయం వేసినప్పుడు ఏం చేస్తారు?", ["#penastory", "#hanumanchalisa", "#telugustories", "#telugu", "#jaihanuman"])
reel("2026-11-27", "cyclist-strangers",
     [{"text": "తెలియని దేశం. తెలియని భాష.", "dur": 2.4}, {"text": "రాత్రి ఎక్కడ పడుకోవాలో తెలియదు.", "dur": 2.4},
      {"text": "అప్పుడు ఒక అపరిచితుడు తలుపు తెరిచాడు.", "dur": 2.6, "gold": True},
      {"text": "ప్రపంచం మనం అనుకున్నంత భయంకరమైనది కాదు.", "dur": 2.8, "style": "small"}],
     "cyclist", "ది ఇండియన్ సైక్లిస్ట్", "నిజమైన ప్రయాణం — తెలుగులో, Pen A Story యాప్‌లో", "యాప్ లింక్ బయోలో",
     "తెలియని దేశం, తెలియని భాష, రాత్రి ఎక్కడ పడుకోవాలో తెలియదు. అప్పుడు ఒక అపరిచితుడు తలుపు తెరిచాడు. 🚪\n\nది ఇండియన్ సైక్లిస్ట్ — 28 దేశాల్లో దొరికిన మంచితనం కథ, ఇప్పుడు తెలుగులో.\n\nఒక అపరిచితుడు మీకు సహాయం చేసిన సంఘటన ఉందా? 👇\n\n" + APP_TE + "\n\n#penastory #theindiancyclist #telugubooks #travelstories #telugureels")
print(len(list(S.glob("*.json"))), "specs")
