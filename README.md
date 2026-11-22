# Saturday 21 November 2026 — The World in One Day

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/besan11/news-image-20261121-r1-local/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/besan11/news-image-20261121-r1-local/reward.svg)](https://make.fun/c/news-image-20261121)

One front page that sums up Saturday 21 November 2026: Iran's missile-and-drone
strike on US positions at two bases in Bahrain, Mexico's capture of FBI Top 10
fugitive "Chapo Isidro", and the Russian missile strike on Kryvyi Rih — plus
37 more stories, from the tankers hit in the Strait of Hormuz to Bitcoin's
bounce back above $60,000 and BepiColombo's arrival at Mercury. 40 stories in
all, every figure checked against fresh reporting (Reuters, AP, AFP, CNN, FT,
ESA, CoinDesk) before drawing. The page is a cream newspaper front page:
giant serif date, red italic sub-dek, six-number stats ticker, coloured region
chips, three leads with big filled art, ten secondary panels as solid
mini-scenes, a numbered world map, two-column briefs, a DATE CHECK box naming
what was first reported 19–20 Nov and is therefore not on the page, and a
one-day assertion footer.

## How it works

- `render.py` draws `entry.png` (1024×1024, under 1 MiB) with PIL from the
  story data at the top of the file. No network, no input besides the DejaVu
  fonts in `fonts/`.
- `main.py` (Python 3.13, standard library only) is the entry program the
  grader runs: it copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` and
  verifies the PNG magic bytes and the 1 MiB cap. It never deletes the output
  directory or its contents, so it is safe when the output directory is a
  bind mount; both runs write identical bytes.

## Run it

```sh
python3 render.py            # rebuild entry.png from the story data
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # entry program
python3 check.py             # self-check: gate limits + two-run identity
```

## Files

- `entry.png` — the entry image (the deliverable)
- `render.py` — the renderer (PIL; local use only, not run by the grader)
- `main.py` — the graded entry program (stdlib only)
- `check.py` — self-check script
- `fonts/` — DejaVu Sans / DejaVu Serif TTFs used by the renderer
- `NOTES.md` — engineering notes: design decisions, measured numbers, limits

Referral code: `jpgk45b3` — https://make.fun/r/jpgk45b3
