"""
Fitts' Law analysis for the Trembling-Finger Springboard experiment.

Usage:
    pip install numpy matplotlib
    python analyze.py data/trials.csv

Reads the CSV exported by index.html (columns: trial, block, gridLevel,
W_px, A_px, MT_ms, errors, timestamp), fits the Shannon formulation of
Fitts' Law:

    MT = a + b * log2(A / W + 1)

via least-squares linear regression on ID = log2(A/W + 1), and saves an
academic-style scatter plot with the regression line to results/scatter.png.
"""
import csv
import sys
import math
import numpy as np
import matplotlib.pyplot as plt


def load(path):
    A, W, MT = [], [], []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            A.append(float(row["A_px"]))
            W.append(float(row["W_px"]))
            MT.append(float(row["MT_ms"]))
    return np.array(A), np.array(W), np.array(MT)


def main(path="data/trials.csv", out="results/scatter.png"):
    A, W, MT = load(path)
    ID = np.log2(A / W + 1)

    b, a = np.polyfit(ID, MT, 1)  # MT = a + b * ID
    r = np.corrcoef(ID, MT)[0, 1]
    r2 = r ** 2

    print(f"n trials        = {len(MT)}")
    print(f"Fitts' Law fit  : MT = {a:.1f} + {b:.1f} * ID")
    print(f"R^2             = {r2:.3f}")
    print(f"Throughput (IP) = {1000 / b:.2f} bits/s"
          if b != 0 else "Throughput undefined (b=0)")

    plt.figure(figsize=(7, 5))
    plt.scatter(ID, MT, alpha=0.7, edgecolor="black", linewidth=0.5, label="Trials")

    xs = np.linspace(ID.min(), ID.max(), 100)
    plt.plot(xs, a + b * xs, color="crimson",
              label=f"MT = {a:.1f} + {b:.1f}·ID   (R²={r2:.2f})")

    plt.xlabel("Index of Difficulty,  ID = log₂(A/W + 1)")
    plt.ylabel("Movement Time (ms)")
    plt.title("Fitts' Law — Trembling-Finger Springboard Task")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(out, dpi=200)
    print(f"Saved plot to {out}")


if __name__ == "__main__":
    csv_path = sys.argv[1] if len(sys.argv) > 1 else "data/trials.csv"
    main(csv_path)
