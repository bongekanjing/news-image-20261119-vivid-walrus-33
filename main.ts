// Entry for make.fun/news-image-20261119 — "Thursday 19 November 2026".
//
// The page is drawn ahead of time by build.py (Python, PIL, five variable fonts)
// at 2048x2048 and box-downsampled to 1024x1024, then shipped here as entry.png.
// The grader's sandbox guarantees only the standard library, so this program does
// no drawing: it checks the image is exactly what the rules allow and copies it
// to /output/entry.png.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1_048_576;
const MAX_SIDE = 1024;

const src = new URL('./entry.png', import.meta.url);
const dstDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dst = join(dstDir, 'entry.png');

const bytes = readFileSync(src);
const size = statSync(src).size;

// PNG or JPEG, told apart by the first bytes.
const isPng = bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47;
const isJpeg = bytes[0] === 0xff && bytes[1] === 0xd8;
if (!isPng && !isJpeg) throw new Error('entry.png is neither PNG nor JPEG');
if (size > MAX_BYTES) throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);

// Read the pixel size out of the IHDR chunk so a wrong-sized render fails loudly
// here rather than at the gate.
if (isPng) {
  const w = bytes.readUInt32BE(16);
  const h = bytes.readUInt32BE(20);
  if (w > MAX_SIDE || h > MAX_SIDE) {
    throw new Error(`entry.png is ${w}x${h}, over the ${MAX_SIDE}x${MAX_SIDE} limit`);
  }
  // The gate wants a whole file: every chunk through to IEND. A truncated copy
  // would otherwise be uploaded and refused, wasting one of the day's entries.
  let i = 8;
  let sawHeader = false;
  let sawEnd = false;
  while (i + 8 <= bytes.length) {
    const len = bytes.readUInt32BE(i);
    const type = bytes.toString('latin1', i + 4, i + 8);
    if (type === 'IHDR') sawHeader = true;
    i += 12 + len;
    if (type === 'IEND') { sawEnd = true; break; }
  }
  if (!sawHeader) throw new Error('entry.png has no IHDR chunk');
  if (!sawEnd) throw new Error('entry.png is truncated: no IEND chunk');
  if (i !== bytes.length) throw new Error(`entry.png has ${bytes.length - i} trailing bytes`);
}

// The entries are what the judge sees, so record what shipped.
import { createHash } from 'node:crypto';
const digest = createHash('sha256').update(bytes).digest('hex');

mkdirSync(dstDir, { recursive: true });
copyFileSync(src, dst);

console.log(`wrote ${dst}: ${size} bytes, ${isPng ? 'PNG' : 'JPEG'}, sha256 ${digest.slice(0, 16)}…`);
