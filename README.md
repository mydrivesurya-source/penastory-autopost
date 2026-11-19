# Pen A Story autopost
Automated Instagram publishing for **@pen_a_story**. This repo is separate from Kya Cheez Hai and shares no tokens, app or files with it.
Claude writes specs, GitHub Actions builds the media and posts through the Instagram Graph API. No laptop needed.

## Daily rhythm (IST)
| Time | Post | Notes |
|---|---|---|
| 10:30 | Story | teaser for the day's reel or a puzzle answer |
| 13:00 | Carousel | **Six Frames**: a complete short story in 6 book pages, daily. Sun = *One Line. Your Turn.* Tue = *Solve the Case* |
| 19:30 | Reel | kinetic story reel ending on the real book cover, or a video Surya shared |
| 21:30 | Story | reshare of the day's reel |

Language mix: about 50% Telugu, 50% English. Telugu real-story reels are the account's proven winners (Indian Cyclist Telugu: 23K–112K views vs ~300–1,400 for designed announcement reels, Nov 2026).

## Standing rules
- Value first: hook → story or problem → why it matters → book → soft CTA. Never just "buy".
- Pen A Story logo on every asset. Real book covers only; never AI-draw a cover.
- **Never use the Winternight or Limitless covers**: they show other publishers' books (*The Bear and the Nightingale* by Katherine Arden; a Robert J. Crane title).
- Max 5 hashtags (Instagram's limit). Never pitch "less screen time" (it's an eBook app).
- Music in reels is synthesised in `render.py` (original, copyright-free). Trending audio can't be added through the API.
- Look: editorial book-page design. Cream paper pages, Playfair Display + Lato, Noto Serif Telugu, one deep colour per episode, gold inset frame.
- Don't change posts that are already queued; add new ones around them.

## Layout
- `specs/YYYY-MM-DD-HHMM-<slug>.json`: one post per file (IST date and time). See the docstring in `scripts/build.py` for kinds: carousel, reel, story, image, video.
- `inbox/`: videos Surya shares. A `video` spec turns one into a 9:16 reel with the logo, keeping its original audio.
- `scripts/render.py` (design + reel engine), `build.py` (specs → media + queue), `publish.py` (Graph API).
- Workflows: `publish.yml` (build on push, publish when dispatched), `keeper.yml` (fires publish every 10 min, 10:00–22:30 IST), `check.yml` (token check, lists the IG user ID).

## Setup state
- Secret `IG_TOKEN`: Pen A Story page token with instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement.
- Variable `IG_USER_ID`: the pen_a_story Instagram business account ID (run `check.yml` to see it).
