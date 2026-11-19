"""Content plan 21-30 Nov 2026 for @pen_a_story. Real Unsplash photography (free licence), Telugu + English mixed.
Run: python scripts/plan_nov21_30.py  -> writes specs/*.json"""
import json, pathlib, datetime
S = pathlib.Path(__file__).resolve().parent.parent / "specs"; S.mkdir(exist_ok=True)
def U(i): return f"https://images.unsplash.com/photo-{i}?w=1600&q=90"
P = {  # photo pool
 "st1": "1763688653741-bcc54bea7c26", "st2": "1743947830042-52acbb973f2d", "st3": "1764705448662-f74992067ff7", "st4": "1653494656006-869fdf081d42",
 "bench": "1771308134963-9ffb3abb2471", "bench2": "1750513538756-46e040ad48b7",
 "let1": "1779729739456-be9369745290", "let2": "1780536890742-a3d937535d66", "let3": "1528458965990-428de4b1cb0d", "let4": "1561812938-f6e60cbf95e3",
 "lib": "1507842217343-583bb7270b66", "lib2": "1481627834876-b7833e8f5570", "lib3": "1524995997946-a1c2e315a42f", "openbook": "1476275466078-4007374efbbe",
 "readsun": "1506880018603-83d5b814b5a6", "bookrow": "1495446815901-a7297e633e8d",
 "tin1": "1779635279571-988a2e63b549", "tin2": "1763801572504-e7fd828d7bf5", "tin3": "1791989642952-32b89c0d9bbf",
 "twin1": "1726747062988-cd0b86c814e0", "twin2": "1599557832120-a73f36b8f37a",
 "rain1": "1470432581262-e7880e8fe79a", "rain2": "1511634829096-045a111727eb", "rainst": "1576514864427-f0809d2b66eb",
 "oldph": "1783534784717-0843229c4f89", "bwph": "1649339035455-1b0ab8a37d49", "watch": "1509048191080-d2984bad6ae5", "clock": "1774904721886-7b3abd03be14",
 "door": "1653495482648-0cfd8847bb11", "door2": "1583008520412-7ee838891ada",
 "gma1": "1533128361669-69c065857a13", "gma2": "1560885673-4e2f056f6e2a", "gma3": "1496813146940-1601b02f81a4",
 "kitch": "1748323123788-87a32949f4b0", "kitch2": "1596450513856-250e5f5c46cc",
 "auto1": "1626149637281-4e227308da18", "auto2": "1564291886459-a39ad7415125", "auto3": "1626491058156-2daaeea7f578",
 "road": "1651678938586-affccc71c270", "water": "1768052271115-3a01d2b042b9", "girl": "1623211270083-5743da6c67ec", "vwomen": "1759738098462-90ffac98c554",
 "hills": "1567960699877-b134ad1caef8", "hillroad": "1619260584294-8a4e63f5ade5", "fall": "1754903272366-f92a6b23f18e",
 "crk1": "1706102005390-2d1f41fdddcd", "crkbw": "1706038416284-6c51d61e2f54",
 "chai1": "1792143663827-c77f1c1f2d71", "chai2": "1786161320176-96236ee66981", "chai3": "1787399087896-fff638c01a2b",
 "banyan": "1780886729568-cac46e1d8ed1", "banyan2": "1786468539777-fa9c5eae293d",
 "moon": "1522030299830-16b8d3d049fe", "moon2": "1532767153582-b1a0e5145009",
 "bdoor": "1524228529766-4d7fe5dc55ca", "crow": "1682467612877-f9b5e55ff2af", "crow2": "1572608705929-0e245b6fa24d",
 "monk": "1751963442555-38e8d2ddcddd", "monk2": "1505221594957-3931cba3a090",
 "diya": "1794550399755-2e72c031cca2", "diya2": "1605292356183-a77d0a9c9d1d",
 "bedread": "1560259344-7b4ca2f09ef9", "bedread2": "1528436610461-e9be9d1f7d6b",
 "jungle": "1694614360428-608d018bb054", "stream": "1685293080597-5d3526faf88e",
 "cofbk": "1544716278-ca5e3f4abd8c", "teabk": "1763908161557-dffe1780dda5", "cofbk2": "1474366521946-c3d4b507abf2",
 "char1": "1696941515998-d83f24967aca", "char2": "1750834115164-8c2658f18dd0", "market": "1787044050216-19d30c0aeaf5",
}
APP = "Daily stories in Telugu & English — free Pen A Story app, link in bio."

def carousel(name, label, frames, end, cap):
    """frames: [(photo, text, small?)]; end: (photo, question, small)"""
    keys = []; slides = []
    for f in frames + [end]:
        if f[0] not in keys: keys.append(f[0])
    for i, f in enumerate(frames):
        sl = {"image": keys.index(f[0]), "text": f[1]}
        if len(f) > 2 and f[2]: sl["small"] = f[2]
        slides.append(sl)
    slides.append({"kind": "end", "image": keys.index(end[0]), "text": end[1], "small": end[2]})
    (S / f"{name}.json").write_text(json.dumps({"kind": "carousel", "style": "photo", "label": label, "images": [U(P[k]) for k in keys],
        "slides": slides, "caption": cap}, ensure_ascii=False, indent=1))

def story(name, photo, title, text="", kicker="", cta=""):
    (S / f"{name}.json").write_text(json.dumps({"kind": "story", "style": "photo", "images": [U(P[photo])], "title": title, "text": text,
        "kicker": kicker, "cta": cta}, ensure_ascii=False, indent=1))

days = [f"2026-11-{d}" for d in range(20, 30)]   # started 20 Nov (shifted one day earlier)
SER = "PLATFORM NO. 3 · సీరియల్"

