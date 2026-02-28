# SOMPT22 — Benchmark Website

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-brightgreen)](https://sompt22.github.io)

Website and automated benchmark challenge platform for the **SOMPT22: A Surveillance Oriented Multi-Pedestrian Tracking Dataset**.

> Simsek, F.E., Cigla, C., Kayabol, K. — [arXiv:2208.02580](https://arxiv.org/abs/2208.02580)

---

## Site Structure

| Page | URL | Description |
|------|-----|-------------|
| Home | `/` | Dataset overview, paper, statistics |
| Challenge | `/challenge/` | Submission guide, format, rules |
| Leaderboard | `/leaderboard/` | Live rankings, sortable by any metric |
| Blog | `/blog/` | News and updates |

---

## Benchmark Challenge System

Participants submit tracking results via GitHub Issues. Evaluation is fully automated via GitHub Actions.

### How It Works

```
Participant opens a GitHub Issue (Benchmark Submission template)
        │
        ▼
GitHub Actions workflow triggers (evaluate_submission.yml)
        │
        ├── Parses issue body (team, tracker, results URL, FPS, ...)
        ├── Downloads results .zip from participant's public link
        ├── Clones private GT repo (via GT_REPO_TOKEN secret)
        ├── Runs evaluate_submission.py (TrackEval / motmetrics)
        │       └── Computes: HOTA, DetA, AssA, MOTA, IDF1, FP, FN, IDs
        ├── Posts results table as a comment on the issue
        ├── Updates _data/leaderboard.json and commits to main
        └── Labels issue as "accepted"
```

### Key Files

```
.github/
├── ISSUE_TEMPLATE/
│   └── submission.yml          ← structured submission form
└── workflows/
    └── evaluate_submission.yml ← evaluation pipeline

scripts/
└── evaluate_submission.py      ← Python evaluation script (HOTA/MOTA/IDF1)

_data/
└── leaderboard.json            ← auto-updated leaderboard data

leaderboard.md                  ← leaderboard page (reads leaderboard.json)
challenge.md                    ← challenge instructions page
_layouts/leaderboard.html       ← wide layout for leaderboard table
```

---

## Setup: Required GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|--------|-------------|
| `GT_REPO_TOKEN` | Personal Access Token with `repo` scope for the private GT repository |
| `GT_REPO` | Private repo containing test GT, e.g. `sompt22/sompt22-gt-private` |

### Private GT Repository Structure

The GT repository must follow the MOT Challenge directory layout:

```
test/
├── SOMPT22-01/
│   └── gt/
│       └── gt.txt
├── SOMPT22-02/
│   └── gt/
│       └── gt.txt
└── ...
```

---

## Submission Format

Results must be in **MOT Challenge format** — one `.txt` file per test sequence:

```
# frame, id, bb_left, bb_top, bb_width, bb_height, conf, x, y, z
1, 1, 584, 408, 48, 152, 1, -1, -1, -1
1, 2, 731, 392, 55, 143, 1, -1, -1, -1
```

Participants zip the result files and upload to a public host (Google Drive, Dropbox, etc.), then open a [Benchmark Submission issue](../../issues/new?template=submission.yml).

---

## Leaderboard

Rankings are sorted by **HOTA** (primary metric). The leaderboard table supports:
- Column sorting (click any header)
- Live search by team / tracker / affiliation
- Gold / silver / bronze row highlighting for top-3

`_data/leaderboard.json` is committed automatically after each accepted submission. Jekyll rebuilds the static site on every push.

---

## Local Development

```bash
bundle install
bundle exec jekyll serve
```

Site available at `http://localhost:4000`.

---

## Evaluation Script

`scripts/evaluate_submission.py` uses [TrackEval](https://github.com/JonathonLuiten/TrackEval)
(latest version, installed from GitHub source).

| Metric group | Metrics |
|---|---|
| HOTA | HOTA, DetA, AssA (mean over α = 0.05 … 0.95) + per-alpha values |
| CLEAR | MOTA, MOTP |
| Identity | IDF1, IDP, IDR |
| Counts | FP, FN, IDSW, MT, ML |

TrackEval's built-in preprocessor filters distractor annotations (`conf=0` in GT)
before computing metrics, consistent with the MOT Challenge evaluation protocol.

```bash
python scripts/evaluate_submission.py \
    --gt_dir   /path/to/test_gt \
    --pred_dir /path/to/results \
    --output   eval_results.json
```

---

## Citation

```bibtex
@misc{simsek2022sompt22,
  doi    = {10.48550/ARXIV.2208.02580},
  url    = {https://arxiv.org/abs/2208.02580},
  author = {Simsek, Fatih Emre and Cigla, Cevahir and Kayabol, Koray},
  title  = {SOMPT22: A Surveillance Oriented Multi-Pedestrian Tracking Dataset},
  year   = {2022}
}
```

---

## License

Dataset annotations: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0).
Dataset videos: available for non-commercial research only.
Website code: MIT.
