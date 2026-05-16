"""Ring-probe angular FFT analysis. Identifies dominant poloidal mode m.

Usage:
    from analysis.ring_modes import mode_spectrum, dominant_mode
    spec = mode_spectrum(probes_array)   # shape (T, 64)
    m_dom, signal = dominant_mode(spec, exclude_dc=True)
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path


def load_probes_csv(path: str | Path) -> np.ndarray:
    """Load ring_probes.csv -> (T, 64) array. First column is step, drop it."""
    df = pd.read_csv(path)
    if "step" in df.columns:
        df = df.drop(columns=["step"])
    return df.to_numpy()


def mode_spectrum(probes: np.ndarray) -> np.ndarray:
    """FFT along the angular axis (64 probes). Returns |FFT|^2 averaged
    over time, shape (33,) for the positive-frequency half of 64-pt FFT.
    """
    fft = np.fft.rfft(probes, axis=1)
    power = (np.abs(fft) ** 2).mean(axis=0)
    return power


def dominant_mode(spectrum: np.ndarray, exclude_dc: bool = True) -> tuple[int, float]:
    """Return (mode_number, signal) of dominant non-DC mode by default."""
    s = spectrum.copy()
    if exclude_dc:
        s[0] = 0.0
    m = int(np.argmax(s))
    return m, float(s[m])


def mode_ratio(spectrum: np.ndarray, m: int) -> float:
    """Ratio of mode m to DC (zonal flow proxy in ring-probe sense)."""
    if spectrum[0] <= 0:
        return 0.0
    return float(spectrum[m] / spectrum[0])


def quartered_spectrum(probes: np.ndarray, n_quarters: int = 4):
    """Yield (q_index, spectrum) for each quarter of the time series."""
    T = probes.shape[0]
    width = T // n_quarters
    for q in range(n_quarters):
        s = probes[q * width:(q + 1) * width]
        yield q + 1, mode_spectrum(s)
