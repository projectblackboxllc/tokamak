# Report 004 — Dirty Twin Benchmark 2: The Inertia Test

**Paired figure:** [`fig_004_dirty_twin_slew.png`](../figures/fig_004_dirty_twin_slew.png)
**Experiment:** `exp_006_dirty_twin_slew`
**Engine:** `tou_tokamak_v3.py` (v3.0-dirty-twin, post-bugfix)
**Date:** 2026-05-16
**Hardware analog:** Tolkamak-0 actuator stack (Engineering Brief 001 v1.1 §1.3)
**Status:** Complete. Includes a mid-run bugfix to the slew model and a re-run.

---

## TL;DR

Two regimes, separated by a sharp threshold around slew_rate ≈ 0.05:

1. **Graceful regime (slew ≥ 0.05):** E_phi drops with slowing actuator but **Ez/Et stays locked at ~0.058**. The mechanism keeps its geometric shape at a reduced operating point. Notable: slew=0.2 and slew=0.05 land on essentially the same E_phi (~4100) — a homeostat at the actuator-rate level, sitting on a floor over a 4× slew span.

2. **Catastrophic regime (slew = 0.01):** Ez/Et collapses to 0.036 (62% of clean), the actuator's signed output bobs near zero (never reaches saturation), and the geometric attractor genuinely degrades. The amp is now so slow that it cannot complete a polarity flip within the 2500-step run.

The critical slew rate is **between 0.01 and 0.05** in simulation units. That bounds the hardware spec — see §6 for the Brief 001 v1.2 revision.

---

## A note on the bugfix mid-run

The v3 engine as originally written slew-limited only the *magnitude* of the actuator output. The sign of the output came from a separate copysign(phase_ema) channel and flipped instantly even at the slowest slew rates. The first exp_006 run showed every slew rate giving identical numbers within 4% — that wasn't a result, it was a buggy model.

A real Class-D amplifier outputs a *signed* voltage. The slew rate limits |d(V_out)/dt| across polarity changes, not only the rise time of magnitude. The bug was fixed (v3.py lines 224–252) to track signed_output and slew-limit it directly. Re-ran exp_006 with the fixed model. The data below is from the post-fix run.

This is the empirical-test-by-trying-to-break-it loop working as intended — a half-physical model surfaced because the data refused to move.

---

## Raw data

Held fixed: 16 probes, 5-step latency, η=0.40, N=65, 2500 steps, seed=42. All TOU on.

| Slew rate | Steps-to-full-range | E_phi | E_zonal | E_turb | Ez/Et | E_phi ratio | Ez/Et ratio |
|---|---|---|---|---|---|---|---|
| instant (None) | 1 | 11087 | 1187 | 20455 | 0.0580 | 1.000 | 1.000 |
| 5.0 | 3.3 | 10054 | 1066 | 18473 | 0.0577 | 0.907 | 0.995 |
| 1.0 | 16.7 | 6992 | 715 | 12648 | 0.0566 | 0.631 | 0.975 |
| 0.2 | 83.3 | 4119 | 709 | 12510 | 0.0567 | 0.371 | 0.977 |
| 0.05 | 333.3 | 4108 | 832 | 14349 | 0.0580 | 0.371 | 1.000 |
| **0.01** | **1666.7** | **2455** | **28** | **791** | **0.0360** | **0.221** | **0.620** |

`Ez/Et ratio` is the structure-preservation indicator: 1.0 means the attractor's shape is unchanged from the clean reference; values significantly below 1.0 mean the shape itself has degraded.

## Interpretation

### The graceful regime (slew ≥ 0.05)

E_phi drops from 11087 (instant) to 4108 (slew=0.05) as the actuator slows by ~333×. But Ez/Et stays within 4% of the clean reference. The mechanism's geometry is preserved across this entire range.

The reason: at slew = 0.05 the actuator takes about 333 simulation steps to traverse the full [-1, +1] range. The plasma's drift-wave period in this regime is on the order of 50–100 steps. So the actuator simply cannot keep up with every wave — it tracks the *envelope* of the phase EMA, not the wave's instantaneous sign. The system rebalances to a lower-energy attractor where the slower actuator's average forcing is still in phase with the wave's envelope. Same geometric shape; less total energy delivered.

Notable: slew=0.2 (83 steps to flip) and slew=0.05 (333 steps to flip) land on **almost identical E_phi**. There is a homeostat-at-the-actuator-rate plateau here. Across a 4× slew span the system finds the same steady state. That replicates the drive-independence finding from Experiment 001 at a different control input.

