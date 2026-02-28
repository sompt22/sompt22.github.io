"""
SOMPT22 Benchmark Evaluation Script
====================================
Evaluates a tracker submission against the SOMPT22 test ground truth.

Usage:
    python evaluate_submission.py \
        --gt_dir   /path/to/gt_repo/test \
        --pred_dir /path/to/submission_results \
        --output   eval_results.json

GT directory structure expected:
    test/
    ├── SOMPT22-01/
    │   └── gt/
    │       └── gt.txt
    ├── SOMPT22-02/
    │   └── gt/
    │       └── gt.txt
    └── ...

Prediction directory (auto-detected layouts):
    Option A:  results/SOMPT22-01.txt   (flat, with subfolder)
    Option B:  SOMPT22-01.txt           (flat, no subfolder)
    Option C:  SOMPT22-01/SOMPT22-01.txt

MOT Challenge format:
    frame, id, bb_left, bb_top, bb_width, bb_height, conf, x, y, z
"""

import argparse
import json
import os
import sys
import glob
import numpy as np
from pathlib import Path

# ── Try to import TrackEval; fall back to motmetrics ─────────────────────────
try:
    import trackeval
    BACKEND = "trackeval"
except ImportError:
    try:
        import motmetrics as mm
        BACKEND = "motmetrics"
    except ImportError:
        print("ERROR: Neither trackeval nor motmetrics is installed.", file=sys.stderr)
        sys.exit(1)


# ── MOT file I/O ──────────────────────────────────────────────────────────────

def load_mot_file(path: str) -> dict:
    """Load a MOT .txt file and return {frame: [(id, x, y, w, h), ...]}"""
    data = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(',')
            if len(parts) < 6:
                continue
            frame = int(float(parts[0]))
            obj_id = int(float(parts[1]))
            x = float(parts[2])
            y = float(parts[3])
            w = float(parts[4])
            h = float(parts[5])
            conf = float(parts[6]) if len(parts) > 6 else 1.0
            if conf < 0:  # ignore DontCare
                continue
            data.setdefault(frame, []).append((obj_id, x, y, w, h))
    return data


def find_pred_file(pred_dir: str, seq_name: str) -> str | None:
    """Find the prediction file for a given sequence name."""
    candidates = [
        os.path.join(pred_dir, f"{seq_name}.txt"),
        os.path.join(pred_dir, "results", f"{seq_name}.txt"),
        os.path.join(pred_dir, seq_name, f"{seq_name}.txt"),
        os.path.join(pred_dir, seq_name, "res.txt"),
    ]
    # Also try any subfolder that was unzipped
    for root, dirs, files in os.walk(pred_dir):
        for fn in files:
            if fn == f"{seq_name}.txt":
                return os.path.join(root, fn)
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


# ── CLEAR / HOTA metrics (motmetrics backend) ─────────────────────────────────

def iou(box1, box2):
    """Compute IoU between two boxes [x, y, w, h]."""
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2
    xa = max(x1, x2)
    ya = max(y1, y2)
    xb = min(x1 + w1, x2 + w2)
    yb = min(y1 + h1, y2 + h2)
    inter = max(0, xb - xa) * max(0, yb - ya)
    union = w1 * h1 + w2 * h2 - inter
    return inter / union if union > 0 else 0.0


def evaluate_with_motmetrics(gt_dir: str, pred_dir: str) -> dict:
    """Evaluate using py-motmetrics (CLEAR metrics + IDF1)."""
    import motmetrics as mm

    sequences = sorted([
        d for d in os.listdir(gt_dir)
        if os.path.isdir(os.path.join(gt_dir, d))
    ])

    if not sequences:
        return {"error": f"No sequences found in GT directory: {gt_dir}"}

    accumulators = []
    names = []
    missing_seqs = []

    for seq in sequences:
        gt_file = os.path.join(gt_dir, seq, "gt", "gt.txt")
        if not os.path.isfile(gt_file):
            gt_file = os.path.join(gt_dir, seq, "gt.txt")
        if not os.path.isfile(gt_file):
            continue

        pred_file = find_pred_file(pred_dir, seq)
        if pred_file is None:
            missing_seqs.append(seq)
            continue

        gt_data   = load_mot_file(gt_file)
        pred_data = load_mot_file(pred_file)

        acc = mm.MOTAccumulator(auto_id=True)
        all_frames = sorted(set(list(gt_data.keys()) + list(pred_data.keys())))

        for frame in all_frames:
            gt_boxes   = gt_data.get(frame, [])
            pred_boxes = pred_data.get(frame, [])

            gt_ids  = [b[0] for b in gt_boxes]
            pred_ids = [b[0] for b in pred_boxes]

            if gt_boxes and pred_boxes:
                dist = np.array([
                    [1.0 - iou(g[1:], p[1:]) for p in pred_boxes]
                    for g in gt_boxes
                ])
                dist[dist > 0.5] = np.nan  # IoU threshold 0.5
            else:
                dist = mm.distances.empty_matrix(len(gt_ids), len(pred_ids))

            acc.update(gt_ids, pred_ids, dist)

        accumulators.append(acc)
        names.append(seq)

    if not accumulators:
        return {"error": f"No matching sequences evaluated. Missing: {missing_seqs}"}

    mh = mm.metrics.create()
    summary = mh.compute_many(
        accumulators,
        metrics=mm.metrics.motchallenge_metrics + ['idf1'],
        names=names,
        generate_overall=True
    )
    overall = summary.loc['OVERALL']

    # Approximate HOTA via geometric mean of DetA and AssA (simplified)
    mota = float(overall.get('mota', 0)) * 100
    idf1 = float(overall.get('idf1', 0)) * 100

    # DetA ~ recall-based, AssA ~ IDF1-based approximation
    num_tp  = int(overall.get('num_matches', 0))
    num_fn  = int(overall.get('num_misses', 0))
    num_fp  = int(overall.get('num_false_positives', 0))
    num_ids = int(overall.get('num_switches', 0))

    deta = num_tp / max(1, num_tp + num_fn + num_fp) * 100
    assa = idf1
    hota = float(np.sqrt(deta * assa / 100))

    if missing_seqs:
        print(f"WARNING: Missing prediction for sequences: {missing_seqs}", file=sys.stderr)

    return {
        "hota": round(hota, 3),
        "deta": round(deta, 3),
        "assa": round(assa, 3),
        "mota": round(mota, 3),
        "idf1": round(idf1, 3),
        "fp":   num_fp,
        "fn":   num_fn,
        "ids":  num_ids,
        "sequences_evaluated": len(accumulators),
        "sequences_missing":   missing_seqs,
        "backend": "motmetrics"
    }