# ======================= SERIAL: Platform No. 3 (13:00) =======================
serial = [
 ([("st1", "Secunderabad station. రాత్రి 9 గంటలు. Meera, 27, Vizag కి 9:40 train కోసం wait చేస్తోంది.", "Episode 1"),
   ("bench", "Waiting room bench మీద ఎవరో మర్చిపోయిన ఒక పాత book."),
   ("let1", "Book లోపల ఒక పసుపు రంగు envelope. పైన రాసి ఉంది: \"To Meera.\""),
   ("let3", "Postmark: 1998. Meera పుట్టింది 1999లో."),
   ("st2", "లోపల ఒక్కటే line: \"Meera, 9:40 train ఎక్కకు.\"")],
  ("st3", "మీరైతే ఆ train ఎక్కుతారా?", "Episode 2 — రేపు 1 PM")),
 ([("st2", "9:38. Train platform మీదకి వచ్చింది. Meera కాళ్ళు కదలలేదు.", "Episode 2"),
   ("st4", "9:40. Train వెళ్ళిపోయింది. Meera ఒక్కతే platform మీద."),
   ("let2", "Envelope లో ఇంకో page ఉంది. \"నువ్వు ఎక్కలేదంటే — Platform No. 3, bench 4 కి వెళ్ళు.\""),
   ("bench2", "Bench 4 మీద ఒక old man. Meera ని చూడగానే లేచి నిలబడ్డాడు."),
   ("tin2", "\"నువ్వు late అయ్యావు, Meera. 27 years late.\"")],
  ("bench", "ఆ old man ఎవరు అనుకుంటున్నారు?", "Episode 3 — రేపు 1 PM")),
 ([("tin2", "\"నా పేరు Raghavaiah. ఈ station కి 30 years station master ని.\"", "Episode 3"),
   ("st1", "\"1998లో ఒక అమ్మాయి ఈ book నాకు ఇచ్చింది. 'Meera అనే అమ్మాయి వస్తుంది. Give her this.'\""),
   ("watch", "\"27 years. ప్రతి రోజు ఈ bench దగ్గర wait చేశాను.\""),
   ("oldph", "ఆయన pocket నుంచి ఒక పాత photo తీశాడు. \"ఆ అమ్మాయి ఇదే.\""),
   ("bwph", "Meera photo చూసింది. ఆ face — అచ్చం తన face లాగే ఉంది.")],
  ("oldph", "ఆ photo లో ఉన్నది ఎవరు?", "Episode 4 — రేపు 1 PM")),
 ([("rain1", "రాత్రి 11. Meera అమ్మకి video call చేసింది. Photo చూపించింది.", "Episode 4"),
   ("gma2", "అమ్మ మాట్లాడలేదు. Screen లో ఆమె కళ్ళు మాత్రమే కనిపించాయి."),
   ("rain2", "\"ఈ photo... నీకు ఎక్కడ దొరికింది?\""),
   ("clock", "Meera చెప్పింది. Station. Book. Letter. 1998."),
   ("gma2", "అమ్మ నెమ్మదిగా అంది: \"అది నేను కాదు, Meera. అది నీ అక్క.\"")],
  ("rain1", "Meera కి ఒక అక్క ఉందా?! Guess చేయండి 👇", "Episode 5 — రేపు 1 PM")),
 ([("gma1", "\"Lalitha. నీకంటే 8 years పెద్దది.\"", "Episode 5"),
   ("door", "\"1998లో ఒక పెద్ద గొడవ. పెళ్ళి వద్దు, నేను teacher అవుతాను అంది.\""),
   ("door2", "\"ఆ రాత్రి bag పట్టుకుని వెళ్ళిపోయింది. తిరిగి రాలేదు.\""),
   ("gma3", "\"అప్పుడు నేను నిన్ను కడుపుతో ఉన్నాను. ఆమెకి తెలుసు — నీ పేరు Meera అని పెట్టింది తనే.\""),
   ("st4", "\"చివరిగా ఆమె కనిపించింది... Platform No. 3 దగ్గరే.\"")],
  ("door", "Lalitha ఎందుకు తిరిగి రాలేదు?", "Episode 6 — రేపు 1 PM")),
 ([("openbook", "Meera ఆ book మళ్ళీ తెరిచింది. ఇది novel కాదు. ఇది Lalitha diary.", "Episode 6"),
   ("let4", "ప్రతి page margin లో చిన్న అక్షరాలు. \"అమ్మకి sorry చెప్పలేకపోయాను.\""),
   ("lib3", "\"Proud గా వెళ్ళాను. Shame తో తిరిగి రాలేకపోయాను.\""),
   ("let1", "చివరి page లో pencil తో గీసిన ఒక map. Hills. ఒక tunnel. ఒక చిన్న school."),
   ("hills", "Map కింద ఒక word: \"Araku.\"")],
  ("let1", "Meera Araku వెళ్తుందా?", "Episode 7 — రేపు 1 PM")),
 ([("st3", "ఉదయం 6:45. Vizag–Araku train. Meera, పక్కన Raghavaiah.", "Episode 7"),
   ("twin1", "Window బయట hills. Tunnels. పొగమంచు."),
   ("hillroad", "Map follow చేస్తూ ఒక మట్టి దారి. రెండు కిలోమీటర్లు నడక."),
   ("road", "దారి చివర ఒక చిన్న school. Gate మీద board:"),
   ("girl", "\"Lalitha's School — Est. 2001.\"")],
  ("road", "Lalitha లోపల ఉంటుందా?", "Episode 8 — రేపు 1 PM")),
 ([("vwomen", "ఒక teacher బయటకి వచ్చింది. \"Lalitha madam market కి వెళ్ళారు. Evening వస్తారు.\"", "Episode 8"),
   ("girl", "Kids Meera చుట్టూ చేరారు. \"మీరు అచ్చం madam లాగే ఉన్నారు!\""),
   ("let2", "ఒక పిల్లాడు ఒక wall చూపించాడు. దాని మీద envelopes. వరుసగా."),
   ("let3", "ప్రతి envelope మీద ఒకే పేరు: \"To Meera.\" ప్రతి సంవత్సరం Nov 20."),
   ("let1", "Meera లెక్కపెట్టింది. 27 letters. ఒక్కటీ post చేయలేదు.")],
  ("let2", "ఆ letters లో ఏం రాసి ఉంటుంది?", "Episode 9 — రేపు 1 PM")),
 ([("hills", "సాయంత్రం 6. పొగమంచులో ఒక figure నడుచుకుంటూ వస్తోంది.", "Episode 9"),
   ("water", "Lalitha. చేతిలో కూరగాయల సంచి. Meera ని చూసి ఆగిపోయింది."),
   ("girl", "ఎవరూ మాట్లాడలేదు. Kids కూడా silent."),
   ("vwomen", "Lalitha: \"నువ్వు వస్తావని తెలుసు. ఆ book నిన్ను తీసుకొస్తుందని.\""),
   ("diya", "\"కానీ ఒక విషయం అమ్మకి ఇప్పటికీ తెలియదు.\"")],
  ("water", "ఆ secret ఏమై ఉంటుంది? Finale రేపు!", "Final Episode — రేపు 1 PM")),
 ([("diya", "\"9:40 train. 1998లో నేను ఎక్కిన train అదే.\"", "Final Episode"),
   ("st2", "\"ఎవరికీ చెప్పకుండా వెళ్ళిపోయాను. ఆ ఒక్క train నా life నుంచి family ని తీసేసింది.\""),
   ("let4", "\"నువ్వు నాలాగా ఎప్పుడూ silent గా వెళ్ళిపోకూడదు. అందుకే ఆ letter.\""),
   ("gma1", "ఆ రాత్రి video call. అమ్మ, Lalitha, Meera. 27 years తర్వాత ముగ్గురూ ఒకే screen లో."),
   ("diya2", "కొన్ని trains miss అయితేనే, మనం ఇంటికి చేరతాం.")],
  ("st1", "ఏ episode మిమ్మల్ని ఎక్కువ కదిలించింది?", "Season 2 త్వరలో · Follow చేయండి")),
]
for i, (fr, end) in enumerate(serial):
    ep = i + 1
    hook = fr[0][1]
    cap = (f"Platform No. 3 · Episode {ep}{' (Finale)' if ep == 10 else ''} 🚉\n\n{hook}\n\n"
           + ("Swipe చేయండి — చివరి slide లో cliffhanger.\n\n" if ep < 10 else "Swipe చేసి finale చదవండి.\n\n")
           + ("ప్రతి రోజు 1 PM కి కొత్త episode. Miss అవ్వకుండా follow చేయండి.\n" if ep < 10 else "Season 2 త్వరలో. ఈ story ఎవరికి పంపాలనిపిస్తుంది? Share చేయండి.\n")
           + f"{APP}\n\n#penastory #platformno3 #telugustories #teluguserial #tenglish")
    carousel(f"{days[i]}-1300-serial-platform3-ep{ep:02d}", SER, fr, end, cap)
    if ep < 10:
        story(f"{days[i]}-2130-story-teaser-ep{ep + 1:02d}", serial[ep][0][0][0], f"Platform No. 3 · Episode {ep + 1}",
              "రేపు 1 PM. Notification on చేసుకోండి 🔔", "TOMORROW · రేపు", "1 PM")

