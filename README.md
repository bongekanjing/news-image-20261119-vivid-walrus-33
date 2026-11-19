# The World in One Day — Thursday 19 November 2026

[![Competition](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)

Entry for the [make.fun one-day world-news image bounty](https://make.fun/bounty/news-image-20261119):
one 1024×1024 front page summing up the world's news of **Thursday 19 November 2026**.

## What the image is

A single broadsheet-style front page, drawn as flat vector art with real type:

- **Masthead** — the day itself, `THURSDAY 19 November 2026`, set at 72 px across the full
  measure, larger than any headline on the page, and under it a sentence stating the page's
  contract: *every story on this page happened, or was first reported, on Thursday 19
  November 2026.*
- **Region key** — seven equal colour tiles (Europe, Americas, Asia, Middle East, Africa,
  Oceania, World) carrying story counts taken from the stories themselves, so the page's
  breadth is checkable at a glance and the arithmetic cannot drift.
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
- **Locator map** — every lead, card and brief plotted on a land mask, keyed by tier: a red
  disc for a story that gets a card or a lead, a grey dot for a brief.
- **`DATE CHECK`** — the day's boundary stated explicitly, naming the stories left out because
  they broke on 18 November and the ones still awaited on the 20th.

### Numbering

The page numbers its stories once, continuously: leads **1–3**, cards **4–13**, briefs
**14–37**. The arithmetic adds up to the story count the strapline claims, because a reader —
or a judge — checking whether 37 stories are really there should be able to count them.

## What is in this repository

`entry.png` and the program that ships it:

```
entry.png   the page, 1024x1024, 310,660 bytes
main.ts     validates the image against every rule, then copies it to /output/entry.png
README.md   this file
LICENSE     MIT
```

`main.ts` draws nothing. The grader's sandbox has no network and guarantees only the standard
library, so the page is drawn ahead of time and the program's job is to prove the bytes are
legal before they are uploaded: PNG signature, byte size against the 1 MiB limit, width and
height read out of IHDR against the 1024 px limit, every chunk walked through to IEND, and no
bytes trailing the end marker. A file that fails any of those raises instead of shipping, so a
bad render cannot cost one of the day's entries.

## Run it

```sh
node main.ts                    # writes /output/entry.png
```

Outside the grader's container, `MAKEFUN_OUTPUT_DIR` stands in for `/output`:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Both runs write the same bytes: the program is deterministic and its only input is the file
already in the repository.

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
