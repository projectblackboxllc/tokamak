# Report 001 — Experiment 001 Headline Result

**Paired figure:** [`fig_001_lh_phase_diagram.png`](../figures/fig_001_lh_phase_diagram.png)
**Experiment:** `exp_001_lh_transition` (`experiments/exp_001_lh_transition.py`)
**Engine:** `tou_tokamak_v2.py` (v2.0)
**Date:** 2026-05-16
**Status:** First-pass result. Hypothesis revised mid-experiment (see §2). Replication at higher N pending.

---

## TL;DR

The TOU accumulator did **not** reproduce the textbook L-H transition signature (where E_zonal/E_turb rises monotonically with drive). It produced something more striking: a **drive-independent attractor**. Across a 16× span of noise amplitude (5% to 80%), every measured energy quantity in the TOU-ON arm is essentially constant.

| Noise η | E_zonal(ON) | E_turb(ON) | Ez/Et (ON) |
|---|---|---|---|
| 0.05 | 26.4 | 2315 | 0.0114 |
| 0.10 | 26.4 | 2312 | 0.0114 |
| 0.20 | 26.1 | 2279 | 0.0114 |
| 0.40 | 26.5 | 2299 | 0.0115 |
| 0.60 | 27.1 | 2333 | 0.0116 |
| 0.80 | 28.0 | 2382 | 0.0118 |

The TOU OFF control, by contrast, scales with drive exactly as ordinary noise-driven physics would:

| Noise η | E_zonal(OFF) | E_turb(OFF) | Ez/Et (OFF) |
|---|---|---|---|
| 0.05 | 0.022 | 1.52 | 0.0145 |
| 0.10 | 0.047 | 2.93 | 0.0162 |
| 0.20 | 0.149 | 8.56 | 0.0175 |
| 0.40 | 0.558 | 31.1 | 0.0179 |
| 0.60 | 1.24 | 68.6 | 0.0180 |
| 0.80 | 2.19 | 121.2 | 0.0181 |

E_zonal in the OFF arm spans **100×**. In the ON arm it spans **6%**. That is the central finding of this experiment.

---

## 1. Question Posed and Question Answered

**Posed:** Does the TOU accumulator amplify the natural L-H transition (zonal flow rising, turbulence falling, ratio crossing a threshold)?

**Answered:** No — but for a more interesting reason. The accumulator does not amplify the L-H mechanism; it **bypasses** it. Once the accumulator saturates (which it does at every noise level within a few hundred steps), the reinjection forcing is essentially constant, and the system relaxes to a fixed energy state determined by the engineered forcing, not by the input noise.

The L-H transition framework assumes natural Reynolds stress is the only zonal-flow driver. The TOU mechanism replaces Reynolds stress with a designed, saturating actuator. The natural transition signature disappears because the natural mechanism is no longer the dominant one.

## 2. Hypothesis Revision

The pre-experimental hypothesis (in the original experiment design) was that TOU would amplify the Ez/Et ratio. The data refutes this. The revised hypothesis, post-data:

> The TOU accumulator-reinjector pair is a noise-to-coherence rectifier with a saturating output. Above a (very low) noise threshold, it imposes a deterministic energy state on the system regardless of further noise. It is acting as a homeostat.

This is consistent with the v1 finding that Mode 4 emerged and persisted under 80% noise — the mechanism's job is to LOCK the system into a structured state. v2 shows that the locking is essentially independent of drive amplitude.

## 3. Confinement-Time Gain

The drive-normalized stored-energy proxy τ_E = ⟨E_φ⟩ / (η²/dt):

| Noise η | τ_E (OFF) | τ_E (ON) | Gain (ON/OFF) |
|---|---|---|---|
| 0.05 | 2,080 | 596,510 | **287×** |
| 0.10 | 1,868 | 150,099 | **80×** |
| 0.20 | 1,815 | 38,079 | **21×** |
| 0.40 | 1,802 | 10,916 | **6.1×** |
| 0.60 | 1,799 | 5,839 | **3.2×** |
| 0.80 | 1,798 | 4,067 | **2.3×** |

The gain monotonically decreases as drive increases, exactly because the ON arm's stored energy is constant while the OFF arm's drive normalization grows. At every drive level the gain is > 1: TOU confines more stored energy per unit drive than the natural mechanism. The amplification is largest at low drive — where the natural mechanism has the least to work with.

## 4. Dominant Ring Mode