# ======================= STANDALONE (19:30) =======================
ONE = "PEN A STORY · ఒక్క కథ"
stand = [
 ("auto-library", [("auto1", "ఈ auto లో meter లేదు. Books ఉన్నాయి.", "ఒక్క కథ · Auto Anna's Library"),
   ("auto3", "Ramesh anna, Ameerpet. Back seat వెనక ఒక చిన్న shelf. 12 books."),
   ("bookrow", "Rule simple: ride లో చదవొచ్చు. నచ్చితే తీసుకెళ్ళొచ్చు. ఒకే condition — ఇంకో book వదిలేయాలి."),
   ("auto2", "ఒక college boy అడిగాడు: \"Anna, మీరు ఎంత వరకు చదువుకున్నారు?\""),
   ("auto3", "\"ఐదో తరగతి. కానీ ఈ auto లో రోజూ పది universities ఎక్కుతాయి.\""),
   ("lib", "3 years later, ఆ boy తిరిగి వచ్చాడు — తను రాసిన మొదటి book తో. First page: \"For Ramesh anna, my first library.\"")],
  ("auto1", "మీ life లో Ramesh anna ఎవరు?", "Comment లో tag చేయండి"), "ఈ auto లో meter లేదు. Books ఉన్నాయి. 🛺📚"),
 ("tiffin-note", [("kitch", "అమ్మ tiffin box లో అన్నంతో పాటు ఒక చిన్న చీటీ ఉండేది.", "ఒక్క కథ · Tiffin Note"),
   ("let3", "\"నీళ్ళు తాగు.\" \"Exam బాగా రాయి.\" \"భయపడకు.\""),
   ("kitch2", "10th class కి వచ్చేసరికి, చీటీలు చదవకుండానే పారేసేవాడిని. Embarrassing అనిపించేది."),
   ("rain2", "ఇప్పుడు నాకు 35. Bangalore. అమ్మ Guntur లో."),
   ("kitch", "నిన్న రాత్రి నా కూతురి tiffin pack చేస్తూ, ఆగిపోయాను."),
   ("let4", "ఒక చిన్న paper తీసి రాశాను: \"భయపడకు.\" కొన్ని అలవాట్లు ప్రేమగా తిరిగి వస్తాయి.")],
  ("kitch", "అమ్మ మీకు చెప్పిన ఒక మాట ఏది?", "Comment చేయండి 👇"), "అమ్మ tiffin box లో ఒక చీటీ ఉండేది. 🍱"),
 ("cricket-ball", [("crk1", "1996. మా గల్లీ cricket. Last ball. 6 runs కావాలి.", "ఒక్క కథ · The Window"),
   ("crkbw", "నేను బలంగా కొట్టాను. Ball నేరుగా Sharma uncle window లోకి. Crash."),
   ("door2", "అందరూ పారిపోయారు. Uncle ball ఇవ్వలేదు. మళ్ళీ ఎప్పుడూ."),
   ("oldph", "2026. Uncle పోయారు. వాళ్ళ అబ్బాయి ఒక box ఇచ్చాడు: \"నాన్న నీ కోసం ఉంచారు.\""),
   ("watch", "లోపల ఆ ball. దాని మీద marker తో: \"Best six I ever saw. — Sharma, 1996.\"")],
  ("crk1", "మీ childhood లో break చేసిన window ఏది? 😄", "Confess చేయండి 👇"), "Last ball. 6 runs. ఒక window. 🏏"),
 ("umbrella", [("rainst", "Koti bus stop. July. ఉరుములతో వర్షం.", "ఒక్క కథ · One Umbrella"),
   ("rain1", "ఒక stranger తన umbrella లో చోటు ఇచ్చాడు. 20 minutes. ఇద్దరూ ఒక్క మాట మాట్లాడలేదు."),
   ("rain2", "Bus వచ్చింది. ఆమె ఎక్కింది. Umbrella అతని దగ్గరే ఉంది. పేరు కూడా అడగలేదు."),
   ("clock", "ప్రతి వర్షాకాలం అతను అదే bus stop కి వెళ్ళేవాడు. Just in case."),
   ("rainst", "7th year. ఒక అమ్మాయి వచ్చి నిలబడింది. చేతిలో ఒక umbrella. \"ఇది తిరిగి ఇవ్వడానికి 7 years పట్టింది.\"")],
  ("rain1", "Rain అంటే మీకు గుర్తొచ్చే memory ఏది?", "Comment చేయండి ☔"), "Koti bus stop. ఒక వర్షం. ఒక umbrella. ☔"),
 ("chai-5am", [("chai1", "Narayana chai stall. ఉదయం 5 గంటలు. 30 years.", "ఒక్క కథ · The 5 AM Chai"),
   ("chai3", "ఆయనకి అందరి order గుర్తు. Auto drivers కి strong. Students కి extra sugar."),
   ("chai2", "ఒక old man రోజూ వచ్చేవాడు. ఒకే chai. ఒకే corner. ఎప్పుడూ ఒంటరిగా."),
   ("clock", "ఒక రోజు ఆయన రాలేదు. రెండో రోజు కూడా. మూడో రోజు Narayana stall మూసేశాడు."),
   ("door", "Flask పట్టుకుని old man ఇంటికి వెళ్ళాడు. జ్వరం. ఒంటరిగా."),
   ("chai1", "\"మీ chai రాలేదు అంటే, ఏదో తేడా ఉందని తెలుసు.\" కొన్ని relationships కి పేరు అవసరం లేదు.")],
  ("chai2", "మీ favourite chai stall ఎక్కడ?", "Tag చేయండి ☕"), "ఉదయం 5. ఒక chai stall. ఒక old man. ☕"),
 ("moon-call", [("moon", "\"చందమామ రావే, జాబిల్లి రావే...\" అమ్మమ్మ ప్రతి రాత్రి ఇదే పాడేది.", "ఒక్క కథ · Same Moon"),
   ("gma3", "Terrace మీద. గోరుముద్దలు. Moon వైపు చూపిస్తూ కథలు."),
   ("moon2", "ఇప్పుడు నేను Texas లో. అమ్మమ్మ Rajahmundry లో. 13,000 km."),
   ("bedread2", "ప్రతి పౌర్ణమి రాత్రి నేను video call చేస్తాను."),
   ("moon", "ఇద్దరం camera ని moon వైపు తిప్పుతాం. \"చూశావా? అదే చందమామ.\"")],
  ("moon2", "మీ అమ్మమ్మ పాడిన పాట ఏది?", "Comment లో రాయండి 🌕"), "Texas లో నేను. Rajahmundry లో అమ్మమ్మ. ఒకే చందమామ. 🌕"),
 ("karthika-diya", [("diya", "Karthika masam. ప్రతి సాయంత్రం Savitri gaaru గడప దగ్గర ఒక దీపం పెడతారు.", "ఒక్క కథ · The Diya"),
   ("gma1", "\"ఎవరి కోసం?\" అని పక్కింటి అమ్మాయి అడిగింది. \"Germany లో మా అబ్బాయి కోసం.\""),
   ("diya2", "\"దీపం ఆరకుండా ఉంటే, వాడికి దారి కనిపిస్తుంది.\""),
   ("door2", "30 రోజులు. 30 దీపాలు. ఒక్కసారీ ఆరలేదు."),
   ("diya", "కార్తీక పౌర్ణమి రాత్రి గేటు చప్పుడు. చేతిలో suitcase. \"అమ్మా, దారి కనిపించింది.\"")],
  ("diya2", "మీ ఇంట్లో ఎవరు దీపం పెడతారు?", "Comment చేయండి 🪔"), "Karthika masam. ఒక దీపం. ఒక అమ్మ. 🪔"),
 ("exam-pen", [("lib2", "EAMCET exam hall. నా pen పని చేయడం మానేసింది. 3 hours మిగిలి ఉన్నాయి.", "ఒక్క కథ · The Pen"),
   ("let4", "పక్క bench అమ్మాయి ఒక్క మాట లేకుండా తన spare pen ఇచ్చింది."),
   ("clock", "Exam అయిపోయింది. Pen తిరిగి ఇవ్వడానికి వెతికాను. కనిపించలేదు."),
   ("cofbk", "15 years ఆ pen నా desk మీదే ఉంది. ప్రతి interview కి, ప్రతి sign కి."),
   ("market", "ఈ రోజు నా clinic లో ఒక patient. Form మీద sign చేయడానికి pen అడిగింది."),
   ("let3", "నేను ఆ pen ఇచ్చాను. ఆమె చూసి నవ్వింది: \"ఇది నాదే కదా?\"")],
  ("lib2", "మీకు ఎవరైనా ఇచ్చిన చిన్న help, life ని మార్చిందా?", "Share చేయండి 👇"), "Exam hall. Pen పని చేయలేదు. 3 hours. ✍️"),
 ("charminar-photo", [("char1", "1975. Charminar ముందు ఒక black & white photo. Newly married couple.", "ఒక్క కథ · Same Spot"),
   ("bwph", "అదే photo 50 years వాళ్ళ ఇంటి wall మీద ఉంది."),
   ("market", "2025. Golden anniversary. మనవడు అడిగాడు: \"తాతయ్యా, ఏం gift కావాలి?\""),
   ("char2", "\"అదే spot. అదే pose. ఇంకో photo.\""),
   ("char1", "అదే Charminar. అదే నవ్వు. Frame లో ఒక్క మార్పు — అమ్మమ్మ చేయి ఇప్పుడు తాతయ్య చేతిలో.")],
  ("char2", "మీ family లో ఒక old photo story చెప్పండి", "Comment చేయండి 📷"), "1975. Charminar. ఒక photo. 50 years later. 📷"),
 ("grandpa-watch", [("watch", "తాతయ్య watch 4:17 దగ్గర ఆగిపోయింది. ఆయన ఎవరినీ repair చేయనివ్వలేదు.", "ఒక్క కథ · 4:17"),
   ("gma1", "\"Watch తప్పు టైం చూపిస్తోంది తాతయ్యా.\" ఆయన నవ్వేవారు: \"లేదు. Correct గానే ఉంది.\""),
   ("let2", "ఆయన పోయిన తర్వాత drawer లో ఒక పాత letter."),
   ("st2", "1971. ఒక railway station. మంటల్లో ఒక coach. ఆయన 12 మందిని బయటకి లాగారు."),
   ("let1", "Letter చివర: \"You saved us at 4:17. We will never forget.\" ఆయన ఎవరికీ చెప్పలేదు. Time ని మాత్రం ఉంచుకున్నారు.")],
  ("watch", "మీ family లో silent hero ఎవరు?", "Comment చేయండి 🕰️"), "తాతయ్య watch 4:17 దగ్గర ఆగిపోయింది. ఎందుకు? 🕰️"),
]
for i, (slug, fr, end, hook) in enumerate(stand):
    cap = (f"{hook}\n\nఒక్క post లో పూర్తి కథ — చివరి వరకు swipe చేయండి.\n\n"
           f"{end[1]} {end[2]}\n\nఈ కథ ఎవరికైనా గుర్తు చేస్తే, వాళ్ళకి send చేయండి.\n{APP}\n\n#penastory #telugustories #shortstory #tenglish #storytelling")
    carousel(f"{days[i]}-1930-story-{slug}", ONE, fr, end, cap)

