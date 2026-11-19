# Run notes — news-image-20261118 round 2

Entry title: **18 November 2026 — The World's News in One Image**

Round 2 replaces round 1 (text-only programmatic front page). The user asked
for a neater, more attractive version with REAL photos. Editorial + visual
style reference: CNN and Al Jazeera coverage dated 18 Nov 2026 (searched
and read in-session: CNN on Trump landing in Shenzhen, Xi–Putin meeting,
Kerch Bridge collapse; Al Jazeera on the Board of Peace Gaza warning and
Kuwait/Bahrain attacks). No CNN/Al Jazeera photographs are used — all
photos below are freely licensed Wikimedia Commons files.

## Stories chosen (all from Wednesday 18 November 2026, reused from round 1)

| Slot | Story |
|---|---|
| Lead | Trump lands in Shenzhen; Xi and Putin meet a day ahead of the first US–China–Russia three-way talks |
| Card 1 | Iran strikes a US base in Kuwait and sites in Bahrain after US strikes on Qeshm Island |
| Card 2 | Ukraine strikes the Kerch Bridge again; part of the road span collapses |
| Card 3 | Mary Peltola unseats Dan Sullivan in Alaska; Democrats take a 56–44 Senate majority |
| Card 4 | Board of Peace warns the Gaza ceasefire is at risk of collapse |
| Brief | Ebola outbreak in DR Congo passes 11,000 cases |
| Brief | Anthropic raises a record $81.3bn in a stock offering |
| Brief | US loses measles-free status after 26 years |

## Photos (all in `assets/`, attribution also in README + image footer)

| Photo | File | Author | License |
|---|---|---|---|
| Shenzhen skyline (lead) | Skyline of Shenzhen from Hong Kong.jpg | Sparktour | CC BY-SA 4.0 |
| Kuwait Towers | Kuwait Towers2025.jpg | Gladiator2030 | CC BY-SA 4.0 |
| Kerch Bridge | Kerch. Crimean Bridge P5020707 2350.jpg | Alexxx1979 | CC BY-SA 4.0 |
| US Capitol | Capitol Building Full View.jpg | Noclip | Public domain |
| Gaza City | Gaza City.JPG | OneArmedMan | Public domain |

Design: photo-led newspaper front page (`render.py`, Python + Pillow,
DejaVu fonts, written fresh in-session). White page, black serif masthead
"18 NOVEMBER 2026", red kickers, big lead photo, 2×2 photo cards with
place tags, three-item briefs strip, photo-credit footer. Two photos are
region-cropped in code: the Shenzhen panorama is zoomed onto the tower
cluster (also cuts the photographer's watermark at the frame edge) and
the Kuwait shot is zoomed onto the towers.

## Image

- File: `entry.png`
- Dimensions: 1024 x 1024 px
- Size: 738,231 bytes (limit 1,048,576)
- SHA-256: `f30e09549d4b9e3528cc5636500c8c8a4930637ebbb2db9ea199ce28685ae74f`

## Local tests (2026-11-19 ~12:20 WIB)

- `python3 render.py` — rendered cleanly. Image visually checked twice:
  fixed the lead crop (skyline was too distant, watermark visible) and
  zoomed the Kuwait photo (towers too small); re-checked, no overlaps,
  no clipped text, all five photos recognisable.
- `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts` — exit 0,
  `out/entry.png` written, digest printed matches source.
- Ran the program twice (`out` and `out2`): both outputs byte-identical
  (sha256 `f30e0954...85ae74f`), `cmp` clean — deterministic.
- `main.ts` validates PNG magic bytes, the 1 MiB size limit, and (after a
  genuine revision) the IHDR width/height ≤ 1024, and exits non-zero on
  any failure. Negative tests: non-PNG file → exit 1; forged 1024x1280
  IHDR → exit 1.
- PIL verified `out/entry.png`: valid PNG, 1024x1024 RGB, 738,231 bytes.
- README 1,837 bytes (< 4096), carries the 3 live make.fun badges +
  bounty link from the first commit. LICENSE carries
  `SPDX-License-Identifier: MIT`.

## Files in repo

`main.ts`, `package.json`, `entry.png`, `render.py`, `assets/` (5 photos),
`README.md`, `LICENSE`, `.makefun/owner.json`, `run-notes.md`
