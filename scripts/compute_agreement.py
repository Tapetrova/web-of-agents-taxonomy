#!/usr/bin/env python3
"""Recompute pairwise agreement and Cohen's kappa from rater CSVs.

Usage:
    python3 scripts/compute_agreement.py

Reads:
    experiments/rater_outputs/rater{1,2,3}.csv
Writes:
    experiments/e4sim_assignments.csv  (long format)
    experiments/e4sim_matrix.csv       (wide summary)
    experiments/e4sim_results.json     (agreement + kappa)

UNSPECIFIED is treated as its own category for agreement and kappa.
"""
from __future__ import annotations
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RATER_DIR = ROOT / "experiments" / "rater_outputs"
OUT_DIR = ROOT / "experiments"


def load_rater(n: int):
    path = RATER_DIR / f"rater{n}.csv"
    rows = []
    for row in csv.DictReader(path.open()):
        if row["system"].startswith("#"):
            continue
        rows.append(row)
    return rows


def cohens_kappa(a, b):
    n = len(a)
    cats = sorted(set(a) | set(b), key=str)
    po = sum(1 for x, y in zip(a, b) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in cats)
    if pe == 1.0:
        return 1.0 if po == 1.0 else float("nan")
    return (po - pe) / (1 - pe)


def main():
    R = {n: load_rater(n) for n in (1, 2, 3)}
    systems = [row["system"] for row in R[1]]
    axes = ["a1", "a2", "a3", "a4"]

    with (OUT_DIR / "e4sim_assignments.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["system", "axis", "rater", "value", "quote", "source"])
        for i, s in enumerate(systems):
            for ax in axes:
                for r in (1, 2, 3):
                    row = R[r][i]
                    w.writerow([s, ax, f"R{r}", row[ax],
                                row[f"{ax}_quote"], row[f"{ax}_source"]])

    with (OUT_DIR / "e4sim_matrix.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["system", "axis", "R1", "R2", "R3",
                    "majority", "all_agree"])
        for i, s in enumerate(systems):
            for ax in axes:
                vals = [R[r][i][ax] for r in (1, 2, 3)]
                c = Counter(vals).most_common()
                majority = c[0][0] if c[0][1] >= 2 else "NONE"
                w.writerow([s, ax, *vals, majority,
                            "yes" if c[0][1] == 3 else "no"])

    out = {}
    for ax in axes:
        r1 = [R[1][i][ax] for i in range(len(systems))]
        r2 = [R[2][i][ax] for i in range(len(systems))]
        r3 = [R[3][i][ax] for i in range(len(systems))]
        pct = {
            "R1R2": sum(1 for a, b in zip(r1, r2) if a == b) / len(r1),
            "R1R3": sum(1 for a, b in zip(r1, r3) if a == b) / len(r1),
            "R2R3": sum(1 for a, b in zip(r2, r3) if a == b) / len(r1),
        }
        k = {
            "R1R2": cohens_kappa(r1, r2),
            "R1R3": cohens_kappa(r1, r3),
            "R2R3": cohens_kappa(r2, r3),
        }
        k["mean"] = (k["R1R2"] + k["R1R3"] + k["R2R3"]) / 3
        out[ax] = {
            "pct_agree": pct,
            "cohens_kappa": k,
            "N": len(systems),
            "disagreements": [
                {"system": systems[i], "vals": [r1[i], r2[i], r3[i]]}
                for i in range(len(systems))
                if len({r1[i], r2[i], r3[i]}) > 1
            ],
        }
    out["_meta"] = {
        "n_raters": 3,
        "n_systems": 5,
        "notes": ("Raters used local corpus only. UNSPECIFIED treated as "
                  "its own category for agreement and kappa."),
    }

    with (OUT_DIR / "e4sim_results.json").open("w") as f:
        json.dump(out, f, indent=2)

    for ax in axes:
        mk = out[ax]["cohens_kappa"]["mean"]
        pa = sum(out[ax]["pct_agree"].values()) / 3
        print(f"Axis {ax}: pct_agree(mean)={pa:.3f}  kappa(mean)={mk:.3f}")


if __name__ == "__main__":
    main()