# ======================= 16:30 rotation: nostalgia / memes / quiz / call-outs =======================
NOS = "చిన్నప్పటి కథలు · NOSTALGIA"
def nostalgia(day, slug, fr, end, hook):
    cap = (f"{hook}\n\nచిన్నప్పుడు అమ్మమ్మ, తాతయ్య, Chandamama చెప్పిన కథలు — మళ్ళీ ఒకసారి.\n\n{end[1]}\n\n"
           f"మీ childhood friend ని tag చేయండి — వాళ్ళకీ గుర్తొస్తుంది.\n{APP}\n\n#penastory #childhoodmemories #telugukathalu #panchatantra #nostalgia")
    carousel(f"{day}-1630-nostalgia-{slug}", NOS, fr, end, cap)

nostalgia(days[1], "thirsty-crow",
  [("crow", "గుర్తుందా? మనం విన్న మొదటి కథ ఇదే కావచ్చు.", "దాహం వేసిన కాకి"),
   ("road", "ఎండాకాలం. ఒక కాకికి చాలా దాహం. ఎక్కడా నీళ్ళు లేవు."),
   ("water", "ఒక కుండ కనిపించింది. కానీ నీళ్ళు అడుగున ఉన్నాయి. ముక్కు అందలేదు."),
   ("crow2", "కాకి ఆలోచించింది. ఒక్కో రాయి తెచ్చి కుండలో వేసింది. ఒకటి. రెండు. పది."),
   ("crow", "నీళ్ళు పైకి వచ్చాయి. కాకి తాగి ఎగిరిపోయింది. Moral: బుద్ధి ఉంటే దారి ఉంటుంది.")],
  ("crow2", "ఈ కథ మీకు ఎవరు చెప్పారు?", "Comment చేయండి 👇"), "దాహం వేసిన కాకి 🐦‍⬛ గుర్తుందా?")
