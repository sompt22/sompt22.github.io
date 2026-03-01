# SOMPT22: A Surveillance Oriented Multi-Pedestrian Tracking Dataset

[![Website](https://img.shields.io/badge/Website-sompt22.github.io-blue)](https://sompt22.github.io)
[![Challenge](https://img.shields.io/badge/Benchmark-Challenge-orange)](https://sompt22.github.io/challenge/)
[![Leaderboard](https://img.shields.io/badge/Leaderboard-live-green)](https://sompt22.github.io/leaderboard/)
[![Paper](https://img.shields.io/badge/arXiv-2208.02580-red)](https://arxiv.org/abs/2208.02580)

**Fatih Emre Simsek**<sup>1,2</sup> · **Cevahir Cigla**<sup>1</sup> · **Koray Kayabol**<sup>2</sup>

<sup>1</sup> Aselsan Inc. · <sup>2</sup> Gebze Technical University

---

## Overview

SOMPT22 is a multi-pedestrian tracking dataset captured from **static surveillance cameras** in outdoor city environments. It provides dedicated benchmarking for surveillance-focused MOT scenarios, complementing general-purpose datasets like MOT17/MOT20.

Key characteristics:
- Static cameras mounted at 6–8 m height on poles
- Outdoor urban scenes with varying crowd densities
- Annotated with pedestrian bounding boxes and track IDs
- Separate training set (with GT) and test set (images only, for benchmarking)

---

## Download

| Split | Contents | Link |
|-------|----------|------|
| Training set | Videos + annotations (GT) | [Google Drive](https://drive.google.com/drive/folders/1Z_gnFmX-EKUe4yLBQPa2pxXkyqYbxkhX?usp=sharing) |
| Test set | Images only (no GT) | [Google Drive](https://drive.google.com/drive/folders/1Z_gnFmX-EKUe4yLBQPa2pxXkyqYbxkhX?usp=sharing) |

---

## Benchmark Challenge

We host an **open benchmark** for multi-pedestrian tracking on the SOMPT22 test set.

- Submit your tracker's results and get scores computed automatically
- Metrics: HOTA, DetA, AssA, MOTA, IDF1
- Rankings updated live on the [Leaderboard](https://sompt22.github.io/leaderboard/)

**[How to Submit →](https://sompt22.github.io/challenge/)**

### Submission Format

Results must follow the **MOT Challenge format** — one `.txt` file per test sequence:

```
# frame, id, bb_left, bb_top, bb_width, bb_height, conf, x, y, z
1, 1, 584, 408, 48, 152, 1, -1, -1, -1
1, 2, 731, 392, 55, 143, 1, -1, -1, -1
```

Zip your result files and follow the steps at [sompt22.github.io/challenge](https://sompt22.github.io/challenge/).

---

## Citation

```bibtex
@misc{simsek2022sompt22,
  doi       = {10.48550/ARXIV.2208.02580},
  url       = {https://arxiv.org/abs/2208.02580},
  author    = {Simsek, Fatih Emre and Cigla, Cevahir and Kayabol, Koray},
  title     = {SOMPT22: A Surveillance Oriented Multi-Pedestrian Tracking Dataset},
  publisher = {arXiv},
  year      = {2022},
  copyright = {Creative Commons Attribution Non Commercial Share Alike 4.0 International}
}
```

---

## License

Dataset annotations: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0).
Dataset videos: available for non-commercial research purposes only.
