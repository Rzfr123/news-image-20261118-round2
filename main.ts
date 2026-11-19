// news-image-20261118 round 2 entrypoint (Node 22, standard library only).
// The image is rendered offline by render.py and committed as entry.png;
// this program copies it to the output directory and validates it first.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576; // 1 MiB, the competition limit

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const dest = join(outDir, 'entry.png');

let bytes: Buffer;
try {
  bytes = readFileSync(source);
} catch {
  fail(`cannot read ${source}`);
}

if (bytes.subarray(0, 8).compare(PNG_MAGIC) !== 0) {
  fail('entry.png does not start with PNG magic bytes');
}
if (bytes.length > MAX_BYTES) {
  fail(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
// The first chunk of a PNG must be IHDR: 4-byte length, 'IHDR', then
// 4-byte big-endian width and height. Reject anything that is not a
// whole 1024x1024-or-smaller image.
if (bytes.length < 33 || bytes.subarray(12, 16).toString('latin1') !== 'IHDR') {
  fail('entry.png has no IHDR chunk where one belongs');
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width === 0 || height === 0 || width > 1024 || height > 1024) {
  fail(`entry.png is ${width}x${height}, over the 1024x1024 limit`);
}

mkdirSync(outDir, { recursive: true });
try {
  copyFileSync(source, dest);
} catch {
  fail(`cannot write ${dest}`);
}

const written = statSync(dest).size;
if (written !== bytes.length) {
  fail(`wrote ${written} bytes, expected ${bytes.length}`);
}
const sha256 = createHash('sha256').update(bytes).digest('hex');
console.log(`entry.png: ${bytes.length} bytes sha256=${sha256}`);