nostalgia(days[4], "tenali-thieves",
  [("banyan", "Tenali Ramakrishna. Vijayanagara. ఒక రాత్రి ఇంటి బయట దొంగలు దాక్కున్నారు.", "Tenali Raman & the Thieves"),
   ("door", "Rama గమనించాడు. భార్యతో గట్టిగా అన్నాడు: \"నగలన్నీ ఈ పెట్టెలో పెట్టి బావిలో పడేద్దాం. Safe.\""),
   ("water", "ఇద్దరూ ఒక బరువైన పెట్టెని బావిలో పడేశారు. లోపల ఉన్నవి రాళ్ళు."),
   ("moon", "రాత్రంతా దొంగలు బావిలో నీళ్ళు తోడారు. తోటంతా తడిసింది."),
   ("banyan2", "ఉదయం Rama: \"Thank you! మా తోటకి నీళ్ళు పెట్టినందుకు.\" దొంగలు పారిపోయారు.")],
  ("banyan", "మీకు favourite Tenali కథ ఏది?", "Comment చేయండి 😄"), "Tenali Ramakrishna vs దొంగలు 😄 ఈ కథ గుర్తుందా?")
nostalgia(days[6], "monkey-crocodile",
  [("monk", "నది ఒడ్డున ఒక నేరేడు చెట్టు. దాని మీద ఒక కోతి. రోజూ ఒక మొసలికి పండ్లు ఇచ్చేది.", "కోతి – మొసలి"),
   ("stream", "మొసలి భార్య అంది: \"ఇంత తీపి పండ్లు తినే కోతి గుండె ఇంకా తీపిగా ఉంటుంది. తీసుకురా.\""),
   ("jungle", "మొసలి కోతిని వీపు మీద ఎక్కించుకుని నది మధ్యకి తీసుకెళ్ళి నిజం చెప్పింది."),
   ("monk2", "కోతి నవ్వింది: \"అయ్యో! నా గుండె చెట్టు మీదే వదిలేశాను. వెనక్కి పద, తెచ్చిస్తా.\""),
   ("monk", "ఒడ్డుకి చేరగానే కోతి చెట్టెక్కేసింది. Moral: ఆపదలో కూడా ప్రశాంతంగా ఆలోచించు.")],
  ("monk2", "Panchatantra లో మీ favourite కథ?", "Comment చేయండి 🐒"), "కోతి – మొసలి 🐒🐊 Panchatantra గుర్తుందా?")
nostalgia(days[8], "birbal-khichdi",
  [("diya2", "Akbar ఒక challenge పెట్టాడు: \"చలి రాత్రి అంతా చెరువులో నిలబడితే బహుమతి.\"", "Birbal's Khichdi"),
   ("moon2", "ఒక పేదవాడు రాత్రంతా నిలబడ్డాడు. దూరంగా palace లో ఒక దీపం చూస్తూ."),
   ("bdoor", "Akbar: \"దీపం వేడి నీకు అందింది. బహుమతి లేదు.\" Birbal ఏమీ అనలేదు."),
   ("kitch2", "మర్నాడు Birbal court కి రాలేదు. \"Khichdi వండుతున్నా\" అని కబురు. కుండ చెట్టు మీద. మంట కింద చాలా దూరంగా."),
   ("diya", "Akbar నవ్వాడు, అర్థమైంది. ఆ పేదవాడికి బహుమతి ఇచ్చాడు.")],
  ("bdoor", "Akbar–Birbal లో మీ favourite కథ?", "Comment చేయండి 👑"), "Birbal ఖిచిడీ ఎందుకు వండలేదు? 👑")

def memes(day, slug, items, end, hook):
    cap = f"{hook}\n\nRelate అయితే, ఒక reader friend కి send చేయండి 😂\n{APP}\n\n#penastory #booklovers #readermemes #telugumemes #bookstagramindia"
    carousel(f"{day}-1630-memes-{slug}", "READER PROBLEMS · 😅", items, end, cap)
memes(days[0], "readers-1",
  [("bedread", "Me: ఒక్క chapter మాత్రమే.\nClock: 3:47 AM 🙂", "Reader problems"),
   ("bedread2", "అమ్మ: \"Light off చెయ్యి.\"\nMe, blanket లో torch తో:"),
   ("cofbk", "Book లో character చనిపోతే, ఇంట్లో ఎవరికైనా చెప్పాలనిపిస్తుంది. ఎవరూ పట్టించుకోరు."),
   ("lib", "Bookshop కి 'just looking' అని వెళ్ళి, 4 books తో బయటకి రావడం.")],
  ("teabk", "ఏది మీరు? 1, 2, 3 లేదా 4?", "Comment చేయండి 😂"), "ఒక్క chapter మాత్రమే అనుకుంటాం… 😂")
memes(days[7], "readers-2",
  [("cofbk2", "Book చదివిన తర్వాత movie చూస్తే:\n\"Book లో ఇలా లేదు\" 😤", "Reader problems"),
   ("teabk", "Bookmark: available.\nMe: చేతిలో ఉన్న bill, ticket, Aadhaar xerox పెడతా."),
   ("rain1", "వర్షం + chai + book = జీవితంలో ఇంకేం అక్కర్లేదు."),
   ("bedread", "Story climax లో ఉన్నప్పుడు ఎవరో పిలిస్తే: 🙂🔪")],
  ("cofbk2", "మీ biggest reader problem ఏది?", "Comment చేయండి 😅"), "Book చదివాక movie చూస్తే… 😤")

def textcar(day, slot, slug, label, fr, end, cap):
    carousel(f"{day}-{slot}-{slug}", label, fr, end, cap)
textcar(days[2], "1630", "oneline-ep01", "ONE LINE. YOUR TURN. · EP 01",
  [("let1", "మేము మొదటి line రాస్తాం. Second line మీది.", "How to play"),
   ("st3", "\"ఆ letter ఒక Tuesday వచ్చింది. దాని మీద date — next year.\"")],
  ("let3", "తర్వాత ఏమైంది? Next line మీరు రాయండి", "Most-liked line wins 🏆"),
  "\"ఆ letter ఒక Tuesday వచ్చింది. దాని మీద date — next year.\" ✉️\n\nFirst line మాది. Second line మీది — comment లో రాయండి (Telugu, English, ఏ language అయినా).\n\nMost-liked line wins. 🏆\n\n#penastory #onelineyourturn #writingprompt #telugustories #storytelling")