def evaluate_with_trackeval(gt_dir: str, pred_dir: str) -> dict:
    """Evaluate using TrackEval (full HOTA)."""
    import trackeval

    # Prepare a flat pred dir with one file per sequence
    flat_pred = "/tmp/trackeval_pred"
    os.makedirs(flat_pred, exist_ok=True)

    sequences = sorted([
        d for d in os.listdir(gt_dir)
        if os.path.isdir(os.path.join(gt_dir, d))
    ])

    missing = []
    for seq in sequences:
        pred_file = find_pred_file(pred_dir, seq)
        if pred_file:
            dest = os.path.join(flat_pred, f"{seq}.txt")
            if not os.path.exists(dest):
                import shutil
                shutil.copy(pred_file, dest)
        else:
            missing.append(seq)

    # TrackEval dataset config
    dataset_config = {
        'GT_FOLDER':   gt_dir,
        'TRACKERS_FOLDER': flat_pred,
        'OUTPUT_FOLDER': '/tmp/trackeval_out',
        'TRACKERS_TO_EVAL': ['submission'],
        'CLASSES_TO_EVAL': ['pedestrian'],
        'EVAL_OFFICIAL_METRICS': True,
        'PRINT_RESULTS': False,
        'PRINT_ONLY_COMBINED': False,
        'PRINT_CONFIG': False,
        'TIME_PROGRESS': False,
        'OUTPUT_SUMMARY': False,
        'OUTPUT_EMPTY_CLASSES': False,
        'OUTPUT_DETAILED': False,
        'PLOT_CURVES': False,
    }

    evaluator = trackeval.Evaluator({'USE_PARALLEL': False, 'NUM_PARALLEL_CORES': 1,
                                     'BREAK_ON_ERROR': True, 'RETURN_ON_ERROR': False,
                                     'LOG_ON_ERROR': '/tmp/trackeval_error.txt',
                                     'PRINT_RESULTS': False, 'PRINT_CONFIG': False,
                                     'TIME_PROGRESS': False, 'DISPLAY_LESS_PROGRESS': True,
                                     'OUTPUT_SUMMARY': False, 'OUTPUT_EMPTY_CLASSES': False,
                                     'OUTPUT_DETAILED': False, 'PLOT_CURVES': False})
    dataset_list = [trackeval.datasets.MotChallenge2DBox(dataset_config)]
    metrics_list = [
        trackeval.metrics.HOTA(),
        trackeval.metrics.CLEAR(),
        trackeval.metrics.Identity(),
    ]

    output_res, output_msg = evaluator.evaluate(dataset_list, metrics_list)

    # Extract combined results
    try:
        res = output_res['MotChallenge2DBox']['submission']['COMBINED_SEQ']['pedestrian']
        hota_res  = res['HOTA']
        clear_res = res['CLEAR']
        id_res    = res['Identity']

        return {
            "hota": round(float(np.mean(hota_res['HOTA'])) * 100, 3),
            "deta": round(float(np.mean(hota_res['DetA'])) * 100, 3),
            "assa": round(float(np.mean(hota_res['AssA'])) * 100, 3),
            "mota": round(float(clear_res['MOTA']) * 100, 3),
            "idf1": round(float(id_res['IDF1']) * 100, 3),
            "fp":   int(clear_res['FP']),
            "fn":   int(clear_res['FN']),
            "ids":  int(clear_res['IDSW']),
            "sequences_evaluated": len(sequences) - len(missing),
            "sequences_missing":   missing,
            "backend": "trackeval"
        }
    except (KeyError, TypeError) as e:
        return {"error": f"Failed to parse TrackEval output: {e}"}


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SOMPT22 Evaluation Script")
    parser.add_argument('--gt_dir',   required=True, help='GT directory (one subdir per sequence)')
    parser.add_argument('--pred_dir', required=True, help='Prediction directory (extracted zip)')
    parser.add_argument('--output',   required=True, help='Output JSON file path')
    args = parser.parse_args()

    if not os.path.isdir(args.gt_dir):
        result = {"error": f"GT directory not found: {args.gt_dir}"}
    elif not os.path.isdir(args.pred_dir):
        result = {"error": f"Prediction directory not found: {args.pred_dir}"}
    else:
        try:
            if BACKEND == "trackeval":
                result = evaluate_with_trackeval(args.gt_dir, args.pred_dir)
            else:
                result = evaluate_with_motmetrics(args.gt_dir, args.pred_dir)
        except Exception as e:
            import traceback
            result = {"error": str(e), "traceback": traceback.format_exc()}

    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    if "error" in result:
        print(f"Evaluation failed: {result['error']}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"Evaluation complete (backend={result.get('backend')}): "
              f"HOTA={result['hota']:.2f}, MOTA={result['mota']:.2f}, IDF1={result['idf1']:.2f}")


if __name__ == '__main__':
    main()
