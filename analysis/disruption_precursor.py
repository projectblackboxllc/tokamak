"""Disruption-precursor analysis.

In real tokamaks, disruptions are sudden loss of confinement. Precursors
include: rising magnetic fluctuations, n=1 locked-mode amplitude, drop in
edge density. The TOU phase_ema and accumulator value are candidate
precursor signals — they integrate inward energy flux.

Two metrics:
- phase_ema rate-of-change |d(phase_ema)/dt|
- accumulator deviation from baseline
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path


def phase_ema_velocity(df: pd.DataFrame, window: int = 50) -> np.ndarray:
    """Rolling mean of |d(phase_ema)/dt|."""
    pe = df["phase_ema"].to_numpy()
    dpe = np.abs(np.diff(pe, prepend=pe[0]))
    s = pd.Series(dpe).rolling(window, min_periods=1).mean().to_numpy()
    return s


def acc_anomaly_score(df: pd.DataFrame, baseline_frac: float = 0.3,
                      z_threshold: float = 3.0) -> np.ndarray:
    """Z-score of accumulator vs early-time baseline.
    Returns array of same length; values > z_threshold = anomalous.
    """
    acc = df["acc"].to_numpy()
    n = len(acc)
    baseline_end = int(n * baseline_frac)
    mu = acc[:baseline_end].mean()
    sigma = acc[:baseline_end].std() + 1e-12
    return (acc - mu) / sigma


def precursor_lead_time(df: pd.DataFrame, energy_collapse_step: int,
                        z_threshold: float = 3.0) -> int:
    """Lead time (in steps) between precursor trigger and energy collapse.
    Positive = warning came BEFORE collapse.
    """
    z = acc_anomaly_score(df)
    steps = df["step"].to_numpy()
    triggered = np.where(z > z_threshold)[0]
    if len(triggered) == 0:
        return -1
    first_trigger_step = int(steps[triggered[0]])
    return energy_collapse_step - first_trigger_step
