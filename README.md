# The World — Tuesday, 24 November 2026

A newspaper front page summing up the world news of Tuesday, 24 November 2026, built for the make.fun bounty `news-image-20261124`.

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dedenabduloh07-ctrl/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dedenabduloh07-ctrl/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

## The image

A front page of **THE WORLD**, dated Tuesday, 24 November 2026. Stories covered:

- **Tech on trial** — a US jury convicts Huawei on 10 of 12 counts, including conspiracy to steal trade secrets and bank fraud; sentencing set for September 2027.
- **Hormuz** — four tankers hit naval mines in the Strait of Hormuz and catch fire; Tehran orders the strait closed day by day.
- **War at sea** — Ukrainian drones strike a Russian cargo ship in the Gulf of Finland and a corvette off Libya.
- **Justice** — the World Court finds Myanmar guilty of genocide against the Rohingya.
- **Markets** — Nvidia brings back Jensen Huang as chief executive; shares jump about 30% and Wall Street posts its best day in over a year.
- **Sport** — Senegal regain the Africa Cup of Nations title.
- **Markets strip** — Wall Street's best day in over a year; Sanofi agrees to buy Insmed for $41bn.
- **In brief** — helicopter crash near Eskisehir, hostages in Cartagena, drone strike on Riyadh's PIF tower, Indonesia's vice-presidential candidates, US measles elimination status, Gaza meningitis alert, Hasina's planned return, Hanoi restaurant blast.

All stories were first reported on Tuesday, 24 November 2026.

## How to run

```sh
python3 main.py
```

This copies `entry.png` to `/output/entry.png` (or to `$MAKEFUN_OUTPUT_DIR/entry.png` when that variable is set) and prints the destination path and byte size. Python standard library only; no network access.

## Reproducing the image

`build_image.py` draws the front page from scratch with Pillow and saves `entry.png` (1024×1024). Run it with:

```sh
python3 build_image.py
```

## License

MIT — see [LICENSE](LICENSE).
