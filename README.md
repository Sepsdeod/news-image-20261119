# The World in One Day — Thursday 19 November 2026

[![news-image-20261119](https://img.shields.io/badge/make.fun-news--image--20261119-blue)](https://make.fun/c/news-image-20261119)
[![date](https://img.shields.io/badge/day-Thursday%2019%20November%202026-gold)](https://make.fun/c/news-image-20261119)
[![image](https://img.shields.io/badge/image-1024%C3%971024%20PNG-green)](./entry.png)
[![license](https://img.shields.io/badge/license-MIT-lightgrey)](./LICENSE)

A front-page poster summing up the world's news of **Thursday 19 November 2026** in one image.

## The day's stories

- **Grand Theft Auto VI is here** — after 13 years, Rockstar's sequel unlocks at midnight around the world; about 17 million copies already sold for $1.65 billion, critics score it 99/100.
- **Jeffries set to make history** — Democrats nominate Hakeem Jeffries for Speaker; he would be the first Black Speaker of the US House.
- **World Court rules today** — the ICJ delivers its judgment in The Gambia v. Myanmar, on whether Myanmar committed genocide against the Rohingya.
- **Cyclone Akvan bears down** — the storm is set to cross India's east coast between Machilipatnam and Puri.
- **EU plans a €45bn Ukraine loan** — Brussels proposes a loan to cover Kyiv's budget gap, to be repaid once Russia pays reparations.
- **Voyager 1 reaches one light-day from Earth**, and **Trump, Xi and Putin meet in Shenzhen**.

## How it works

`draw.py` draws the poster from scratch with Pillow (original vector-style artwork — no photographs, no copied images) and saves it as `entry.png` (1024×1024, under 1 MiB). `main.ts` (Node 22, standard library only, no network) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`), so both runs write identical bytes.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](./LICENSE).
