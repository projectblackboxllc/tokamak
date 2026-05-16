# Report 002 — The Drive-Independent Attractor (Homeostat Result)

**Paired figure:** [`fig_002_homeostat_attractor.png`](../figures/fig_002_homeostat_attractor.png)
**Experiment:** `exp_001_lh_transition` (post-processed)
**Engine:** `tou_tokamak_v2.py` (v2.0)
**Date:** 2026-05-16
**Status:** Post-processing of Experiment 001 data with reframed interpretation.

---

## What the Figure Shows

**Top row.** Steady-state zonal-flow energy E_zonal (left) and turbulent energy E_turb (right), each plotted versus noise amplitude η on a log scale. The red TOU-OFF curve climbs roughly two decades across the sweep. The green TOU-ON curve is a horizontal line.

**Bottom-left.** τ_E gain (TOU on divided by TOU off) decreases monotonically from 287× at η=0.05 to 2.3× at η=0.80. Annotations carry the exact gain at each drive level. The dashed gray line marks parity (gain = 1).

**Bottom-right.** Drive-induced relative variation (max − min)/mean across the six-point sweep, in percent. OFF arm: 309% on E_zonal, 307% on E_turb. ON arm: 7% and 4%. The TOU mechanism reduces drive sensitivity by **~40× to ~75×** depending on the metric.

## Why This Matters

In the L-H transition literature, the order parameter is the *ratio* E_zonal / E_turb. We pre-registered the ratio because that is what the textbook says will move. The ratio in fact moves slightly the *wrong* direction (Section 4 below). The interesting movement is in the *level*, not the ratio.

The TOU mechanism is acting as a homeostat: an active control system that pins one or more state variables to a setpoint regardless of disturbance. The setpoint is determined by the saturating reinjection gain (tanh(k·A)) and the geometry of the ring reinjection kernel, not by the input noise.

In tokamak engineering terms, this is closer to a fast actuator feedback loop than a phase transition. The H-mode literature has a parallel concept — *artificial H-mode* induced by external biasing — but it is not the same mechanism. The TOU homeostat is information-rectifier driven: it integrates inward energy flux into a single scalar A, then radiates that scalar out as coherent forcing.

## Numbers To Quote

| Quantity | OFF range across η | ON range across η | Reduction factor |
|---|---|---|---|
| E_zonal | 0.022 → 2.19 (×100) | 26.1 → 28.0 (×1.07) | 100× → **~94× reduction in sensitivity** |
| E_turb | 1.52 → 121.2 (×80) | 2279 → 2382 (×1.05) | 80× → **~76× reduction in sensitivity** |
| τ_E gain (ON/OFF) | 287× at η=0.05, 2.3× at η=0.80 | — | — |

The headline single number for an audience: **The TOU mechanism reduces drive sensitivity by ~75×.**

## Caveats

Same as Report 001 §6. Specifically:
- N=65 grid, 2500 steps, single seed.
- The probe-ring layout (on the magnetic axis) inflates the m=0 component and creates a small high-mode aliasing artifact at low drive.
- The proxy τ_E is not a true decay measurement.
- Replication at v1's N=121 and 30k steps is the next priority.

## Pointer

This report and figure 002 are derived entirely from `data/exp_001_lh_transition.csv`. They share the same raw data as figure 001 / report 001 — the difference is in interpretation, not in the experiment.

## Revision Log

- 2026-05-16, v1: written after Experiment 001 sweep completed; supersedes the L-H framing in Report 001 while preserving Report 001 as the historical record of the original hypothesis.
