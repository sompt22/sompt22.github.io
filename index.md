---
title: SOMPT22
feature_text: |
  ## SOMPT22
  A Surveillance Oriented Multi-Pedestrian Tracking Dataset
feature_image: "/assets/cam2_anno.png"
excerpt: "SOMPT22 is a multi-pedestrian tracking dataset captured from static surveillance cameras. It provides dedicated benchmarking for outdoor city surveillance scenarios."
---

<style>
.feature { position: relative; }
.feature::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
}
.feature .container { position: relative; z-index: 1; }
.feature h2, .feature p { color: white !important; text-shadow: 0 2px 6px rgba(0,0,0,0.7); }
</style>

[Fatih Emre Simsek](https://www.linkedin.com/in/fatihemresimsek/ "Fatih Emre Simsek")<sup>1,2</sup> &nbsp; [Cevahir Cigla](https://www.linkedin.com/in/cevahir-%C3%A7%C4%B1%C4%9Fla-phd-19236135/ "Cevahir Cigla")<sup>1</sup> &nbsp; [Koray Kayabol](https://www.linkedin.com/in/koray-kayabol-75454045/ "Koray Kayabol")<sup>2</sup>

<sup>1</sup>[Aselsan Inc.](https://www.linkedin.com/company/aselsan/mycompany/ "Aselsan Inc.") &nbsp; <sup>2</sup>[Gebze Technical University](https://www.linkedin.com/school/gebze-teknik-%C3%BCniversitesi/ "Gebze Technical University")

{% include figure.html image="/assets/paper_pics/tumbnail.png" width="1920" height="1000" %}

{% include button.html text="Paper" icon="link" link="https://arxiv.org/abs/2208.02580" color="#0d84f7" %} {% include button.html text="Download Dataset" icon="link" link="https://drive.google.com/drive/folders/1Z_gnFmX-EKUe4yLBQPa2pxXkyqYbxkhX?usp=sharing" color="#28a745" %} {% include button.html text="Leaderboard" icon="link" link="/leaderboard/" color="#e36209" %} {% include button.html text="Submit Results" icon="link" link="/challenge/" color="#6f42c1" %} {% include button.html text="GitHub" icon="github" link="https://github.com/sompt22" color="#0366d6" %}

## Abstract

Multi-object tracking (MOT) has been dominated by the use of track by detection approaches due to the success of convolutional neural networks (CNNs) on detection in the last decade. As the datasets and bench-marking sites are published, research direction has shifted towards yielding best accuracy on generic scenarios including re-identification
(reID) of objects while tracking. In this study, we narrow the scope of MOT for surveillance by providing a dedicated dataset of pedestrians and focus on in-depth analyses of well performing multi-object trackers to observe the weak and strong sides of state-of-the-art (SOTA) techniques for real-world applications. For this purpose, we introduce SOMPT22 dataset; a new set for multi person tracking with annotated short videos
captured from static cameras located on poles with 6-8 meters in height positioned for city surveillance. This provides a more focused and specific benchmarking of MOT for outdoor surveillance compared to public MOT datasets. We analyze MOT trackers classified as one-shot and two-stage with respect to the way of use of detection and reID networks on
this new dataset. The experimental results of our new dataset indicate that SOTA is still far from high efficiency, and single-shot trackers are good candidates to unify fast execution and accuracy with competitive performance.

## Benchmark Challenge

We host an open benchmark challenge for multi-pedestrian tracking on the SOMPT22 test set.
Submit your tracker's results and get your scores computed automatically — rankings are updated live.

{% include button.html text="View Leaderboard" icon="link" link="/leaderboard/" color="#e36209" %} {% include button.html text="How to Submit" icon="link" link="/challenge/" color="#6f42c1" %}

## Dataset

The dataset is distributed as a single archive containing two splits: **training** (with ground-truth annotations) and **test** (images only, no GT). The test GT is held privately for benchmark evaluation.

{% include button.html text="Download Dataset" icon="link" link="https://drive.google.com/drive/folders/1Z_gnFmX-EKUe4yLBQPa2pxXkyqYbxkhX?usp=sharing" color="#28a745" %}

## Detection & Tracking Datasets

{% include figure.html image="/assets/paper_pics/table1_1.png" width="1920" height="1000" %}

{% include figure.html image="/assets/paper_pics/table2_2.png" width="1920" height="1000" %}

## SOMPT22 Statistics

{% include figure.html image="/assets/paper_pics/fig1_3.png" width="1920" height="1000" %}

{% include figure.html image="/assets/paper_pics/table3_4.png" width="1920" height="1000" %}

## Experiment Setup

{% include figure.html image="/assets/paper_pics/table4-5.png" width="1920" height="1000" %}

## Benchmark Results

{% include figure.html image="/assets/paper_pics/table6-7.png" width="1920" height="1000" %}

{% include figure.html image="/assets/paper_pics/table8.png" width="1920" height="1000" %}

{% include figure.html image="/assets/paper_pics/table9.png" width="1920" height="1000" %}

{% include figure.html image="/assets/paper_pics/fig2.png" width="1920" height="1000" %}

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

## License

The annotations of SOMPT22 are licensed under a [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0 "Creative Commons Attribution 4.0 License"). The dataset of SOMPT22 is available for non-commercial research purposes only. All videos and images of SOMPT22 are obtained from the Internet.
