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
  her mother, reading it aloud in the twelfth room.
  Written so far: Ep4 (3 Dec) — trunk opens, 400-page novel titled *The Second Key* (1984), Sitara = ammamma (Rukmini);
  page one says "Read the last chapter first"; the last chapter is called "Lakshmi" = Ananya's mother. Ep5 teaser: 1984, night train to Bangalore. (Keep it fiction; never present it as a real Pen A Story publication.)
- Next serial (#3, from 8 Dec) is Telugu; pick genre from the stats.

## Learnings (virality decision log)
- **20 Nov** — Day 1 of the system. 6 posts live (library-card standalone, AM story, Platform No. 3 ep1, reader memes 1, reel last-customer, auto-library standalone).
  No stats yet: the first nightly `stats.py` run happens after 21:40 IST today, so status/stats.json did not exist at review time.
  Decision: no changes; 30 Nov written on the standing mix (serial #2 English, Telugu nostalgia/standalone, English reel). First real review on 21 Nov.
- **21 Nov** — Review on the latest stats (20 Nov 21:47 IST; the 21 Nov nightly run had not happened yet). 5 system posts measured, all <1 day old.
  Won: the reel (last-customer) reached 35 vs 7-16 for the carousels (reels get 2-5x distribution). Weak: its avg watch was 2.2 s, so viewers leave in beat 1.
  Account history: big hits were Telugu + emotional/tribute (teacher tribute 26 shares; Telugu cyclist 4.5k interactions).
  Change (from 1 Dec): reel beat 1 is a 2.8 s, under-8-word hook; no format cut or boosted yet (<5 posts per format). 1 Dec written; quiz #2 answer pre-written for 2 Dec 10:30.
- **22 Nov** — Review on the latest stats (21 Nov 21:49 IST; the 22 Nov nightly run had not happened yet). 9 system posts measured.
  Won: serial ep1 (3.0, reach 28), reel last-customer (3.0, reach 85), library-card standalone (2.5). Weak: tiffin-note standalone (1.1, reach 6),
  thirsty-crow nostalgia (1.3), reel window-seat (1.6 — but avg watch rose to 3.5 s from 2.3 s, so the short hook helps).
  Every post so far: 0 shares, 0 saves, 0 comments. Reels reach 3-5x carousels. Telugu carousels median 2.15 vs English posts 1.8. No format has 5+ posts yet.
  Change (from 2 Dec): every caption gets one concrete "send this to <specific person>" line (shares are the gap); reels keep the <=8-word 2.8 s hook
  and add a twist in the final beat. Mix and 50/50 language split unchanged. Next check: if reels keep 3x reach through 29 Nov, add a 2nd daily reel from 30 Nov+.
- **23 Nov** — Review on the latest stats (22 Nov 21:41 IST; the 23 Nov nightly run had not happened yet). 13 system posts measured; compared at equal age
  across the 3 snapshots because raw scores punish posts <9 h old. Won: reels (reach 35-45 at 4 h, 85-107 at 28 h, 3-6x carousels; median 2.2), serial ep1 (3.1).
  Weak: serial reach falling episode to episode (16 -> 13 -> 11 at 9 h), One Line ep1 and nostalgia (1.3 at 5 h vs memes 1.8), Telugu standalones tiffin/cricket (1.1-1.3).
  Still 0 shares / 0 saves / 0 comments on every post; still no format with 5+ posts, so nothing cut.
  Change (3 Dec): serial slide 1 = one-line "Previously" recap; 19:30 Telugu standalone told as a Telugu photo reel (test: if it beats the Telugu carousel
  median, 19:30 alternates reel/carousel); 16:30 picks memes. Renderer: new per-slide "shade" to darken bright photos (QC kept failing on bright frames).
  Followers flat: 461 -> 460 -> 460.
