# TOU Engine (Toroidal Oscillatory Unit) — 3D

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20245905.svg)](https://doi.org/10.5281/zenodo.20245905)
[![Companion v1 Software](https://img.shields.io/badge/Companion%20v1%20(software)-10.5281%2Fzenodo.18450491-blue)](https://doi.org/10.5281/zenodo.18450491)
[![Site](https://img.shields.io/badge/site-projectblackboxllc.github.io%2Ftokamak-blue)](https://projectblackboxllc.github.io/tokamak/)

Author: Andrew Woodward  
ORCID: [0009-0006-9717-7161](https://orcid.org/0009-0006-9717-7161)  
Affiliation: Project Black Box LLC (CAGE Code 11FU4)  
Source: https://github.com/projectblackboxllc/tokamak  
Version: v1.2 (whitepaper) / v1.0 (this engine)  

**Whitepaper PDF:** [`papers/plain_language/v1.2/tokamak_zenodo_v1.2.pdf`](papers/plain_language/v1.2/tokamak_zenodo_v1.2.pdf) · **Live site:** https://projectblackboxllc.github.io/tokamak/

---

## Overview

The TOU Engine is a three-dimensional toroidal wave simulation designed to
study nonlinear wave dynamics, geometry-driven mode formation, and
self-organization under stochastic perturbation.

The system evolves a scalar wave field constrained to a toroidal manifold
and incorporates nonlinear energy accumulation and phase-sensitive
reinjection. Under both nominal and high-noise conditions, the system
exhibits persistent angular mode structure.

This project demonstrates:

- Emergent angular mode locking driven by geometry
- Long-horizon stability under sustained stochastic forcing
- Nonlinear feedback–mediated self-organization
- Robust recovery of dominant modes after perturbation

This codebase is a numerical physics experiment focused on wave dynamics
in closed manifolds.

---

## Tokamak Extension — Findings (May 2026)

### tou_tokamak.py

The TOU engine was extended to Tokamak magnetic confinement geometry by adding:

- **Safety factor profile** `q(r) = q₀ + q₁(r/a)²` — defines field-line winding pitch across the minor radius
- **Parallel gradient operator** `∇_∥` — perturbations propagate along field lines, not Cartesian axes
- **Coupled density field `n`** — drift-wave two-field system: density drives potential, potential drives density
- **All TOU mechanisms preserved unchanged** — accumulator, phase-sensitive reinjection, 64 ring probes

### Three-Run Progression

**Run 1** (`κₙ=0.08`, accumulator standard):
Drift-wave instability saturated the accumulator (inj=1.0). Mode 4 present but buried at rank 5 behind high harmonics. DC component dominant.

**Run 2** (`κₙ=0.02`, accumulator standard):
Drive reduced 4×. Mode structure identical — same harmonic family, Mode 4 still rank 5. Confirmed: mode structure is invariant to drive strength at saturation.

**Run 3** (`κₙ=0.02`, `leak=0.15`, `k=5×10⁻⁵`):
Accumulator allowed to breathe — 373/800 steps operating proportionally (inj < 0.99).
**Mode 4 rose to rank 2, signal 15,129 vs. 3,232 in saturated runs — 4.7× stronger.**

### Key Finding

When the TOU accumulator operates proportionally (not fully saturated), the Tokamak geometry naturally selects **Mode 4** as the dominant drift-wave mode — the same geometric attractor the original TOU engine finds in the scalar wave case.

The DC component (Mode 0) is physically correct: in Tokamak confinement this is the **zonal flow** — the mean poloidal E×B circulation that self-regulates turbulence. The TOU accumulator is behaving as **Reynolds stress**: collecting inward turbulent energy flux and reinjecting it coherently, driving the emergence of zonal flow + Mode 4 drift-wave structure.

| TOU Mechanism | Tokamak Physics Analog |
|---|---|
| Inward energy accumulation | Reynolds stress driving zonal flow |
| Phase-sensitive reinjection | Coherent E×B forcing |
| Mode 4 poloidal attractor | Dominant drift-wave mode |
| DC component | Zonal flow suppressing higher turbulence |

### Maximum Stress Result (80% noise, q₀=1.05, 30,000 steps)

The system was subjected to the most extreme conditions tested:
- **80% noise amplitude** — near white noise, instant assault from step zero
- **q₀=1.05** — 5% above the kink instability boundary (q<1 triggers sawtooth collapse in real Tokamaks)
- **q₁=3.0** — steep safety factor gradient, severe field-line shear across minor radius
- **ping amplitude 10.0 every 50 steps** — continuous hard perturbation
- **30,000 steps**

**Mode 4 quarter-by-quarter evolution:**

| Quarter | Mode 4 signal | Rank (non-DC) |
|---|---|---|
| Q1 (steps 0–7500) | 29,010 | 1st |
| Q2 (steps 7500–15000) | 103,610 | 1st |
| Q3 (steps 15000–22500) | 179,330 | 1st |
| Q4 (steps 22500–30000) | 254,840 | 1st |

Mode 4 locked rank 1 (non-DC) from the first quarter and grew **monotonically** across all 30,000 steps. Final signal: **261,794** — 80.6× stronger than the first run.

**Geometric invariant discovered:** The Mode 4 / DC (zonal flow) ratio = **0.026** across both extreme runs (45% noise and 80% noise), despite different kappa_n, different step counts, and different q profiles. The ratio is fixed by the geometry, not the physics parameters.

### Principle Confirmed

*The harder the system is driven, the more inward energy flux the accumulator captures, and the more coherently it reinjects. Adversarial energy is converted into geometric order. The TOU does not resist turbulence — it absorbs and restructures it.*

**Mode 4 was never defined. Never seeded. Never explicitly coded.**
It emerges from toroidal geometry + radial accumulation + phase-sensitive reinjection alone.
It holds rank 1 under every condition tested, including Tokamak drift-wave physics at the kink instability boundary.
The geometry is the attractor. The attractor is Mode 4.

This is consistent with the behavior observed in all prior stress tests: noise does not destroy coherence. It funds it.

---

## Folder Structure

tou-engine-zenodo/
├── tou_engine3d.py          # Main simulation engine
├── tou_ring_analysis.py     # Post-run angular FFT analysis
├── requirements.txt
├── README.md
├── LICENSE
├── CITATION.cff
└── outputs/
└── run_STRESS_YYYYMMDD-HHMMSS/
├── metrics.csv
├── ring_probes.csv
├── ring_modes.json
├── diagnostics.png
├── final_slice.png
└── slices/
└── frame_000000.png

---

## Requirements

- Python 3.10+
- NumPy
- Matplotlib
- Pandas

Install dependencies:

```bash
pip install -r requirements.txt


⸻

Running the Engine

From the project directory:

python3 tou_engine3d.py

This will:
    •    Create a timestamped run directory under outputs/
    •    Execute the full simulation headlessly
    •    Save time-series diagnostics, angular probe data, and figures
    •    Export periodic slice images for visualization

⸻

Running Analysis

After a run completes:

python3 tou_ring_analysis.py

The analyzer will:
    •    Automatically select the most recent run directory
    •    Compute angular coherence statistics
    •    Perform FFT-based angular mode analysis
    •    Save results to ring_modes.json in the run directory

⸻

Scientific Notes
    •    Angular modes emerge without explicit symmetry enforcement
    •    Mode-4 dominance appears as a stable geometric attractor
    •    Harmonic structure (8, 12, 16, 20, 24) confirms genuine mode locking
    •    Noise does not destroy coherence; it is absorbed by nonlinear feedback

⸻

Disclaimer

This software is provided strictly for research and experimental use.
It makes no claims regarding propulsion, thrust, reactionless motion,
or applied engineering systems.

⸻

Citation

If you use this work, please cite it using the included CITATION.cff.

---

## Tokamak v2 — Experiment 001 Findings (May 2026, appended)

> Append-only section. v1 (above) describes the original Zenodo Mode-4 result with `tou_tokamak.py`. v2 introduces `tou_tokamak_v2.py` (with adiabaticity coupling, curvature drive, zonal/turbulent decomposition, JSON frame export) and a paired-run experiment infrastructure. v2 does NOT replace v1.

### Why this matters
This toroid was built to disprove two assumptions that run through most of physics and engineering: that systems respond linearly to drive, and that complex-system self-organization proceeds via discrete-state bifurcations. Experiment 001 disproves both, in the same data set, with one toggled mechanism. The drive-independent attractor reported below is the empirical disproof — not a curiosity. See `papers/plain_language/v1.0/tokamak_plain_v1.0.md` and `papers/technical/v1.0/tokamak_technical_v1.0.md` §6.6 for the full claim and its scope.

### What v2 adds
- Hasegawa-Wakatani-style adiabaticity coupling α(φ − n) between potential and density fields
- Bad-curvature drive κ_B
- Explicit zonal-flow / turbulent-energy decomposition (poloidal-mean vs fluctuation)
- A confinement-time proxy τ_E
- A `tou_on` flag isolating the TOU accumulator+reinjection mechanism from the underlying physics
- Per-step JSON frame export for video rendering

### Experiment 001 — paired-run drive sweep
Six noise levels (5%, 10%, 20%, 40%, 60%, 80%), each run twice (TOU ON, TOU OFF), all other parameters fixed (N=65, 2500 steps, α=0.5, κ_B=0.05, q₀=1.2, q₁=2.0).

### Headline result
TOU ON pins the system to a drive-independent energy state.

| Metric | OFF (range across 16× drive sweep) | ON (range across same sweep) |
|---|---|---|
| E_zonal | 0.022 → 2.19 (×100) | 26.1 → 28.0 (×1.07) |
| E_turb | 1.52 → 121.2 (×80) | 2279 → 2382 (×1.05) |
| Drive-induced variation | ~308% | ~5.5% |

Confinement-time gain (ON/OFF) is **287× at η=0.05** and **2.3× at η=0.80** — always positive, monotonically decreasing with drive.

At drive ≥ 0.40 both arms select Mode 3 as the dominant non-DC ring mode. (v1's Mode 4 was specific to N=121, q₀=1.05, q₁=3.0, 30k steps — the existence of a low-m geometric attractor replicates; the specific mode shifts with geometry.)

### Reframing
The pre-experiment hypothesis was a textbook L-H transition (zonal-to-turbulent ratio rising with drive). The data refutes that framing — the ratio is essentially flat in the ON arm. The empirical mechanism is a **saturating homeostat**: above a low drive threshold, the accumulator saturates (inj → 1.0) and the reinjection forcing becomes drive-independent. The system relaxes to a fixed energy state determined by the geometry and the saturation gain.

### Where to look
- Engine: `tou_tokamak_v2.py`
- Experiment orchestrator: `experiments/exp_001_lh_transition.py`
- Aggregated data: `data/exp_001_lh_transition.csv`
- Headline figure: `figures/fig_002_homeostat_attractor.png` (4-panel)
- Original sweep figure: `figures/fig_001_lh_phase_diagram.png`
- Reports: `reports/report_001_lh_phase_diagram.md` (rewritten post-data), `reports/report_002_homeostat_attractor.md` (homeostat reframe)
- Living state: `CLAUDE.md`

### Caveats
This is a first-pass result on a smaller grid (N=65) and shorter run (2500 steps) than the v1 published result. Replication at v1 conditions, ensemble runs across seeds, and flux-surface probe relayout are on the followup list. See `reports/report_001_lh_phase_diagram.md` §6-7 for the full limitations table.
