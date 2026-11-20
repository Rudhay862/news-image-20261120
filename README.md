# The World Today — 20 November 2026

One image summing up the world's news of Friday 20 November 2026, built for the
[make.fun](https://make.fun) bounty `news-image-20261120` ($250, top 50 share).

## The image

`entry.png` (1024×1024) is a front page of the day's verified news:

- **Lead:** Trump puts the Iran decision off to 2027 — "no rush", he will "see what
  happens" after 1 January.
- Trump, Putin & Xi issue a joint peace declaration a day after their historic
  three-way summit.
- Houthis strike Riyadh; the sovereign wealth fund's tower is hit.
- Cyclone Akvan: 300,000 evacuated as the storm nears Odisha.
- NASA confirms Voyager 1 passes one light-day from Earth.
- GTA 6 sales pass $1.8bn, beating The Odyssey's global run.
- Europe signals readiness for Ukraine peace talks with Russia.
- Ticker: Hayabusa2's asteroid landing scrapped, US–Venezuela military deal,
  Senegal migrant boat sinking, Van Gogh's record $190.4m sale, Modi meets the
  Prince & Princess of Wales, Nicholls 113* in Wellington.

## How it works

`main.py` copies the bundled `entry.png` to `/output/entry.png` deterministically
(no network), verifying its SHA-256 first. `draw_image.py` is the Pillow program
that drew the image.

## Run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Referral

Try make.fun: https://make.fun/r/xk7vph3j
