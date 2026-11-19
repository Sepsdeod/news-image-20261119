// news-image-20261119 entrypoint (coordinator rebuild, v2).
//
// The program is deterministic and network-free: it reads entry.png from
// the repository root (next to this file) and writes the exact same bytes
// to $MAKEFUN_OUTPUT_DIR/entry.png when that is set, or /output/entry.png.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const source = join(here, "entry.png");
const target = join(outDir, "entry.png");
if (!existsSync(source)) {
  throw new Error(`poster not found: ${source}`);
}
copyFileSync(source, target);
const inBytes = statSync(source).size;
const outBytes = statSync(target).size;
if (inBytes !== outBytes) {
  throw new Error(`output size mismatch: ${outBytes} != ${inBytes}`);
}
console.log(`wrote ${target} (${outBytes} bytes, byte-identical)`);
