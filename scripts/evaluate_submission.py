"""
SOMPT22 Benchmark Evaluation Script
====================================
Evaluates a tracker submission against the SOMPT22 test ground truth
using TrackEval (https://github.com/JonathonLuiten/TrackEval).

Metrics computed
----------------
  HOTA, DetA, AssA  — Higher Order Tracking Accuracy (primary)
  MOTA, MOTP        — CLEAR metrics
  IDF1, IDP, IDR    — Identity metrics
  FP, FN, IDSW, MT, ML

Usage
-----
    python evaluate_submission.py \
        --gt_dir   /path/to/gt_repo/test \
        --pred_dir /path/to/extracted_submission \
        --output   eval_results.json

GT directory structure (--gt_dir points to the split folder)
-------------------------------------------------------------
    test/
    ├── SOMPT22-01/
    │   └── gt/
    │       └── gt.txt          ← MOT Challenge format
    ├── SOMPT22-02/
    │   └── gt/
    │       └── gt.txt
    └── ...

Prediction directory (auto-detected, any nesting)
-------------------------------------------------
    The script walks the entire directory tree and picks up the first
    file named <seq>.txt for each sequence.

GT file format (MOT Challenge)
-------------------------------
    frame, id, bb_left, bb_top, bb_width, bb_height, conf, class, visibility
    conf=0  → distractor / ignore region (excluded by TrackEval's preprocessor)
    class=1 → pedestrian
"""

import argparse
import json
import os
import shutil
import sys

