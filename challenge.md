---
title: "SOMPT22 Challenge"
feature_text: |
  ## SOMPT22 Benchmark Challenge
  Submit your multi-pedestrian tracking results and compete on the leaderboard
feature_image: "/assets/cam2_anno.png"
layout: page
---

<style>
.challenge-section {
  background: #f8f9fa;
  border-left: 4px solid #0d84f7;
  padding: 1rem 1.25rem;
  margin: 1.5rem 0;
  border-radius: 0 4px 4px 0;
}
.challenge-section h3 { margin-top: 0; }
.step-list { counter-reset: steps; list-style: none; padding: 0; }
.step-list li {
  counter-increment: steps;
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  align-items: flex-start;
}
.step-list li::before {
  content: counter(steps);
  background: #0d84f7;
  color: white;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  min-width: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.85rem;
}
.format-box {
  background: #1e1e1e;
  color: #d4d4d4;
  padding: 1rem;
  border-radius: 6px;
  font-family: monospace;
  font-size: 0.85rem;
  overflow-x: auto;
}
.format-box .comment { color: #6a9955; }
.format-box .keyword { color: #569cd6; }
.metric-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 0.75rem;
  margin: 1rem 0;
}
.metric-card {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 0.75rem;
  text-align: center;
}
.metric-card .metric-name { font-weight: 700; color: #0d84f7; font-size: 1rem; }
.metric-card .metric-desc { font-size: 0.8rem; color: #555; margin-top: 0.25rem; }
.warning-box {
  background: #fff8e1;
  border-left: 4px solid #ffc107;
  padding: 0.75rem 1rem;
  margin: 1rem 0;
  border-radius: 0 4px 4px 0;
}
.btn-submit {
  display: inline-block;
  background: #0d84f7;
  color: white !important;
  padding: 0.75rem 2rem;
  border-radius: 6px;
  font-weight: 600;
  text-decoration: none !important;
  margin: 0.5rem 0;
  font-size: 1rem;
}
.btn-submit:hover { background: #0a6cc9; }
</style>

## Overview

The SOMPT22 Benchmark Challenge is an open competition for multi-pedestrian tracking on surveillance footage. Participants run their trackers on the **test set** and submit results for automated evaluation.

- **Primary metric:** HOTA (Higher Order Tracking Accuracy)
- **Evaluation tool:** [TrackEval](https://github.com/JonathonLuiten/TrackEval)
- **Results format:** MOT Challenge format (`.txt` per sequence)
- **Submission:** via GitHub Issue

---

## Datasets

<div class="challenge-section">
<h3>Training Set (public)</h3>
<p>
  Videos and ground-truth annotations are publicly available for download.
  Use the training set to develop and tune your tracker.
</p>
{% include button.html text="Download Training Set" icon="link" link="https://drive.google.com/drive/folders/1Z_gnFmX-EKUe4yLBQPa2pxXkyqYbxkhX?usp=sharing" color="#0d84f7" %}
</div>

<div class="challenge-section">
<h3>Test Set (images only — no GT)</h3>
<p>
  The test set contains only video frames. Ground-truth annotations are held privately
  for evaluation. Download the test set, run your tracker, and submit results.
</p>
{% include button.html text="Download Test Set" icon="link" link="https://drive.google.com/drive/folders/1Z_gnFmX-EKUe4yLBQPa2pxXkyqYbxkhX?usp=sharing" color="#28a745" %}
</div>

---

## Evaluation Metrics

<div class="metric-grid">
  <div class="metric-card">
    <div class="metric-name">HOTA</div>
    <div class="metric-desc">Higher Order Tracking Accuracy — primary ranking metric</div>
  </div>
  <div class="metric-card">
    <div class="metric-name">DetA</div>
    <div class="metric-desc">Detection Accuracy (sub-metric of HOTA)</div>
  </div>
  <div class="metric-card">
    <div class="metric-name">AssA</div>
    <div class="metric-desc">Association Accuracy (sub-metric of HOTA)</div>
  </div>
  <div class="metric-card">
    <div class="metric-name">MOTA</div>
    <div class="metric-desc">Multiple Object Tracking Accuracy (CLEAR metric)</div>
  </div>
  <div class="metric-card">
    <div class="metric-name">IDF1</div>
    <div class="metric-desc">ID F1 Score — identity preservation</div>
  </div>
  <div class="metric-card">
    <div class="metric-name">FP / FN / IDs</div>
    <div class="metric-desc">False Positives, False Negatives, ID Switches</div>
  </div>
</div>

---

## Result Format

Results must be in **MOT Challenge format**: one `.txt` file per test sequence, named after the sequence.

<div class="format-box">
<span class="comment"># Format: frame, id, bb_left, bb_top, bb_width, bb_height, conf, x, y, z</span><br>
<span class="comment"># conf = detection confidence (use 1 if not applicable)</span><br>
<span class="comment"># x, y, z = -1 for 2D tracking</span><br>
1, 1, 584, 408, 48, 152, 1, -1, -1, -1<br>
1, 2, 731, 392, 55, 143, 1, -1, -1, -1<br>
2, 1, 586, 412, 48, 152, 1, -1, -1, -1<br>
...
</div>

**File structure expected:**

<div class="format-box">
results/<br>
├── SOMPT22-01.txt<br>
├── SOMPT22-02.txt<br>
├── SOMPT22-03.txt<br>
└── ...
</div>

Compress the `results/` folder as a `.zip` file before submitting.

<div class="warning-box">
⚠️ <strong>Important:</strong> Sequence names must exactly match the SOMPT22 test sequence names.
Use the sequence list provided in the test set README.
</div>

---

## How to Submit

<ol class="step-list">
  <li><div><strong>Run your tracker</strong> on all SOMPT22 test sequences and prepare result files in MOT format.</div></li>
  <li><div><strong>Upload your results</strong> as a <code>.zip</code> file to a publicly accessible location (Google Drive, Dropbox, GitHub Releases, etc.).</div></li>
  <li><div><strong>Open a GitHub Issue</strong> on this repository using the <em>Benchmark Submission</em> template. Fill in all required fields including the public download link to your results zip.</div></li>
  <li><div><strong>Automated evaluation</strong> will run within a few minutes. Results will be posted as a comment on your issue.</div></li>
  <li><div><strong>Leaderboard update</strong>: accepted submissions are added to the leaderboard automatically.</div></li>
</ol>

<a class="btn-submit" href="https://github.com/sompt22/sompt22.github.io/issues/new?template=submission.yml" target="_blank">
  Open Submission Issue →
</a>

---

## Rules

1. **Test GT is private** — do not attempt to obtain or use test ground-truth labels.
2. **One active submission per team per week** — wait for evaluation results before resubmitting.
3. **Paper or technical report required** for top-3 entries (link or arXiv preprint accepted).
4. Trackers may use **any publicly available pretrained model**. External private training data must be declared.
5. Reported **FPS** must be measured on a standard GPU (e.g., RTX 3090 or equivalent). Declare your hardware.
6. The organizers reserve the right to re-evaluate submissions or request code for reproducibility.

---

## Questions?

Open a [GitHub Discussion](https://github.com/sompt22/sompt22.github.io/discussions) or contact via [LinkedIn](https://www.linkedin.com/in/fatihemresimsek/).

---

*Evaluation powered by [TrackEval](https://github.com/JonathonLuiten/TrackEval) — HOTA metric by Luiten et al.*
