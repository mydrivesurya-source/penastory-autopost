# Pen A Story autopost
Automated Instagram publishing for **@pen_a_story**. This repo is separate from Kya Cheez Hai and shares no tokens, app or files with it.
Claude writes specs, GitHub Actions builds the media and posts through the Instagram Graph API. No laptop needed.

## Daily rhythm (IST)
| Time | Post |
|---|---|
| 10:30 | Story: meme / mood / teaser (real photo) |
| 13:00 | Carousel: **serial**, one continuing story, cliffhanger every day (Series 1: *Platform No. 3*, 21-30 Nov) |
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