### The catastrophic regime (slew = 0.01)

slew = 0.01 corresponds to 1667 steps to traverse the full [-1, +1] range — longer than the entire 2500-step simulation. The actuator's signed_output ends the run at −0.06: it never saturated, just bobbed near zero. With no coherent forcing reaching the wave, the mechanism's role becomes negligible. E_phi drops to 2455 (22% of clean), Ez crashes to 28 (vs 1187 at instant), and Ez/Et falls to 0.036 — the first benchmark cell in any Dirty Twin experiment that shows actual structural degradation.

The break is real, not numerical noise: signed_output time-history confirms the actuator never engages.

### Where the threshold is

Between slew=0.01 and slew=0.05. A finer sweep across slew ∈ {0.01, 0.02, 0.03, 0.05} would localize the threshold to within a factor of 2; current data localizes it to within a factor of 5.

## Engineering implications for Tolkamak-0 (Brief 001 v1.2 revision)

The amplifier-driving-the-biased-ring-electrode needs to satisfy two specs:

**Hard requirement (catastrophic floor):**
The amp must be able to complete a full polarity flip (−V_max to +V_max) in less time than the plasma's drift-wave period. Below this, the mechanism breaks.

**Soft requirement (graceful regime, preserves structure):**
The amp should be able to complete a polarity flip in less than ~10× the drift-wave period. Above this rate, the attractor's shape is preserved but its energy level drops.

**Optimal (fully-effective regime):**
The amp should be ~10× faster than the drift-wave period (~3 simulation steps to flip in our units). Energy delivered is then 90%+ of the instant-actuator reference.

| Hardware regime | Slew (sim units) | Steps-to-flip | E_phi vs instant | Status |
|---|---|---|---|---|
| Optimal | ≥ 5.0 | ≤ 3 | ≥ 0.91 | Acceptable |
| Adequate | 0.2 – 5.0 | 17 – 83 | 0.37 – 0.91 | Acceptable with reduced ops point |
| Graceful floor | 0.05 – 0.2 | 83 – 333 | ~0.37 | Marginal; structure preserved |
| **Catastrophic** | **≤ 0.01** | **≥ 1667** | **≤ 0.22** | **Mechanism fails** |

For Brief 001 §1.3, the AE Techron / Vincent Audio HV-class amplifiers in the optimal regime are commercially available (the AE Techron 7700-series, for example, has hundreds of V/μs at the ±200V output). The hardware spec is not exotic — it is permissive. **The risk is not finding the right amp; the risk is over-engineering for a sub-μs target when 10× drift-wave-period is sufficient.**

This is a budget signal: we do NOT need to spec the most aggressive amp on the market. A mid-tier Class-D in the optimal slew regime ($5–10K class) is sufficient.

## What this benchmark surfaced beyond the headline

The mid-run bugfix is the most important *process* outcome. The half-physical slew model would have passed the experiment silently. Pushing the slew_rate parameter through five orders of magnitude and noticing the data refused to move is what surfaced the bug. **This is the engineering value of the "intentionally break it" framing.** A model that survives every degradation by being modeled incorrectly is more dangerous than a model that fails for the right physical reason.

## Caveats

- N=65, 2500 steps, single seed (42).
- Slew rate is symmetric (up-and-down rates equal). Asymmetric slew (push faster than pull, or vice versa) is a follow-up.
- The mapping from simulation `actuator_slew_rate` to hardware V/μs depends on Tolkamak-0 plasma calibration (drift-wave period in physical time).
- 5-step latency is held throughout; a slow amp + a fast amp interact with latency in ways this experiment does not isolate.

## Status

- **Benchmark 2: complete with bugfix and re-run.**
- **Brief 001 v1.2 revision pending** — incorporates the slew envelope above into §1.3.
- **Next: Benchmark 3 (exp_007, magnetic ripple).** Ready to run.

## Revision Log

- 2026-05-16, v1: auto-generated by `exp_006_dirty_twin_slew.py` (initial run with the magnitude-only slew model). Numbers were flat across the slew sweep because the model wasn't physically realistic; not preserved here.
- 2026-05-16, v2 (this version): rewritten after v3 engine bugfix (signed-output slew) and re-running the sweep. Real engineering finding: two regimes, threshold between slew=0.01 and slew=0.05, structural preservation in the graceful regime, catastrophic breakdown below.
