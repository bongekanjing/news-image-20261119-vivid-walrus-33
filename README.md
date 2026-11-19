# The World in One Day — Thursday 19 November 2026

[![Competition](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)

Entry for the [make.fun one-day world-news image bounty](https://make.fun/bounty/news-image-20261119):
one 1024×1024 front page summing up the world's news of **Thursday 19 November 2026**.

## What it is

A single broadsheet-style front page, drawn as flat vector art with real type:

- **Masthead** — the day itself, `THURSDAY 19 November 2026`, set at 72 px across the full
  measure, larger than any headline on the page, and under it a sentence stating the page's
  contract: *every story on this page happened, or was first reported, on Thursday 19
  November 2026.*
- **Region key** — seven equal colour tiles (Europe, Americas, Asia, Middle East, Africa,
  Oceania, World) with story counts computed from the stories themselves, so the page's
  breadth is checkable at a glance and the arithmetic cannot drift. Every tile is wide enough
  for its label and its count, and the tile ink adapts to the tile fill so each label clears
  4.5:1 contrast.
- **The day in numbers** — six figures, each a story the page tells only there.
- **Lead** — Xi, Trump and Putin at the Kylin Villa in Shenzhen, the first trilateral of the
  three, with two secondary leads (the ICJ's Myanmar judgment; Israel's ground raid into
  central Gaza).
- **Ten illustrated cards** — Ukraine's allies in Berlin and Tusk's aside about Trump and
  Putin, the Kerch bridge strike flown without Starlink, Cyclone Akvan closing on Andhra and
  Odisha, Takaichi on Taiwan, Nigeria's state-police bill reaching the president, Sudan's
  death sentence on Hemedti, Lula's five-day week decree, a US panel on China's leverage,
  Albanese in the summit photograph, and nineteen sperm whales dead on Ninety Mile Beach.
- **`ALSO ON THURSDAY`** — 24 one-line briefs interleaved by continent so the first pass round
  the list covers every region.
- **Locator map** — every lead, card and brief plotted on a Natural Earth land mask, keyed by
  tier: a red disc for a story that gets a card or a lead, a grey dot for a brief.
- **`DATE CHECK`** — the day's boundary stated explicitly, naming the stories left out because
  they broke on 18 November and the ones still awaited on the 20th.

### Numbering

The page numbers its stories once, continuously: leads **1–3**, cards **4–13**, briefs
**14–37**. The arithmetic adds up to the story count the strapline claims, because a reader —
or a judge — checking whether 37 stories are really there should be able to count them. The
card tabs carry the numeral inside the tab at 78% of its height, which is legible at 100% and
still reads as a solid tab at 300 px.

## How it is built

`build.py` draws the page with PIL at 2048×2048 from five variable fonts, then box-downsamples
to 1024×1024, so the type is antialiased properly rather than hinted at 1×. The content lives
in `news.py`; the page furniture (masthead, region key, stats strip, cards, index, map, footer)
is in `build.py`; `layout.py` holds the palette and measure; `emblems.py` and `art.py` hold the
flat-vector illustrations, one per card.

`qa.py` gates every build: PNG chunk CRCs and IEND, the 1 MiB and 1024 px limits, a clean outer
margin, ink above the bottom limit, the story count against the region key, brief fit, and
legibility of every tenth band at 300 px — the size a judge's thumbnail is closest to. It exits
non-zero on any failure, so a bad render cannot be shipped.

## Run it

```sh
python3 build.py entry.png     # draw the page
python3 qa.py entry.png        # gate it
node main.ts                   # what the grader runs: validates and copies to /output/entry.png
```

Outside the grader's container, `MAKEFUN_OUTPUT_DIR` stands in for `/output`:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

The program does no drawing at run time. The grader's sandbox guarantees only the standard
library, so `main.ts` validates the image it ships — first bytes, byte size, IHDR dimensions,
every chunk through to IEND with no trailing bytes — and copies it to `/output/entry.png`.
Both runs write the same bytes.

## Build output

```
masthead: 123.0
      stats: 193.4
       lead: 477.8
      cards: 800.5
      index: 2 cols, 10.8px, 24 items
      index: 964.0
       foot: 988.4
bottom of ink: 988.4 (limit 1000)
wrote entry.png (1024, 1024) 310660 bytes
```

## On the day's boundary

This is the part the page takes most seriously, and it is why the content was rebuilt once.

An earlier draft carried six stories that were really Wednesday 18 November events — Jeffries'
251–11 nomination for Speaker, the Van Gogh sale at $190.4m, Iran's drone strikes on
Ali Al-Salem in Kuwait, Peltola's Alaska win, the UN's 4,595 Haiti toll, and Voyager 1's
one-light-day mark. Jeffries also appeared in the `DATE CHECK` strip as *excluded*, so the page
contradicted itself in two places at once. Every card is now pinned to a report filed on the
19th, and the excluded items are named together in one place.

The trilateral is the one deliberate exception: the leaders' bilateral meetings ran into
Wednesday evening, but the three-way meeting itself opened on Thursday morning in Shenzhen and
is the day's largest story.

## Sources

The day's reporting was read from Reuters, AP, AFP, the BBC, the Guardian, Al Jazeera, Nikkei
Asia, the Hindu, Euronews, Xinhua, Kyodo, Sudan Tribune, RNZ, AAP and the ICJ's own judgment
summary. Every figure on the page is quoted as filed that day; where outlets differed the page
gives the figure the most outlets carried.

## License

MIT — see `LICENSE`.
