// Entry program for "Sum up 19 November's world news in one image".
//
// The picture itself is entry.png, drawn ahead of time by draw.py and kept
// in this repository. The program's whole job is to place those exact bytes
// at <output>/entry.png, where the output directory is the one the harness
// names: MAKEFUN_OUTPUT_DIR when set, /output otherwise. It runs twice and
// must write the same bytes both times, which copying a fixed file does by
// construction. Node standard library only; no network.

import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

function main(): void {
  const src = statSync(source);
  if (!src.isFile() || src.size === 0) {
    throw new Error(`entry image missing or empty: ${source}`);
  }
  if (src.size > 1048576) {
    throw new Error(`entry image over the 1 MiB cap: ${src.size} bytes`);
  }
  const magic = readFileSync(source).subarray(0, 8);
  const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  if (!magic.equals(pngMagic)) {
    throw new Error("entry image does not start with the PNG signature");
  }
  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, target);
  const written = statSync(target).size;
  if (written !== src.size) {
    throw new Error(`copy short: wrote ${written} of ${src.size} bytes`);
  }
  console.log(`entry.png: ${written} bytes -> ${target}`);
}

try {
  main();
} catch (err) {
  console.error(err instanceof Error ? err.message : String(err));
  process.exit(1);
}
