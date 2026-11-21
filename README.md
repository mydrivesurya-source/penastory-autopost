# Pen A Story autopost
Automated Instagram publishing for **@pen_a_story**. This repo is separate from Kya Cheez Hai and shares no tokens, app or files with it.
Claude writes specs, GitHub Actions builds the media and posts through the Instagram Graph API. No laptop needed.

## Daily rhythm (IST)
| Time | Post |
|---|---|
| 10:30 | Story: meme / mood / teaser (real photo) |
| 13:00 | Carousel: **serial**, one continuing story, cliffhanger every day (Series 1: *Platform No. 3*, 20-29 Nov) |
| 18:00 | **Reel** (English): cinematic photo reel, a complete micro-story, often ending on a real Pen A Story book |
| 16:30 | Carousel rotation: **nostalgia** (Panchatantra, Tenali, Akbar-Birbal, Chandamama-style, retold), **reader memes**, **story quiz**, **author call-out**, **One Line. Your Turn.** |
| 19:30 | Carousel: **standalone**, a complete short story in one post |
| 21:30 | Story: tomorrow's serial teaser |

Look: real photography (Unsplash, free licence), soft film grade, Telugu + English mixed in natural speech, minimal text low on the frame, small logo. No coloured template cards.
Plans live in `scripts/plan_*.py` (they write specs). Nothing from hold/ is ever published.

## Standing rules
- Value first: hook → story or problem → why it matters → book → soft CTA. Never just "buy".
- Pen A Story logo on every asset. Real book covers only; never AI-draw a cover.
- **Never use the Winternight or Limitless covers**: they show other publishers' books (*The Bear and the Nightingale* by Katherine Arden; a Robert J. Crane title).
- Max 5 hashtags (Instagram's limit). Never pitch "less screen time" (it's an eBook app).
- Music in reels is synthesised in `render.py` (original, copyright-free). Trending audio can't be added through the API.
- Don't change posts that are already queued; add new ones around them.

## Layout
- `specs/YYYY-MM-DD-HHMM-<slug>.json`: one post per file (IST date and time). See the docstring in `scripts/build.py` for kinds: carousel, reel, story, image, video.
- `inbox/`: videos Surya shares. A `video` spec turns one into a 9:16 reel with the logo, keeping its original audio.
- `scripts/render.py` (design + reel engine), `build.py` (specs → media + queue), `publish.py` (Graph API).
- Workflows: `publish.yml` (build on push, publish when dispatched), `keeper.yml` (fires publish every 10 min, 10:00–22:30 IST), `check.yml` (token check, lists the IG user ID).

## Setup state
- Secret `IG_TOKEN`: Pen A Story page token with instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement.
- Variable `IG_USER_ID`: the pen_a_story Instagram business account ID (run `check.yml` to see it).

## Pen A Story books (real covers in assets/covers)
The Unseen Curriculum (Vibhuti Vaid) · Camera on His Shoulder (Jasveer Singh Dangi) · Four Hearts, One Story (Vishal Varshney) · Ramayana (Vamsi Krishna Dasari) · The Secret to Love That Lasts (Sukanya Biswas) · 2Min Stories (Surya Teja) · The Rise of Sun's Grove (Surya Teja) · ఈ 21వ శతాబ్దపు కొత్త రాజకీయ నీతి (Kanagiri SN Prasad).
A story ends on a book only where the theme genuinely matches. Never claim a book is free.

## Serials
- **#1 Platform No. 3** (Telugu, 10 eps, 20-29 Nov). Finale 29 Nov.
- **#2 The Second Key** (English, 8 eps, 30 Nov - 7 Dec, 13:00). Ananya (29, Bangalore) comes to sell her late ammamma's house in Hyderabad's Old City.
  Ep1 (30 Nov): brass key between pages 88-89 of ammamma's last book, note "Not for the doors you can see"; 11 doors, the key fits none.
  Planned arc: Ep2 neighbour Jaffer uncle (photo tin2, already teased): "Your ammamma's house had twelve doors" — one was plastered over in 1984.
  Ep3 behind the wall upstairs: a tiny room, a desk, a typewriter, letters to publishers signed "Sitara", all rejections. Ep4 a locked trunk the key opens:
  a finished novel, 1984, never published; note "Read the last chapter first." Ep5 the last chapter is about a daughter who left home (Ananya's mother).
  Ep6 Ananya calls her mother; the mother knew nothing about the novel. Ep7 Ananya cancels the sale. Ep8 finale: the book gets its first reader —
  her mother, reading it aloud in the twelfth room. (Keep it fiction; never present it as a real Pen A Story publication.)
- Next serial (#3, from 8 Dec) is Telugu; pick genre from the stats.

## Learnings (virality decision log)
- **20 Nov** — Day 1 of the system. 6 posts live (library-card standalone, AM story, Platform No. 3 ep1, reader memes 1, reel last-customer, auto-library standalone).
  No stats yet: the first nightly `stats.py` run happens after 21:40 IST today, so status/stats.json did not exist at review time.
  Decision: no changes; 30 Nov written on the standing mix (serial #2 English, Telugu nostalgia/standalone, English reel). First real review on 21 Nov.
- **21 Nov** — Review on the latest stats (20 Nov 21:47 IST; the 21 Nov nightly run had not happened yet). 5 system posts measured, all <1 day old.
  Won: the reel (last-customer) reached 35 vs 7-16 for the carousels (reels get 2-5x distribution). Weak: its avg watch was 2.2 s, so viewers leave in beat 1.
  Account history: big hits were Telugu + emotional/tribute (teacher tribute 26 shares; Telugu cyclist 4.5k interactions).
  Change (from 1 Dec): reel beat 1 is a 2.8 s, under-8-word hook; no format cut or boosted yet (<5 posts per format). 1 Dec written; quiz #2 answer pre-written for 2 Dec 10:30.