| Noise η | Dominant m (OFF) | Dominant m (ON) | Note |
|---|---|---|---|
| 0.05 | 3 | 28 | ON arm aliasing — low absolute signal |
| 0.10 | 3 | 28 | "" |
| 0.20 | 3 | 28 | "" |
| 0.40 | 3 | **3** | Real attractor emerges |
| 0.60 | 3 | **3** | Stable |
| 0.80 | 3 | **3** | Stable |

At drive ≥ 0.40, **both arms select Mode 3** as the dominant non-DC poloidal mode. The natural drift-wave + curvature physics at this q-profile picks Mode 3. The TOU mechanism amplifies the SAME mode rather than imposing a different one — which is the right behavior for a non-disruptive controller.

(Note: this differs from v1's Mode 4 result. v1 used different geometry (N=121, q₀=1.05, q₁=3.0) and a much longer run (30,000 steps). Mode 3 vs Mode 4 is a function of the safety-factor profile and aspect ratio. The general claim — *a geometric attractor exists* — replicates; the specific mode does not need to.)

The m=28 result in the ON arm at noise ≤ 0.2 is almost certainly aliasing — at low drive the ring-probe signal is small and the probe-spacing on the N=65 grid (≈ 2 cells) makes high modes near Nyquist (m=32) susceptible to grid noise. A flux-surface probe layout would fix this and is on the followup list.

## 5. What This Means for Real Plasma Physics

Honestly: this is a numerical experiment, and the TOU mechanism is engineered, not derived from microscopic plasma equations. The mapping to real tokamak physics is by analogy:

- Accumulator ↔ engineered Reynolds-stress collection
- Reinjection ↔ engineered coherent E×B forcing
- Mode-3 (or Mode-4) attractor ↔ low-m poloidal mode preference

If the analogy holds even loosely, the implication is interesting: an external actuator that delivers a saturating, phase-coherent poloidal forcing could in principle pin a real plasma to a structured, drive-independent state — a kind of artificial H-mode by direct construction rather than by triggering the natural L-H transition.

We are not claiming this works in a real plasma. We are claiming it works in this numerical model, and the mechanism is small enough that anyone can inspect it.

## 6. Limitations

- **N = 65 grid.** Smaller than v1's 81/121. High-resolution replication is the next experiment.
- **2500 steps with 2000-step noise ramp.** Only the last 500 steps see full noise; steady-state windowing is the second half (last 1250 steps), which averages over the ramp tail. A longer-step replication will sharpen this.
- **Single seed (42).** Stochastic robustness requires ensemble runs.
- **τ_E is a proxy.** Not a true decay measurement. A decay-style follow-up (cut noise, measure e-folding) is planned.
- **Ring probes at magnetic axis.** This biases the DC component and creates near-Nyquist aliasing at low drive in the ON arm. A flux-surface probe layout would clean this up.
- **L-H framing was the wrong question.** The experiment still answered something interesting; the original framing has been replaced (§2).

## 7. Followups

| # | Question | Status |
|---|---|---|
| F1 | Does the attractor persist at N=121 and 30,000 steps? | not started |
| F2 | What is the saturation curve (E_zonal vs accumulator-leak) holding noise fixed? | not started |
| F3 | What does an ensemble of 16 seeds look like at one noise level? | not started |
| F4 | Do flux-surface probes recover Mode 3 cleanly at all drives, eliminating the m=28 artifact? | not started |
| F5 | At what α (adiabaticity) does the attractor disappear? Is there an α threshold? | not started |

## 8. Data Pointers

- Aggregated CSV: [`data/exp_001_lh_transition.csv`](../data/exp_001_lh_transition.csv)
- Per-run outputs: see `off_run_dir` and `on_run_dir` columns of the CSV
- Frame manifest: [`videos/frame_data/exp_001_frames.json`](../videos/frame_data/exp_001_frames.json)
- Paired figure: [`figures/fig_001_lh_phase_diagram.png`](../figures/fig_001_lh_phase_diagram.png)

## 9. Note on Naming

The figure and report carry the slug `lh_phase_diagram` because the experiment was designed to test the L-H hypothesis. The slug is preserved for traceability — what we set out to test, vs what we found. A follow-up figure with the homeostat framing is filed as `fig_002_homeostat_attractor.png` / `report_002_homeostat_attractor.md`.

## 10. Revision Log

- 2026-05-16, v1: auto-generated from `exp_001_lh_transition.py`. L-H framing assumed. Replaced.
- 2026-05-16, v2 (this version): rewritten after the sweep completed. Homeostatic-attractor interpretation introduced. Figure 001 unchanged (it shows the attractor signature clearly — green ON line is flat across drive); figure 002 added with explicit attractor framing.
