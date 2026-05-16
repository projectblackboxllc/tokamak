#!/usr/bin/env python3
"""Generate Zenodo-safe copies of the aggregated experiment CSVs.

Reads from ../../../../data/  (the original aggregated CSVs)
Writes to .                    (this folder)

Redacts mechanism-state columns (anything that exposes the TOU
accumulator integral, the saturating-actuator command, or the actuator's
signed output) plus internal filesystem path columns. Leaves all
measurement quantities and parameter settings intact.
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
SRC = HERE.parent.parent.parent.parent / "data"  # repo root /data

# Columns to strip from any CSV they appear in
REDACT = {
    "final_inj_cmd",
    "final_inj_applied",
    "final_signed_output",
    "final_acc",
    "run_dir",
    "off_run_dir",
    "on_run_dir",
}

FILES = [
    "exp_001_lh_transition.csv",
    "exp_005_dirty_twin_blindness.csv",
    "exp_006_dirty_twin_slew.csv",
    "exp_007_dirty_twin_ripple.csv",
    "exp_008_dirty_twin_ripple_stringent.csv",
]

def main():
    for name in FILES:
        src = SRC / name
        dst = HERE / name
        df = pd.read_csv(src)
        dropped = [c for c in df.columns if c in REDACT]
        df_clean = df.drop(columns=dropped)
        df_clean.to_csv(dst, index=False)
        print(f"{name:48s}  dropped {len(dropped):>2} cols → {list(dropped)}")
        print(f"  kept ({len(df_clean.columns):>2}): {list(df_clean.columns)}")
        print()

if __name__ == "__main__":
    main()
