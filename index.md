---
title: SOMPT22
feature_text: | 
  
feature_image: "/assets/cam2_anno.png"
excerpt: "Alembic is a starting point for [Jekyll](https://jekyllrb.com/) projects. Rather than starting from scratch, this boilerplate is designed to get the ball rolling immediately. Install it, configure it, tweak it, push it."
---

Multi-Object Tracking Dataset. 

[Fatih Emre Simsek](https://www.linkedin.com/in/fatihemresimsek/ "Fatih Emre Simsek")<sup>1,2</sup> [Cevahir Cigla](https://www.linkedin.com/in/cevahir-%C3%A7%C4%B1%C4%9Fla-phd-19236135/ "Cevahir Cigla")<sup>1</sup> [Koray Kayabol](https://www.linkedin.com/in/koray-kayabol-75454045/ "Koray Kayabol")<sup>2</sup>

<sup>1</sup>[Aselsan Inc.](https://www.linkedin.com/company/aselsan/mycompany/ "Aselsan Inc.") <sup>2</sup>[Gebze Technical University](https://www.linkedin.com/school/gebze-teknik-%C3%BCniversitesi/ "Gebze Technical University") 

{% include figure.html image="/assets/paper_pics/tumbnail.png" width="1920" height="1000" %}


{% include button.html text="Fork it" icon="github" link="https://github.com/sompt22" color="#0366d6" %} {% include button.html text="Tweet it" icon="twitter" link="https://twitter.com/" color="#0d94e7" %} {% include button.html text="Paper" icon="link" link="https://arxiv.org/abs/2208.02580" color="#0d84f7" %}


## Abstract

Multi-object tracking (MOT) has been dominated by the use of track by detection approaches due to the success of convolutional neural networks (CNNs) on detection in the last decade. As the datasets and bench-marking sites are published, research direction has shifted towards yielding best accuracy on generic scenarios including re-identification
(reID) of objects while tracking. In this study, we narrow the scope of MOT for surveillance by providing a dedicated dataset of pedestrians and focus on in-depth analyses of well performing multi-object trackers to observe the weak and strong sides of state-of-the-art (SOTA) techniques for real-world applications. For this purpose, we introduce SOMPT22 dataset; a new set for multi person tracking with annotated short videos
captured from static cameras located on poles with 6-8 meters in height positioned for city surveillance. This provides a more focused and specific benchmarking of MOT for outdoor surveillance compared to public MOT datasets. We analyze MOT trackers classified as one-shot and two-stage with respect to the way of use of detection and reID networks on
this new dataset. The experimental results of our new dataset indicate that SOTA is still far from high efficiency, and single-shot trackers are good candidates to unify fast execution and accuracy with competitive performance.

## Dataset

Download the dataset from [Google Drive](https://drive.google.com/drive/folders/1Z_gnFmX-EKUe4yLBQPa2pxXkyqYbxkhX?usp=sharing)

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

``` js
@misc{https://doi.org/10.48550/arxiv.2208.02580,
  doi = {10.48550/ARXIV.2208.02580},
  url = {https://arxiv.org/abs/2208.02580},
  author = {Simsek, Fatih Emre and Cigla, Cevahir and Kayabol, Koray},
  keywords = {Computer Vision and Pattern Recognition (cs.CV), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {SOMPT22: A Surveillance Oriented Multi-Pedestrian Tracking Dataset},
  publisher = {arXiv},
  year = {2022},
  copyright = {Creative Commons Attribution Non Commercial Share Alike 4.0 International}
}
```


## License

The annotations of SOMPT22 are licensed under a [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0 "Creative Commons Attribution 4.0 License"). The dataset of SOMPT22 is available for non-commercial research purposes only. All videos and images of SOMPT22 are obtained from the Internet. 
