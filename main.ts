// news-image-20261119 entrypoint: copy the front-page poster to the output.
//
// The program is deterministic and network-free: it reads entry.png from the
// repository root (next to this file) and writes the exact same bytes to
// /output/entry.png, or to $MAKEFUN_OUTPUT_DIR/entry.png when that is set.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
mkdirSync(outDir, { recursive: true });
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");
copyFileSync(source, target);
console.log(`wrote ${target}`);
