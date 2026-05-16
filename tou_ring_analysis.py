#!/usr/bin/env python3
"""
TOU Ring Analyzer — FFT Mode Analysis
"""

import os, glob, json
import pandas as pd
import numpy as np

def analyze_latest():
    runs = sorted(glob.glob("outputs/run_*"))
    if not runs:
        print("No runs found.")
        return
    run = runs[-1]
    print(f"--- TOU RING ANALYZER ---")
    print(f"Targeting Run: {run}")

    df = pd.read_csv(run+"/ring_probes.csv")
    tail = df.tail(int(len(df)*0.2)).iloc[:,1:].values

    ring_std = np.std(tail, axis=1)
    print("\nAngular Coherence (Std Dev):")
    print(f"  Min:  {ring_std.min():.4f}")
    print(f"  Mean: {ring_std.mean():.4f}")
    print(f"  Max:  {ring_std.max():.4f}")

    fft = np.abs(np.fft.fft(tail,axis=1))[:,:tail.shape[1]//2]
    avg = fft.mean(axis=0)
    modes = sorted(enumerate(avg), key=lambda x:x[1], reverse=True)

    print("\nDominant Angular FFT Modes:")
    for i,(m,v) in enumerate(modes[:5]):
        tag = "(DC Offset)" if m==0 else ""
        print(f"  {i+1}. Mode {m:2d} (|X|={v:.4e}) {tag}")

    with open(run+"/ring_modes.json","w") as f:
        json.dump({
            "run":run,
            "dominant_modes":[{"mode":int(m),"mag":float(v)} for m,v in modes[:10]],
            "avg_coherence":float(ring_std.mean())
        },f,indent=2)

    print("\nAnalysis Complete.")

if __name__ == "__main__":
    analyze_latest()
    

