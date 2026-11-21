[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/dhosmatullah/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/dhosmatullah/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — 20 November 2026

A front-page style collage that sums up the world news of **Friday
20 November 2026** in a single 1024×1024 image. `main.py` (Python 3,
standard library only, no network) draws the whole page procedurally —
masthead, hero story, four panel stories, a climate strip and a news
ticker — with a built-in 5×7 bitmap font and a hand-rolled PNG encoder,
and writes it to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).
Output is deterministic: 20,113 bytes, well under the 1 MiB gate.

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## The stories shown (all events of / first reported on 20 Nov 2026)

1. **Russia fires 400+ drones & 110 missiles at Ukraine** — Kyiv bridges
   and power infrastructure hit, 8 killed; Russian missiles fell inside
   Poland (NATO). Figures as reported by President Zelensky.
2. **Shenzhen summit** — Trump, Xi and Putin meet face to face; the US,
   China and Russia issue a joint declaration that nuclear war must never
   be fought, but reach no arms-control deal.
3. **ICJ rules Myanmar committed genocide against the Rohingya** — the
   World Court's ruling on the 2017 crimes in Rakhine State, with
   reparations ordered; Myanmar rejects the ruling.
4. **Anthropic's $81bn record IPO** — the largest stock-market debut in
   history, reported by Reuters.
5. **UK & EU strike a reset deal in Brussels** — post-Brexit package
   including 100,000 youth-mobility visas a year each way, eased food
   trade and linked carbon markets.
6. **COP31 final day in Antalya** — climate talks end without a deal
   after fossil-fuel phase-out language is dropped from the draft.
7. Ticker: Haitian police kill 34 gang members; Cyclone Akvan makes
   landfall in Odisha, India; Iraqi forces enter Jurf al-Sakhar under a
   militia deal.

## Sources

Researched on 21 November 2026 from that day's reporting and cross-checked
across at least two independent roundups per story:

- Reuters, 20 Nov 2026 — Morning Bid "AI's tough crowd" (Anthropic IPO,
  UK–EU reset); Reuters Open Interest weekly (Shenzhen meeting, Anthropic).
- Open Chronicle, "Global News Brief, November 20, 2026"
  (openchronicle.org) — Shenzhen declaration, ICJ Myanmar ruling, Kyiv
  attacks, EU–UK Brussels summit, Haiti.
- "Meanwhile in Ukraine" daily summary, 20 Nov 2026 (Patreon) — barrage
  scale (400+ drones, 110 missiles, 8 killed), missiles in Poland.
- Informed Clearly, "Daily News Summary – 2026-11-20"
  (informedclearly.com) — Anthropic $81bn IPO.
- PANA / Panapress, 20 Nov 2026 — COP31 Antalya final day.
- Global Affairs News and 24 International video roundups, 20 Nov 2026 —
  ICJ ruling, COP31 deadlock, UK–EU youth mobility (100k/yr), Cyclone
  Akvan landfall, Haiti police operation.

## License

MIT — see `LICENSE`.
