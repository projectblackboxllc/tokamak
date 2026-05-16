"""Zonal-flow vs turbulence diagnostics from metrics.csv.

The L-H transition signature: zonal-flow energy grows, turbulent energy
collapses. Ratio Ez/Et crossing a threshold marks the transition.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path


def load_metrics(path: str | Path) -> pd.DataFrame:
    return pd.read_csv(path)


def steady_state_window(df: pd.DataFrame, frac: float = 0.5) -> pd.DataFrame:
    """Return the last `frac` of rows (drop transients)."""
    n = len(df)
    return df.iloc[int(n * (1 - frac)):]


def zonal_ratio(df: pd.DataFrame, frac: float = 0.5) -> float:
    """E_zonal / E_turb averaged over the steady-state window."""
    ss = steady_state_window(df, frac)
    ez = ss["E_zonal"].mean()
    et = ss["E_turb"].mean()
    return float(ez / (et + 1e-12))


def turbulence_suppression(df_off: pd.DataFrame, df_on: pd.DataFrame,
                           frac: float = 0.5) -> float:
    """Relative drop in turbulent energy with TOU on vs off.
    Positive value = TOU suppresses turbulence.
    """
    et_off = steady_state_window(df_off, frac)["E_turb"].mean()
    et_on = steady_state_window(df_on, frac)["E_turb"].mean()
    return float((et_off - et_on) / (et_off + 1e-12))


def zonal_amplification(df_off: pd.DataFrame, df_on: pd.DataFrame,
                        frac: float = 0.5) -> float:
    """How much more zonal-flow energy with TOU on vs off."""
    ez_off = steady_state_window(df_off, frac)["E_zonal"].mean()
    ez_on = steady_state_window(df_on, frac)["E_zonal"].mean()
    return float((ez_on - ez_off) / (ez_off + 1e-12))
