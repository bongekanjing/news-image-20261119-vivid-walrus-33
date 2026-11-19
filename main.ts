// make.fun — news-image-20261119. Entry: one 1024x1024 front page for
// Thursday 19 November 2026, drawn ahead of time and shipped as entry.png.
//
// The grader's sandbox has no network and only the standard library, so this
// program draws nothing. It proves the image it ships is legal, then copies it
// to /output/entry.png. Every rule the gate applies to the bytes is applied
// here first, so a bad file fails on this side of the upload rather than
// costing one of the day's three entries.

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { join } from "node:path";

// The limits from RULES.txt, kept as named constants so they read as rules
// rather than as magic numbers buried in a condition.
const MAX_BYTES = 1_048_576;
const MAX_SIDE = 1024;
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const source = new URL("./entry.png", import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error("entry.png is missing from the repository");
}

const bytes = readFileSync(source);
const size = statSync(source).size;

// The rules accept a whole PNG or a whole JPEG and tell them apart by the
// first bytes. This entry ships a PNG; the JPEG branch exists so the message
// names what was actually found if the file is ever swapped.
const looksPng = PNG_MAGIC.every((byte, i) => bytes[i] === byte);
const looksJpeg = bytes[0] === 0xff && bytes[1] === 0xd8;

if (!looksPng && !looksJpeg) {
  throw new Error(
    `entry.png is neither PNG nor JPEG (first bytes ${bytes.subarray(0, 8).toString("hex")})`,
  );
}

if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the ${MAX_BYTES}-byte limit`);
}

// A PNG's width and height live at fixed offsets inside IHDR, which the format
// requires to be the first chunk. Checking them from the header avoids pulling
// in an image library the sandbox may not have.
let width = 0;
let height = 0;

if (looksPng) {
  width = bytes.readUInt32BE(16);
  height = bytes.readUInt32BE(20);

  if (width > MAX_SIDE || height > MAX_SIDE) {
    throw new Error(`entry.png is ${width}x${height}, over ${MAX_SIDE}x${MAX_SIDE}`);
  }

  // "A whole image" means every chunk with its checksum and the data its
  // header describes. Walking the chunk chain catches a truncated copy, and
  // the trailing-byte test catches one with junk appended. Both are the kind
  // of fault a partial download produces.
  let offset = 8;
  let sawHeader = false;
  let sawEnd = false;

  while (offset + 8 <= bytes.length) {
    const length = bytes.readUInt32BE(offset);
    const type = bytes.toString("latin1", offset + 4, offset + 8);

    if (type === "IHDR") sawHeader = true;
    offset += 12 + length; // 4 length + 4 type + data + 4 CRC

    if (type === "IEND") {
      sawEnd = true;
      break;
    }
  }

  if (sawHeader === false) {
    throw new Error("entry.png has no IHDR chunk, so it is not a PNG the gate will read");
  }
  if (sawEnd === false) {
    throw new Error("entry.png stops before its IEND chunk: the file is truncated");
  }
  if (offset !== bytes.length) {
    throw new Error(`entry.png carries ${bytes.length - offset} bytes past IEND`);
  }
}

const digest = createHash("sha256").update(bytes).digest("hex");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

// What shipped, in the log, so the two runs can be compared byte for byte.
console.log(
  `wrote ${target}: ${size} bytes, ${looksPng ? "PNG" : "JPEG"} ` +
    `${width}x${height}, sha256 ${digest.slice(0, 16)}`,
);