textcar(days[3], "1630", "author-callout", "CALLING ALL WRITERS · రచయితలకు",
  [("let4", "మీ దగ్గర ఒక కథ ఉందా? Notebook లో, phone notes లో, మనసులో?", "Calling all writers"),
   ("cofbk", "Telugu లో అయినా, English లో అయినా — Pen A Story మీ book ని publish చేస్తుంది. Free of cost."),
   ("lib3", "మీ book 175+ countries లో readers కి చేరుతుంది.")],
  ("let4", "DM చేయండి: AUTHOR", "మీ మొదటి book ఇక్కడ మొదలవ్వచ్చు"),
  "మీ దగ్గర ఒక కథ ఉందా? ✍️\n\nTelugu లో అయినా, English లో అయినా — Pen A Story మీ eBook ని publish చేస్తుంది, free of cost. 175+ countries లో readers.\n\nInterested? \"AUTHOR\" అని DM చేయండి. Writer friend ని tag చేయండి 👇\n\n#penastory #teluguwriters #indianauthors #publishyourbook #writersofinstagram")
textcar(days[5], "1630", "quiz-guess-story", "STORY QUIZ · కథ కనుక్కోండి",
  [("jungle", "3 clues. ఒక్క కథ. Guess చేయగలరా?", "Story Quiz #1"),
   ("stream", "Clue 1: ఒక నది."),
   ("jungle", "Clue 2: ఒక చెట్టు మీద తీపి పండ్లు."),
   ("monk2", "Clue 3: \"నా గుండె చెట్టు మీదే వదిలేశాను.\"")],
  ("stream", "ఏ కథ? Comment చేయండి", "Answer రేపు story లో"),
  "3 clues. ఒక్క కథ. 🔍\n\nనది. తీపి పండ్లు. \"నా గుండె చెట్టు మీదే వదిలేశాను.\"\n\nఏ కథో comment చేయండి — answer రేపు story లో. 90s kids కి easy 😉\n\n#penastory #storyquiz #panchatantra #telugukathalu #childhoodmemories")
textcar(days[9], "1630", "oneline-ep02", "ONE LINE. YOUR TURN. · EP 02",
  [("st4", "మేము మొదటి line రాస్తాం. Second line మీది.", "Episode 2"),
   ("rain2", "\"ఆ రాత్రి power పోయింది. చీకట్లో ఎవరో నా పేరు పిలిచారు — నా గొంతుతోనే.\"")],
  ("rain1", "తర్వాత ఏమైంది? మీ line రాయండి", "Most-liked line wins 🏆"),
  "\"ఆ రాత్రి power పోయింది. చీకట్లో ఎవరో నా పేరు పిలిచారు — నా గొంతుతోనే.\" 🕯️\n\nSecond line మీది. Comment లో రాయండి. Most-liked line wins. 🏆\n\n#penastory #onelineyourturn #writingprompt #telugustories #horrorstory")

# ======================= 10:30 meme / mood stories =======================
am = [("bedread", "Me: 10 PM కి పడుకుంటా.\nAlso me at 2 AM: \"ఇంకో episode.\"", "Mood"),
      ("crow", "కాకి – కుండ కథ: మన first problem-solving class 🐦‍⬛", "Today 4:30 PM"),
      ("chai1", "Weekend plan: chai + కథ + no phone calls ☕", "Weekend mood"),
      ("lib2", "Calling all writers ✍️ మీ కథ మాకు పంపండి — today 4:30 PM", "Writers"),
      ("banyan", "Tenali Ramakrishna is back 😄 Today 4:30 PM", "Nostalgia"),
      ("monk2", "Story quiz ఈ రోజు 4:30 PM 🔍 90s kids ready?", "Quiz day"),
      ("monk", "Quiz answer: కోతి – మొసలి 🐒🐊 Full story ఈ రోజు 4:30 PM", "Answer"),
      ("teabk", "Weekend reading pile ready ఉందా? 📚", "Weekend soon"),
      ("bdoor", "Birbal ఖిచిడీ కథ ఈ రోజు 4:30 PM 👑", "Nostalgia"),
      ("rain2", "Platform No. 3 Finale ఈ రోజు 1 PM 🚉", "FINALE")]
for i, (ph, t, k) in enumerate(am):
    story(f"{days[i]}-1030-story-am", ph, t, "", k.upper())
print(len(list(S.glob("2026-11-2*.json"))) + len(list(S.glob("2026-11-30*.json"))), "specs")

# ======================= ENGLISH half (50/50 balance) =======================
APP_EN = "New stories every day on the free Pen A Story app. Link in bio."
ONE_EN = "PEN A STORY · ONE STORY"
def stand_en(day, slug, fr, end, hook):
    cap = (f"{hook}\n\nA complete story in one post. Swipe to the end.\n\n{end[1]} {end[2]}\n\n"
           f"If this reminded you of someone, send it to them.\n{APP_EN}\n\n#penastory #shortstory #storytelling #indianauthors #bookstagramindia")
    carousel(f"{day}-1930-story-{slug}", ONE_EN, fr, end, cap)
stand_en(days[3], "umbrella", [("rainst", "Koti bus stop. July. Thunder, and the kind of rain that doesn't stop.", "One Story · One Umbrella"),
   ("rain1", "A stranger tilted his umbrella toward her. Twenty minutes. Not a single word."),
   ("rain2", "Her bus came. She got on. The umbrella stayed with him. He never asked her name."),
   ("clock", "Every monsoon after that, he went back to the same bus stop. Just in case."),
   ("rainst", "Seventh year. A woman stood beside him, holding an umbrella. \"It took me seven years to return this.\"")],
  ("rain1", "What's your favourite rain memory?", "Tell us below ☔"), "One bus stop. One rain. One umbrella. ☔")
stand_en(days[4], "chai-5am", [("chai1", "Narayana's chai stall. 5 AM. Thirty years.", "One Story · The 5 AM Chai"),
   ("chai3", "He knew every order by heart. Strong for the auto drivers. Extra sugar for the students."),
   ("chai2", "One old man came every day. One chai. Same corner. Always alone."),
   ("clock", "One morning he didn't come. Nor the next. On the third day, Narayana shut his stall early."),
   ("door", "He carried a flask to the old man's house. Fever. Nobody else had noticed."),
   ("chai1", "\"When your chai goes undrunk, I know something is wrong.\" Some relationships don't need a name.")],
  ("chai2", "Where's your favourite chai stall?", "Tag it ☕"), "5 AM. A chai stall. An old man who stopped coming. ☕")
stand_en(days[7], "exam-pen", [("lib2", "Exam hall. My pen died. Three hours to go.", "One Story · The Pen"),
   ("let4", "The girl at the next bench slid her spare pen across. Didn't say a word."),
   ("clock", "When the exam ended, I looked for her to return it. She was gone."),
   ("cofbk", "Fifteen years, that pen sat on my desk. Every interview. Every signature."),
   ("market", "Today a patient at my clinic asked to borrow a pen for her form."),
   ("let3", "I handed her that pen. She looked at it and smiled. \"Isn't this mine?\"")],
  ("lib2", "Has a tiny kindness ever changed your life?", "Share it below 👇"), "My pen died in the exam hall. Three hours left. ✍️")
