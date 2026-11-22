# Engineering notes — news-image-20261121 r1

## What this is

A one-page cream newspaper front page for Saturday 21 November 2026,
drawn by `render.py` (PIL) and shipped as a fixed `entry.png` that the
graded program `main.py` copies to the output directory. The design follows
the pattern that won the 20 November board (same 9-component template), with
the execution fixes from the r2 gap study applied: a dark lead panel, big
filled lead art, solid mini-scenes in every secondary panel, only big round
numbers in the ticker, coloured region chips, and briefs with real detail
instead of calendar filler.

## Design decisions

- **Trio lead.** Iran–Bahrain (IRGC strike on al-Riffa/Awali, Bahrain's
  civilian-plant fire, no injuries) + Chapo Isidro (announced Saturday;
  operation Friday night, 11 killed) + Kryvyi Rih (2 killed, 60 wounded,
  double-tap, missiles also landed in Poland). All three were first
  reported on Saturday 21 Nov; the Friday-night events are worded as
  reported/announced on Saturday, never as Saturday events.
- **Dark accents (gap-study E1).** Lead 1 art is navy, lead 3 art is dark
  slate with a red casualty banner, lead 2 is a dark night raid; every
  secondary panel is a solid-colour mini-scene. The page stays cream
  overall.
- **Lead art fills the frame (E2).** Missile arcs + sun + burning horizon;
  helicopter + searchlight + burning roadblocks + CAPTURED stamp; missile
  streak + lit apartment blocks + red banner. No wide empty sky or sea.
- **Ticker (E4).** Only big round numbers: $60,000 · $1.8bn · $7.5bn ·
  69% · $120bn · 400+. No small counts, no odd precision.
- **Region chips (E5).** EUROPE 8 · THE AMERICAS 15 · ASIA-PACIFIC 3 ·
  MIDEAST 7 · WORLD 7 = 40 stories. The Americas count is high because the
  day was US-heavy (markets, FBI, Amazon, Mexico, Brazil, Florida).
- **Briefs (E8).** 27 items, two columns, one dense line each, every item a
  real detail (no observances, no duplication of lead/panel content).
  Items are capped at ~53 characters so each fits one line at 11.5 pt.
- **DATE CHECK.** Six exclusions with dates: Shenzhen summit (19 Nov),
  ICJ Rohingya ruling (19 Nov), Anthropic $83 IPO pricing (19 Nov),
  Russia's overnight Kyiv barrage (19–20 Nov), COP31's scheduled final
  day (20 Nov), BepiColombo's transfer-module separation (3 Sep).
- **Map.** Simplified continent outlines drawn from general geography
  (equirectangular). Pins 1–13; pins 9 and 13 share Washington (FBI + White
  House angles) and are nudged apart; pins 1 and 4 share the Gulf and are
  nudged apart. Caption says positions are approximate.

## Facts verified before drawing (21 Nov 2026, fresh search)

- Bahrain: IRGC targeted al-Riffa and Awali, claimed 2 Patriot radars hit;
  Bahrain: civilian industrial facility hit, fire, no injuries; air
  defences intercepted other attacks (Reuters/Xinhua).
- Chapo Isidro: captured in Guasave Friday night, announced Saturday;
  FBI Top 10; 11 killed (7 gunmen + 4 soldiers); $5m US reward (Reuters,
  AP, CNN, WSJ).
- Kryvyi Rih: 2 killed (boy 7, woman 20), 60 wounded incl. 6 children,
  ~25 apartment buildings damaged, double-tap (AP).
- Poland: 2 Russian missiles + suspected drone came down Friday; Kh-101
  landed ~50 km from the border; Tusk "likely provocation"; Rutte
  "dangerous" (AP).
- Hormuz: tankers Torkel (stern) and Arina (engine room) hit early
  Saturday, no casualties; third tanker hit a mine and caught fire; IRGC
  unveiled a twin-missile launcher; Iran says it downed a US drone over
  Qeshm (UKMTO via AP/TradeWinds).
- Bitcoin: +9% from a $55,130 low (weakest since Sept 2024) back above
  $60,000 (~$60,300); $1.8bn leveraged positions liquidated (CoinDesk).
- BepiColombo: enters Mercury orbit 21 Nov after 8 years; ESA MPO +
  JAXA Mio; insertion 18:24 UTC; science from April 2027 (ESA, Nature).
- COP31: past Friday deadline, no deal Saturday; draft drops fossil fuels
  and the $120bn adaptation target; EU "good deal or no deal" (Reuters).
- Markets: Friday 20 Nov — Nasdaq −5.28% (negative for the year), S&P
  −3.7%, Dow −1.9%, Nvidia −13.8%, Anthropic −9.1% to $88.30; Nikkei and
  Kospi fell 5%+ overnight into Saturday; VIX closed 35.89 (AP/CNN).
  The rout itself is a 20 Nov event, so the panel is framed on Saturday's
  Asian follow-through.
- Zelensky/Trump: Zelensky told CNN (reported Saturday) Putin is "a
  killer" after Trump called him a "friend" in Shenzhen and defended the
  relationship at the White House on Friday (Euronews/AFP).
- Amazon–Decart: FT reported Saturday that Amazon is nearing a ~$7.5bn
  deal; could be announced next week; nothing signed (FT via TradingView).
- Dengue: Wolbachia mosquitoes cut dengue/chikungunya ~69% in a 4-year,
  5,700-child Belo Horizonte trial, reported Saturday (AP).
- FBI NCIC: CNN reported Friday 20 Nov that the FBI is investigating a
  suspected breach of the NCIC database, the second FBI system hit in
  months (Reuters). Included as a panel with no date claim.

## Weaknesses, honestly

- The world map is a simplified outline, not a precise coastline; pins are
  approximate (caption says so).
- Lead 2's helicopter is a stylised silhouette; the searchlight cone is
  subtle at thumbnail size.
- The Friday-night events (Chapo capture, Kryvyi Rih strike, Poland
  incursion, Wall Street rout, FBI report) are Saturday's news only in the
  sense that they were first reported on Saturday; the page words them
  that way, and DATE CHECK names the 19–20 Nov items that were left out.
- The ICJ Rohingya ruling date (19 Nov) is taken from the coordinator's
  brief, not re-verified in a fresh search during this build.

## Measured numbers

- `entry.png`: 1024×1024, 228,875 bytes (limit 1,048,576) — measured after
  the final render.
- `main.py` two-run check: run twice with separate output directories;
  sha256 identical (see `check.py` output).
- Grader-condition rehearsal: repo copied read-only, no network, run as an
  unprivileged user, output directory pre-created as a mount-like dir;
  exit 0 twice with identical bytes (see check.py).
- Region counts sum: 8 + 15 + 3 + 7 + 7 = 40 = 3 leads + 10 panels +
  27 briefs.
