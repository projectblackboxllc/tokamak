"""Energy confinement time tau_E estimator.

In real tokamaks: tau_E = stored_energy / heating_power.

In the TOU/Tolkamak simulation: stored_energy is the steady-state mean of
E_phi (potential field energy density). Heating power is dominated by
the noise injection rate, which has variance per step scaling like
noise_amp^2 * dt.

Two estimators are provided:
- tau_E_proxy: steady-state E_phi / noise variance per unit time (cheap)
- tau_E_decay: e-folding time of E_phi decay after noise is cut (gold standard,
  requires a separate decay run)
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path


def tau_E_proxy(df: pd.DataFrame, noise_amp: float, dt: float = 0.12,
                frac: float = 0.5) -> float:
    """Cheap confinement-time proxy: steady-state E_phi over drive rate."""
    n = len(df)
    ss = df.iloc[int(n * (1 - frac)):]
    E_mean = ss["E_phi"].mean()
    drive_rate = (noise_amp ** 2) / dt
    return float(E_mean / (drive_rate + 1e-12))


def tau_E_decay(E_timeseries: np.ndarray, dt_metric: float) -> float:
    """e-folding time of an energy decay curve.

    E_timeseries: 1D array of E_phi after noise is cut.
    dt_metric: time between metric samples (NOT engine dt).
    """
    E = np.asarray(E_timeseries, dtype=float)
    if E.size < 3 or E[0] <= 0:
        return 0.0
    # log-linear fit
    valid = E > 0
    if valid.sum() < 3:
        return 0.0
    t = np.arange(E.size) * dt_metric
    logE = np.log(E[valid])
    slope, _ = np.polyfit(t[valid], logE, 1)
    if slope >= 0:
        return float("inf")  # not decaying
    return float(-1.0 / slope)


def scaling_exponent(tau_E_array: np.ndarray, drive_array: np.ndarray) -> float:
    """Power-law scaling exponent of tau_E vs drive (ITER-style scaling)."""
    valid = (tau_E_array > 0) & (drive_array > 0)
    if valid.sum() < 3:
        return 0.0
    slope, _ = np.polyfit(np.log(drive_array[valid]), np.log(tau_E_array[valid]), 1)
    return float(slope)
