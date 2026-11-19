// news-image-20261119: copy the front-page poster to the output path.
//
// The poster (entry.png) is drawn by draw.py and committed in this repo.
// This program only copies it, byte for byte, so both runs write
// identical bytes. Standard library only, no network.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
if (!existsSync(source)) {
  throw new Error(`poster missing: ${source}`);
}
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output/entry.png";
const target = outDir.endsWith(".png")
  ? outDir
  : join(outDir, "entry.png");

mkdirSync(dirname(target), { recursive: true });
copyFileSync(source, target);
console.log(`wrote ${target}`);