import numpy as np
import trackeval


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_seq_length(gt_txt_path: str) -> int:
    """Return sequence length from seqinfo.ini if present, else max frame in GT.

    Reading seqinfo.ini is preferred because GT files may not have annotations
    on every frame (e.g. empty final frames), which would cause max-frame to
    undercount and TrackEval to skip those frames during evaluation.
    """
    seqinfo_path = os.path.join(os.path.dirname(gt_txt_path), '..', 'seqinfo.ini')
    seqinfo_path = os.path.normpath(seqinfo_path)
    if os.path.isfile(seqinfo_path):
        with open(seqinfo_path) as f:
            for line in f:
                if line.lower().startswith('seqlength'):
                    try:
                        return int(line.split('=')[1].strip())
                    except (ValueError, IndexError):
                        break

    max_frame = 0
    with open(gt_txt_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(',')
            try:
                max_frame = max(max_frame, int(float(parts[0])))
            except (ValueError, IndexError):
                pass
    return max_frame


def find_pred_file(pred_dir: str, seq_name: str) -> str | None:
    """Walk pred_dir tree and return the path to <seq_name>.txt, or None.

    Matching is case-insensitive so submissions like 'sompt22-01.txt' are
    accepted alongside the canonical 'SOMPT22-01.txt'.
    """
    target = f"{seq_name}.txt".lower()
    for root, _dirs, files in os.walk(pred_dir):
        for fname in files:
            if fname.lower() == target:
                return os.path.join(root, fname)
    return None


def discover_sequences(gt_split_dir: str) -> list[str]:
    """Return sorted list of sequences that have a gt/gt.txt file."""
    seqs = []
    for name in os.listdir(gt_split_dir):
        gt_file = os.path.join(gt_split_dir, name, 'gt', 'gt.txt')
        if os.path.isdir(os.path.join(gt_split_dir, name)) and os.path.isfile(gt_file):
            seqs.append(name)
    return sorted(seqs)


# ── Evaluation ────────────────────────────────────────────────────────────────

def evaluate(gt_split_dir: str, pred_dir: str) -> dict:
    """
    Run TrackEval on all sequences found in gt_split_dir.

    TrackEval expected layout
    -------------------------
      GT_FOLDER / <split> / <seq> / gt / gt.txt
      TRACKERS_FOLDER / <tracker> / <TRACKER_SUB_FOLDER> / <seq>.txt

    We derive <split> from the basename of gt_split_dir so the caller
    can simply pass the path to the split folder directly.
    """
    split_name = os.path.basename(gt_split_dir.rstrip('/'))  # e.g. "test"
    gt_root    = os.path.dirname(gt_split_dir.rstrip('/'))    # parent of split/

    sequences = discover_sequences(gt_split_dir)
    if not sequences:
        return {"error": f"No sequences with gt/gt.txt found in: {gt_split_dir}"}

    # Build SEQ_INFO: {seq_name: num_frames} — avoids needing seqinfo.ini
    seq_info = {
        seq: get_seq_length(os.path.join(gt_split_dir, seq, 'gt', 'gt.txt'))
        for seq in sequences
    }

    # ── Stage tracker predictions into TrackEval's expected structure ──────
    # TRACKERS_FOLDER/submission/data/<seq>.txt
    tracker_root     = '/tmp/te_trackers'
    tracker_sub_fol  = 'data'
    tracker_data_dir = os.path.join(tracker_root, 'submission', tracker_sub_fol)
    # Always start clean so stale files from a previous run don't contaminate results.
    shutil.rmtree(tracker_root, ignore_errors=True)
    os.makedirs(tracker_data_dir, exist_ok=True)

    missing = []
    for seq in sequences:
        pred_file = find_pred_file(pred_dir, seq)
        dest = os.path.join(tracker_data_dir, f"{seq}.txt")
        if pred_file:
            shutil.copy(pred_file, dest)
        else:
            missing.append(seq)
            open(dest, 'w').close()  # empty file → scores 0 for this sequence

    if missing:
        print(f"WARNING: No prediction found for {len(missing)} sequence(s): {missing}",
              file=sys.stderr)

    if len(missing) == len(sequences):
        return {"error": "No prediction files matched any GT sequence. "
                         "Ensure file names match sequence names (e.g. SOMPT22-01.txt).",
                "sequences_missing": missing}

    # ── TrackEval config ───────────────────────────────────────────────────
    eval_config = {
        'USE_PARALLEL':          False,
        'NUM_PARALLEL_CORES':    1,
        'BREAK_ON_ERROR':        True,
        'RETURN_ON_ERROR':       False,
        'LOG_ON_ERROR':          '/tmp/te_error.txt',
        'PRINT_RESULTS':         False,
        'PRINT_CONFIG':          False,
        'TIME_PROGRESS':         False,
        'DISPLAY_LESS_PROGRESS': True,
        'OUTPUT_SUMMARY':        False,
        'OUTPUT_EMPTY_CLASSES':  False,
        'OUTPUT_DETAILED':       False,
        'PLOT_CURVES':           False,
    }

    dataset_config = {
        'GT_FOLDER':         gt_root,
        'TRACKERS_FOLDER':   tracker_root,
        'OUTPUT_FOLDER':     '/tmp/te_out',
        'SPLIT_TO_EVAL':     split_name,
        'TRACKERS_TO_EVAL':  ['submission'],
        'CLASSES_TO_EVAL':   ['pedestrian'],
        'TRACKER_SUB_FOLDER': tracker_sub_fol,
        'SEQ_INFO':          seq_info,   # avoids needing seqinfo.ini
        'DO_PREPROC':        True,       # filters distractors (conf=0 in GT)
        'PRINT_CONFIG':      False,
    }

    # ── Run evaluation ─────────────────────────────────────────────────────
    evaluator    = trackeval.Evaluator(eval_config)
    dataset_list = [trackeval.datasets.MotChallenge2DBox(dataset_config)]
    metrics_list = [
        trackeval.metrics.HOTA(),
        trackeval.metrics.CLEAR(),
        trackeval.metrics.Identity(),
    ]

    output_res, _output_msg = evaluator.evaluate(dataset_list, metrics_list)

    # ── Extract results ────────────────────────────────────────────────────
    combined = output_res['MotChallenge2DBox']['submission']['COMBINED_SEQ']['pedestrian']
    hota_res  = combined['HOTA']
    clear_res = combined['CLEAR']
    id_res    = combined['Identity']

    # HOTA is computed at 19 α thresholds (0.05 … 0.95); final value = mean
    hota_per_alpha = {
        f"{0.05 * (i + 1):.2f}": round(float(hota_res['HOTA'][i]) * 100, 3)
        for i in range(len(hota_res['HOTA']))
    }

    return {
        # Primary metrics
        "hota": round(float(np.mean(hota_res['HOTA'])) * 100, 3),
        "deta": round(float(np.mean(hota_res['DetA'])) * 100, 3),
        "assa": round(float(np.mean(hota_res['AssA'])) * 100, 3),
        # CLEAR
        "mota": round(float(clear_res['MOTA']) * 100, 3),
        "motp": round(float(clear_res['MOTP']) * 100, 3),
        # Identity
        "idf1": round(float(id_res['IDF1']) * 100, 3),
        "idp":  round(float(id_res['IDP'])  * 100, 3),
        "idr":  round(float(id_res['IDR'])  * 100, 3),
        # Counts
        "fp":   int(clear_res['FP']),
        "fn":   int(clear_res['FN']),
        "ids":  int(clear_res['IDSW']),
        "mt":   int(clear_res['MT']),
        "ml":   int(clear_res['ML']),
        # Diagnostics
        "hota_per_alpha":      hota_per_alpha,
        "sequences_evaluated": len(sequences) - len(missing),
        "sequences_missing":   missing,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='SOMPT22 TrackEval evaluation script')
    parser.add_argument('--gt_dir',   required=True,
                        help='Path to GT split folder (contains one subdir per sequence)')
    parser.add_argument('--pred_dir', required=True,
                        help='Path to extracted submission directory')
    parser.add_argument('--output',   required=True,
                        help='Output JSON file path')
    args = parser.parse_args()

    if not os.path.isdir(args.gt_dir):
        result = {"error": f"GT directory not found: {args.gt_dir}"}
    elif not os.path.isdir(args.pred_dir):
        result = {"error": f"Prediction directory not found: {args.pred_dir}"}
    else:
        try:
            result = evaluate(args.gt_dir, args.pred_dir)
        except Exception as exc:
            import traceback
            result = {"error": str(exc), "traceback": traceback.format_exc()}

    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    if "error" in result:
        print(f"Evaluation failed: {result['error']}", file=sys.stderr)
        sys.exit(1)

    print(
        f"HOTA={result['hota']:.2f}  DetA={result['deta']:.2f}  AssA={result['assa']:.2f}  "
        f"MOTA={result['mota']:.2f}  IDF1={result['idf1']:.2f}  "
        f"FP={result['fp']}  FN={result['fn']}  IDSW={result['ids']}"
    )


if __name__ == '__main__':
    main()
