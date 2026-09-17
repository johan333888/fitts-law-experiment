"""
Fitts' Law analysis for the Trembling-Finger Springboard experiment.

Usage:
    pip install numpy matplotlib
    python analyze.py data/trials.csv

Reads the CSV exported by index.html (columns: trial, block, gridLevel,
W_px, A_px, MT_ms, errors, timestamp) and fits the Shannon formulation of
Fitts' Law, MT = a + b * log2(A / W + 1), via least-squares linear
regression on ID = log2(A/W + 1).

Two fits are produced, side by side:

  1. Raw trial-level fit, one point per individual tap (n = all trials).
     This keeps every trial's full motor/tremor noise, so R^2 is lower.
  2. Block-averaged fit, one point per icon-size block (n = number of
     blocks), each point the mean ID and mean MT of that block's taps.
     This is the classic Fitts'-Law-paper approach of averaging repeated
     trials per condition before regressing, which cancels out per-trial
     noise and yields a much higher R^2 for the same underlying data.

Both are saved side by side to results/scatter.png.
"""
import csv
import sys
import math
import numpy as np
import matplotlib.pyplot as plt


def load(path):
    rows = list(csv.DictReader(open(path, newline="")))
    A = np.array([float(r["A_px"]) for r in rows])
    W = np.array([float(r["W_px"]) for r in rows])
    MT = np.array([float(r["MT_ms"]) for r in rows])
    block = np.array([r["gridLevel"] for r in rows])
    return A, W, MT, block


def fit(ID, MT):
    b, a = np.polyfit(ID, MT, 1)  # MT = a + b * ID
    r2 = np.corrcoef(ID, MT)[0, 1] ** 2
    return a, b, r2


def block_average(ID, MT, block):
    ids, mts = [], []
    for lvl in np.unique(block):
        mask = block == lvl
        ids.append(ID[mask].mean())
        mts.append(MT[mask].mean())
    return np.array(ids), np.array(mts)


def plot_fit(ax, ID, MT, a, b, r2, title):
    ax.scatter(ID, MT, alpha=0.75, edgecolor="black", linewidth=0.5, label="Trials")
    xs = np.linspace(ID.min(), ID.max(), 100)
    ax.plot(xs, a + b * xs, color="crimson",
            label=f"MT = {a:.1f} + {b:.1f}·ID   (R²={r2:.2f})")
    ax.set_xlabel("Index of Difficulty,  ID = log₂(A/W + 1)")
    ax.set_ylabel("Movement Time (ms)")
    ax.set_title(title)
    ax.legend()
    ax.grid(alpha=0.25)


def main(path="data/trials.csv", out="results/scatter.png"):
    A, W, MT, block = load(path)
    ID = np.log2(A / W + 1)

    a_raw, b_raw, r2_raw = fit(ID, MT)
    ID_blk, MT_blk = block_average(ID, MT, block)
    a_blk, b_blk, r2_blk = fit(ID_blk, MT_blk)

    print(f"n trials              = {len(MT)}")
    print(f"Raw-trial fit         : MT = {a_raw:.1f} + {b_raw:.1f} * ID   R^2 = {r2_raw:.3f}")
    print(f"n blocks (averaged)   = {len(MT_blk)}")
    print(f"Block-averaged fit    : MT = {a_blk:.1f} + {b_blk:.1f} * ID   R^2 = {r2_blk:.3f}")
    print(f"Throughput (IP, raw)  = {1000 / b_raw:.2f} bits/s" if b_raw else "n/a")
    print(f"Throughput (IP, blk)  = {1000 / b_blk:.2f} bits/s" if b_blk else "n/a")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    plot_fit(ax1, ID, MT, a_raw, b_raw, r2_raw,
             f"Raw trials (n={len(MT)})")
    plot_fit(ax2, ID_blk, MT_blk, a_blk, b_blk, r2_blk,
             f"Block-averaged (n={len(MT_blk)} icon sizes)")
    fig.suptitle("Fitts' Law — Trembling-Finger Springboard Task")
    fig.tight_layout()
    fig.savefig(out, dpi=200)
    print(f"Saved plot to {out}")


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/trials.csv"
    main(csv_path)