stand_en(days[9], "grandpa-watch", [("watch", "My grandfather's watch stopped at 4:17. He never let anyone fix it.", "One Story · 4:17"),
   ("gma1", "\"Your watch is wrong, thatha.\" He'd smile. \"No. It's right.\""),
   ("let2", "After he passed, we found an old letter in his drawer."),
   ("st2", "1971. A railway station. A coach on fire. He pulled twelve people out."),
   ("let1", "The letter ended: \"You saved us at 4:17. We will never forget.\" He never told anyone. He just kept the time.")],
  ("watch", "Who's the quiet hero in your family?", "Tell us below 🕰️"), "Why did grandfather's watch stop at 4:17? 🕰️")
textcar(days[3], "1630", "author-callout", "CALLING ALL WRITERS",
  [("let4", "Got a story sitting in a notebook, your phone notes, or your head?", "Calling all writers"),
   ("cofbk", "Pen A Story publishes new authors as eBooks. English or Telugu. No publishing fee."),
   ("lib3", "Your book reaches readers in 175+ countries through the Pen A Story app.")],
  ("let4", "DM us the word AUTHOR", "Your first book could start here"),
  "Got a story you've never shown anyone? ✍️\n\nPen A Story publishes new authors as eBooks, in English or Telugu, with no publishing fee. Readers in 175+ countries.\n\nDM us \"AUTHOR\" to start. Tag a friend who should be writing 👇\n\n#penastory #indianauthors #writersofinstagram #publishyourbook #amwriting")
memes(days[0], "readers-1",
  [("bedread", "Me: just one chapter.\nThe clock: 3:47 AM 🙂", "Reader problems"),
   ("bedread2", "Mum: \"Lights off.\"\nMe under the blanket with a torch:"),
   ("cofbk", "When a character dies and you need to tell someone, but nobody in the house cares."),
   ("lib", "Walking into a bookshop \"just to look\" and walking out with four books.")],
  ("teabk", "Which one is you? 1, 2, 3 or 4?", "Tell us 😂"), "\"Just one chapter,\" we said… 😂")
textcar(days[2], "1630", "oneline-ep01", "ONE LINE. YOUR TURN. · EP 01",
  [("let1", "We write the first line. You write the second.", "How to play"),
   ("st3", "\"The letter arrived on a Tuesday. It was postmarked next year.\"")],
  ("let3", "What happens next? Write line two", "Most-liked line wins 🏆"),
  "\"The letter arrived on a Tuesday. It was postmarked next year.\" ✉️\n\nThe first line is ours. The second is yours. Write it in the comments, in any language.\n\nMost-liked line wins. 🏆\n\n#penastory #onelineyourturn #writingprompt #shortstory #writersofinstagram")

# ======================= DAILY REEL 18:00 (English, cinematic photo reels) =======================
def reel(day, slug, beats, end, cap, music=0):
    keys = []
    for b in beats + [end]:
        if b[0] not in keys: keys.append(b[0])
    B = [dict({"image": keys.index(b[0]), "text": b[1], "dur": b[2]}, **({"small": b[3]} if len(b) > 3 else {})) for b in beats]
    E = {"image": keys.index(end[0]), "text": end[1], "small": end[2]}
    (S / f"{day}-1800-reel-{slug}.json").write_text(json.dumps({"kind": "reel", "style": "photo", "images": [U(P[k]) for k in keys],
        "beats": B, "end": E, "caption": cap, "music": music}, ensure_ascii=False, indent=1))
TAGS = "#penastory #shortstory #storytelling #readersofinstagram #bookstagramindia"
reel(days[0], "last-customer",
 [("lib", "The bookshop was closing for good.", 3.0, "41 years. Last night."), ("readsun", "At 9 PM, a girl in a school uniform was still in the corner, reading.", 3.6),
  ("lib2", "\"We're closing, beta.\" She didn't look up. \"Can I finish this chapter?\"", 3.8), ("lib3", "At midnight she asked, \"Who decides when a shop's story ends?\"", 3.6),
  ("lib", "Mr. Rao took the closing sign off the door.", 3.4, "Some stories refuse to end.")],
 ("lib2", "Would you have kept it open?", "Pen A Story · a new story every day"),
 f"The bookshop was closing for good. One customer refused to leave. 📚\n\nWould you have kept it open? Tell us 👇\n\n{APP_EN}\n\n{TAGS}")
reel(days[1], "window-seat",
 [("twin1", "Window seat. Hyderabad to Vizag. 12 hours with a stranger.", 3.2), ("tin1", "She wrote in a notebook the whole way. He pretended not to look.", 3.6),
  ("twin2", "Rajahmundry. The bridge. She tore out a page and handed it to him.", 3.6), ("let4", "It was a sketch of him, asleep. Under it: \"You snore. Nice to meet you.\"", 4.0),
  ("st3", "Vizag. She got off. He still has the page. Eleven years now.", 3.4, "Some people stay for one journey. Some stay forever.")],
 ("twin1", "Ever met someone on a train you never forgot?", "Tell us your train story"),
 f"Window seat. 12 hours. A stranger with a notebook. 🚆\n\nEver met someone on a train you never forgot? Tell us 👇\n\n{APP_EN}\n\n{TAGS}", music=1)
reel(days[2], "letter-next-year",
 [("let1", "The letter arrived on a Tuesday.", 2.6), ("let3", "The postmark said next year.", 2.8),
  ("let2", "Inside, in her own handwriting: \"Don't take the job in Pune.\"", 3.6), ("rain2", "She laughed. Then she noticed the coffee stain on the corner.", 3.4),
  ("cofbk2", "The same stain her cup had just left on the table.", 3.2, "Your turn: what happens next?")],
 ("let1", "Write the next line in the comments", "Most-liked line wins 🏆"),
 f"The letter arrived on a Tuesday. It was postmarked next year. ✉️\n\nWrite the next line in the comments. Most-liked line wins 🏆\n\n{APP_EN}\n\n#penastory #writingprompt #onelineyourturn #shortstory #storytelling")
reel(days[3], "power-cut",
 [("diya2", "Power cut. 8 PM. No phones. No Wi-Fi.", 3.0), ("gma3", "Ammamma lit a candle and said, \"Sit. I'll tell you a story.\"", 3.6),
  ("moon", "A king. A clever minister. A moon that followed a boy home.", 3.6), ("diya", "The lights came back at 10. Nobody moved.", 3.2),
  ("gma1", "Best night of the year. And it cost nothing.", 3.2, "Remember those nights?")],
 ("moon2", "Which story did your grandparents tell you?", "Tell us below 🕯️"),
 f"Power cut. No phones. Ammamma's stories. Best night of the year. 🕯️\n\nWhich story did your grandparents tell you? 👇\n\n{APP_EN}\n\n#penastory #childhoodmemories #90skids #storytelling #nostalgia", music=1)
reel(days[4], "margin-notes",
 [("bookrow", "A second-hand book. ₹40. Abids Sunday market.", 3.0), ("openbook", "Someone had written in the margins. Funny notes. Sad ones.", 3.4),
  ("let4", "On the last page: \"If you're reading this, write back.\"", 3.4), ("cofbk", "So she did. And left the book back at the same stall.", 3.2),
  ("market", "Six months later, the book returned. Two new pages of handwriting.", 3.6, "Some friendships start in the margins.")],
 ("bookrow", "Do you write in your books?", "Yes or no? 👇"),
 f"A ₹40 book. Notes in the margins. \"If you're reading this, write back.\" 📖\n\nDo you write in your books? Yes or no 👇\n\n{APP_EN}\n\n{TAGS}")
reel(days[5], "red-pen",
 [("let3", "Every essay I wrote came back covered in red ink.", 3.2), ("clock", "Mrs. D'Souza. Class 9. I hated that red pen.", 3.0),
  ("let2", "Last year I sent her my first published book.", 3.0), ("let1", "She posted it back. Every page marked. In red.", 3.4),
  ("lib3", "On the last page: \"Finally. No corrections. Proud of you.\"", 3.6, "Some teachers never stop teaching.")],
 ("let3", "Tag the teacher who made you a writer", "Tell them today ✍️"),
 f"Every essay came back covered in red ink. Then I sent her my first book. ✍️\n\nTag the teacher who made you who you are 👇\n\n{APP_EN}\n\n#penastory #teachers #writersofinstagram #shortstory #indianauthors", music=1)
reel(days[6], "recipe-book",
 [("kitch", "Amma's recipe book had no measurements.", 3.0), ("kitch2", "\"Salt: enough.\" \"Chilli: depends on Nanna's mood.\"", 3.4),
  ("let2", "After she passed, I tried to cook her rasam. It was never right.", 3.6), ("let3", "Then I found a note on the last page I'd never turned.", 3.0),
  ("kitch", "\"The secret ingredient is: make it for someone you love.\"", 3.6, "It tasted right that night.")],
 ("kitch2", "Which dish tastes like home to you?", "Tell us 🍲"),
 f"Amma's recipe book had no measurements. Just one secret on the last page. 🍲\n\nWhich dish tastes like home to you? 👇\n\n{APP_EN}\n\n{TAGS}")
reel(days[7], "3am-readers",
 [("bedread", "Readers at 3 AM be like:", 2.6), ("bedread2", "\"One more chapter.\"", 2.4),
  ("cofbk", "*Plot twist happens*", 2.4), ("teabk", "\"Okay, now I HAVE to finish it.\"", 2.8),
  ("lib", "Sunrise. Book finished. Zero regrets. Slight regrets.", 3.2)],
 ("bedread", "Tag your 3 AM reading partner", "We see you 😂"),
 f"\"One more chapter\" at 3 AM hits different 😂\n\nTag your 3 AM reading partner 👇\n\n{APP_EN}\n\n#penastory #readermemes #booklovers #bookstagram #readersofinstagram", music=1)
reel(days[8], "thatha-pages",
 [("oldph", "Thatha wrote every night for fifty years.", 3.0, "A story"), ("let4", "Notebooks under the bed. 400 pages. Nobody read them.", 3.4),
  ("gma1", "\"Who reads an old man's stories?\" he said.", 3.0), ("cofbk", "His granddaughter typed them up. One page a night.", 3.2),
  ("lib3", "On his 80th birthday, she handed him a book with his name on the cover.", 3.8, "It's never too late to be an author.")],
 ("let4", "Who in your family should write their story?", "Tag them 👇"),
 f"Fifty years of notebooks under the bed. One granddaughter who typed every page. ✍️\n\nWho in your family should write their story? Tag them 👇 Want to publish your own book? DM us \"AUTHOR\".\n\n{APP_EN}\n\n#penastory #indianauthors #writersofinstagram #shortstory #storytelling")
reel(days[9], "last-letter",
 [("st1", "Platform No. 3. Ten days. One story.", 2.8), ("let1", "A letter from 1998. A sister nobody mentioned.", 3.2),
  ("hills", "A school in the hills of Araku.", 2.8), ("let2", "Twenty-seven letters that were never posted.", 3.0),
  ("diya2", "And one train that should have been missed.", 3.2, "The full serial is on our page.")],
 ("st1", "Season 2? Comment YES", "Platform No. 3 · Pen A Story"),
 f"10 days. One serial. A letter from 1998 that changed a family. 🚉\n\nThe full Platform No. 3 serial is on our page, in Telugu. Want Season 2 in English too? Comment YES 👇\n\n{APP_EN}\n\n#penastory #platformno3 #serialstory #shortstory #storytelling", music=1)
print("EN half written")

# ======================= Pen A Story books at the end of matching stories =======================
def book(name, cover, title, small):
    f = S / f"{name}.json"; d = json.loads(f.read_text()); d["images"].append(f"assets/covers/{cover}"); i = len(d["images"]) - 1
    if d["kind"] == "reel": d["book"] = {"image": i, "text": title, "small": small}
    else: d["slides"].append({"kind": "book", "image": i, "text": title, "small": small})
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1))
book(f"{days[1]}-1800-reel-window-seat", "four-hearts.png", "Four Hearts, One Story", "Vishal Varshney · love, friendship, sacrifice")
book(f"{days[3]}-1800-reel-power-cut", "camera-on-his-shoulder.png", "Camera on His Shoulder", "Jasveer Singh Dangi · the nostalgia our generation carries")
book(f"{days[5]}-1800-reel-red-pen", "unseen-curriculum.jpg", "The Unseen Curriculum", "Vibhuti Vaid · what great teachers teach without a syllabus")
book(f"{days[3]}-1930-story-umbrella", "love-that-lasts.png", "The Secret to Love That Lasts", "Sukanya Biswas · 60 exercises for a stronger relationship")
book(f"{days[1]}-1930-story-tiffin-note", "2min-stories.jpg", "2Min Stories", "Surya Teja · పిల్లలకు నిద్రకు ముందు చిన్న కథలు")
book(f"{days[5]}-1930-story-moon-call", "ramayana.jpg", "Ramayana", "Vamsi Krishna Dasari · అమ్మమ్మ కథలు, పిల్లల కోసం బొమ్మలతో")
book(f"{days[1]}-1630-nostalgia-thirsty-crow", "suns-grove.jpg", "The Rise of Sun's Grove", "Surya Teja · అడవి కథలు, కొత్త తరం కోసం")
book(f"{days[6]}-1630-nostalgia-monkey-crocodile", "2min-stories.jpg", "2Min Stories", "Surya Teja · రెండు నిమిషాల్లో ఒక కథ")
print("books linked")
