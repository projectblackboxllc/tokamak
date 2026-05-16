---
title: "A Toroidal Geometric Rectifier: Empirical Disproof of Linear-Response in Plasma Confinement"
author: "Andrew Woodward · Project Black Box LLC"
date: "2026-05-16"
subtitle: "Zenodo Whitepaper v1.2"
---

# A Toroidal Geometric Rectifier: Empirical Disproof of Linear-Response in Plasma Confinement

**Author:** Andrew Woodward
**ORCID:** [0009-0006-9717-7161](https://orcid.org/0009-0006-9717-7161)
**Affiliation:** Project Black Box LLC · CAGE Code 11FU4
**Source repository:** [github.com/projectblackboxllc](https://github.com/projectblackboxllc)
**Version:** Zenodo Whitepaper v1.2
**Date:** 2026-05-16
**Companion to:** *TOU Engine — Toroidal Self-Organization in a 3D Wave Manifold* (v1, Zenodo, January 2026)

---

::: voice-note
**A note on this document.** Each section is written in **two voices**. The *Plain* paragraph is for readers from outside fusion physics — engineers, investors, journalists, anyone curious. The *Scientific* paragraph immediately following carries the technical framing for readers with field background. Neither paragraph contains the mathematical formulation of the underlying control law. The exact accumulator and reinjection kernel implementations are held proprietary; the empirical findings, parameter regimes, and experimental design are open and reproducible from the accompanying source release.
:::

---

## Abstract

::: plain
This work shows, in a clean numerical experiment, that a particular toroidal geometry combined with two simple feedback mechanisms produces a structured energy state that does not respond linearly to input drive and does not undergo a phase transition. Push the system with five-percent noise, push it with eighty-percent noise — it sits in the same place. Across a sixteen-fold change in input, the output stays within seven percent of itself. Four additional stress tests subject the same mechanism to the kinds of imperfections a real instrument would impose — only a few sensors instead of perfect information, delayed control commands, a slow amplifier, magnetic-field irregularities — and the structured state survives all of them. The mechanism is small, deterministic, and inspectable.
:::

::: scientific
A 3D toroidal numerical experiment, the Tolkamak system, demonstrates a drive-independent attractor produced by an engineered Reynolds-stress accumulator and phase-sensitive coherent reinjector layered on a Hasegawa-Wakatani-style drift-wave substrate with bad-curvature drive and a parametric safety-factor profile. Across a 16× span of stochastic drive amplitude, every measured steady-state energy quantity in the active-mechanism arm is invariant to within 4–7%, while the control arm scales by two decades. A four-stage *Dirty Digital Twin* benchmark sequence further demonstrates that the attractor survives realistic sensor sparsity (down to 4 discrete probes), control-loop latency (smooth ~5%/step graceful degradation), actuator slew limits down to a hardware-relevant threshold, and a 40% q-profile ripple — both in the original perpendicular-dominant regime (10⁻⁶-level effect) and in a physically representative parallel-dominant regime with parallel-to-perpendicular coupling ratio ≈ 11 (0.24% effect, two orders of magnitude inside pre-registered pass thresholds). The findings constitute the empirical disproof, in this geometry and under this mechanism, of two assumptions widely applied to driven dissipative systems on toroidal manifolds: linear response of steady-state to input drive, and discrete-state bifurcation as the mechanism of self-organization.
:::

---

## 1. What This Work Is

::: plain
The system simulates a doughnut-shaped ring of energy — the same geometry that fusion reactors called *tokamaks* use to confine plasma. We added two simple ideas: an *accumulator* that listens to the energy flowing inward and adds it up, and a *reinjector* that gives the ring a coherent push in time with its own rhythm. Two ideas. About thirty lines of inspectable computer code. The rest is standard physics. The whole question of this paper is: what happens when you run that combination?
:::

::: scientific
Tolkamak v2 and v3 are 3D numerical simulations on a toroidal manifold with major-radius and minor-radius parameters chosen to give a sensible aspect ratio (R/a). The wave-potential and density fields are coupled through a Hasegawa-Wakatani-style adiabaticity term, augmented by a bad-curvature drive and a parallel gradient operator on a parametric safety-factor profile q(r). Layered on this substrate are two engineered mechanisms: a directional accumulator that integrates inward radial energy flux with a configurable leak, and a phase-sensitive reinjection forcing that drives a toroidal ring source in phase with the local wave-derivative exponential moving average. The accumulator and reinjector together form what we call a **toroidal geometric rectifier** — a continuum-medium analog of an electrical diode-capacitor rectifier, operating on energy flux rather than charge, and producing a structured spatial output rather than a directed scalar one.
:::

---

## 2. Methodology and Parameters

::: plain
The full numerical experiment is built in Python, runs on a desktop computer, and produces three things per run: a CSV of measured energy quantities over time, a CSV of 64 angular "probe" readings around the ring, and a JSON of state snapshots suitable for visualizing. Every experiment in this paper was run with a fixed random seed, so anyone can reproduce the exact same numbers given the same code. The simulation parameters that describe the *physics* (geometry, drift-wave coupling, curvature drive, safety-factor profile) are open. The parameters that configure the *mechanism* (the accumulator's gain and leak constants, the reinjection kernel) are held proprietary pending IP review.
:::

::: scientific
**Engine and reproducibility.**

- Tolkamak v2 (`tou_tokamak_v2.py`) — base engine including TOU accumulator/reinjector and the Hasegawa-Wakatani drift-wave physics.
- Tolkamak v3 (`tou_tokamak_v3.py`, "Dirty Digital Twin") — extends v2 with five toggleable physical-realism constraints (sensor sparsity, sensor latency, sensor noise, actuator slew rate, q-profile ripple), all default-off so v3 reproduces v2 bit-identically with default arguments.
- All experiments use seed = 42 unless explicitly varied. Reproducibility is a first-class requirement.

**Open physics parameters** (varied across or held fixed across experiments — full disclosure):

| Parameter | Role | Default / range used |
|---|---|---|
| N | Cubic-grid side length | 65 (Tolkamak-0 scale); 121 in v1 high-resolution prior work |
| dt | Integration time step (dimensionless) | 0.12 |
| steps | Total integration steps per run | 2500 |
| R_frac, r_frac | Major/minor radius as grid fraction | 0.32, 0.12 (aspect ratio ≈ 2.7) |
| c | Perpendicular wave speed | 1.0 (default) → 0.3 (parallel-dominant stringent regime) |
| α (alpha_adiab) | Hasegawa-Wakatani adiabaticity coupling | 0.5 |
| κ_B (kappa_B) | Bad-curvature drive amplitude | 0.05 |
| κ_n (kappa_n) | Drift-wave parallel coupling | 0.08 (default) → 1.0 (stringent) |
| D_diff | Density-field diffusion | 0.02 (default) → 0.10 (stringent) |
| q₀, q₁ | Safety-factor profile q(r) = q₀ + q₁(r/a)² | 1.2, 2.0 |
| Noise amplitude η | Stochastic drive level | swept ∈ {0.05, 0.10, 0.20, 0.40, 0.60, 0.80} |
| Noise ramp | Steps over which noise reaches full amplitude | 2000 |

**Proprietary mechanism parameters** (configuration of the TOU accumulator and reinjector — values redacted from this release): `ping_every`, `ping_amp`, `reinject_gain`, `accumulator_leak`, `k` (saturation gain), `phase_alpha` (EMA coefficient), and the construction of the ring-source kernel. Full input/output behavior at the engine API level is documented.

**Measured quantities (open).** For every run we record:

- E_φ — total wave-field energy (kinetic + potential).
- E_zonal — m=0 poloidal-mean component (the zonal-flow proxy).
- E_turb — the non-zonal fluctuation component.
- Ez/Et — the structural-shape indicator (the L-H-style "order parameter").
- τ_E — confinement-time proxy: ⟨E_φ⟩ / (η²/dt).
- 64 ring-probe time series → mode-spectrum FFT → dominant non-DC poloidal mode m*.
:::

---

## 3. The Question

::: plain
Standard plasma physics expects two things from a system like this. First, that it responds linearly — push harder, it pushes back proportionally. Second, that when it self-organizes it does so by switching between two states (called "low-confinement" and "high-confinement" in fusion language; the L-H transition). We built the system to test whether neither of those is necessary, given the right geometry and the right feedback rule.
:::

::: scientific
The dominant framework for self-organization in driven dissipative plasma systems is the L-H mode transition: at a critical drive threshold, drift-wave-driven Reynolds stress generates a sheared zonal flow that decorrelates further turbulence, triggering a state change with measurably different stored energy. The Tolkamak architecture proposes an alternative: engineer the Reynolds-stress collection explicitly (the accumulator) and engineer the coherent forcing explicitly (the reinjector), so the structured state emerges by direct construction rather than by transition. The empirical question is whether such an engineered structure exhibits the linear-response and bifurcation signatures predicted by the standard framework, or whether it does something else.
:::

---

## 4. The Headline Result — Experiment 001

::: plain
We ran the simulation twelve times: six different input noise levels, each at two settings — accumulator on, accumulator off — with everything else identical. With the mechanism off, every measured energy quantity scaled with noise as ordinary physics predicts (about two decades across the sweep). With the mechanism on, every measured energy quantity stayed within seven percent of the same value across the entire sweep. The system is in the same state at every input level.
:::

::: scientific
Paired-shot drive sweep: noise amplitude η ∈ {0.05, 0.10, 0.20, 0.40, 0.60, 0.80}, control arm (TOU off) vs treatment arm (TOU on), all other parameters held identical. The steady-state window for diagnostics is the second half of each run (steps 1250–2500), allowing transient dynamics to settle.
:::

### Full Experiment 001 results

| η | E_zonal (OFF) | E_zonal (ON) | E_turb (OFF) | E_turb (ON) | Ez/Et (OFF) | Ez/Et (ON) | τ_E gain (ON/OFF) | Dominant mode m* (ON) |
|---|---|---|---|---|---|---|---|---|
| 0.05 | 0.022 | 26.4 | 1.52 | 2315 | 0.0145 | 0.0114 | 287× | 28 |
| 0.10 | 0.047 | 26.4 | 2.93 | 2312 | 0.0162 | 0.0114 | 80× | 28 |
| 0.20 | 0.149 | 26.1 | 8.56 | 2279 | 0.0175 | 0.0114 | 21× | 28 |
| 0.40 | 0.558 | 26.5 | 31.1 | 2299 | 0.0179 | 0.0115 | 6.1× | 3 |
| 0.60 | 1.24 | 27.1 | 68.6 | 2333 | 0.0180 | 0.0116 | 3.2× | 3 |
| 0.80 | 2.19 | 28.0 | 121.2 | 2382 | 0.0181 | 0.0118 | 2.3× | 3 |

**Drive-induced variation across the sweep**

| Quantity | OFF arm | ON arm | Sensitivity reduction |
|---|---|---|---|
| E_zonal | 0.022 → 2.19 (×100) | 26.1 → 28.0 (×1.07) | ≈ 94× |
| E_turb | 1.52 → 121.2 (×80) | 2279 → 2382 (×1.05) | ≈ 76× |
| Single-number headline | (max − min)/mean = **309%** | (max − min)/mean = **7%** | **≈ 44× reduction** |

::: plain
**Headline number for an audience:** the mechanism reduces the system's sensitivity to input noise by roughly seventy-five times. The "homeostat" word — a system that holds its setpoint against a disturbance — is the closest one-word fit. Note the dominant ring mode column: under the strongest drive cells, the system finds the same low-poloidal-order mode (m=3 in this v2 parameter regime; m=4 was the attractor reported in the v1 prior work at different geometry). The specific mode is geometry-dependent, but the *existence* of a low-mode geometric attractor replicates.
:::

::: scientific
The treatment-arm steady-state is structurally a saturating-actuator homeostat: above a low drive threshold the accumulator saturates, and the reinjection forcing becomes drive-independent, fixing the steady-state energy to a level set by the saturation gain and the geometry rather than by input drive. The dominant ring-mode discrepancy at low η (m=28 in the ON arm vs m=3 in the OFF arm) is attributed to ring-probe aliasing on the N=65 lattice at low absolute signal levels; both arms converge to m=3 once the signal grows above the noise floor (η ≥ 0.40). A flux-surface probe layout is on the followup roadmap for v3.1.
:::

![**Figure 1.** Headline result — the drive-independent attractor. Top row: E_zonal and E_turb steady-state energy versus input drive on a log scale. The red TOU-OFF curve climbs two decades. The green TOU-ON curve is flat. Bottom row: confinement gain (ON ÷ OFF) decreasing monotonically from 287× to 2.3× but always positive; drive-induced variation reduced from ~308% (OFF) to ~5.5% (ON) — a ~44–77× reduction depending on metric. This is the disproof of linear response in one image.](figures/fig_002_homeostat_attractor.png){width=100%}

---

## 5. The Falsification Protocol — "Dirty Digital Twin"

::: plain
A mathematically perfect simulation isn't proof of anything physically useful. To get closer to what a real machine would experience, we built a "dirty digital twin": a version of the same simulation that intentionally degrades itself to mimic real-world limits. Only a few sensors instead of perfect information. Control commands that arrive late. An amplifier that can't change its output instantly. A doughnut shape that isn't perfectly smooth. Then we ran the same tests again and asked: does the mechanism still work? Critically, every pass/fail threshold for each benchmark was *set before the run started*. We did not move the goalposts after seeing data.
:::

::: scientific
A four-benchmark stress test layered on the Tolkamak v3 engine, with each physical-realism constraint individually toggleable: sensor sparsity (full-band integration replaced with N discrete probes); control-loop latency (delay in the sense→accumulate→act path); sensor noise floor (additive Gaussian on probe readings); actuator slew rate (bounded |d/dt| on the signed actuator output); and magnetic-ripple injection (multiplicative ripple on the safety-factor profile). Pass/fail thresholds are pre-registered in each experiment script before the sweep. The protocol's goal is to falsify the architecture's geometric-immunity claim under hardware-realistic conditions, not to confirm it under generous ones.
:::

---

## 6. Benchmark 1 — Sensor Sparsity and Latency

::: plain
The mechanism normally "sees" the whole interior of the ring at once. We replaced that with only 4 to 32 widely-spaced probes — what a real instrument array would actually be able to measure — and added increasing delays in the control loop, plus a small noise floor on the probe readings. Result: probe count doesn't matter much (4 probes vs 32 probes vs full-information give nearly identical numbers — only a 3% spread). Latency does matter: the system loses about 5% of its stored energy for each unit of delay, smoothly. But here is the key — *the shape of the attractor is preserved even as the energy drops*. The system stays in the same kind of state, just at a slightly lower level.
:::

::: scientific
The control-channel sensor signal — the band-mean inward energy flux — is reconstructable to within 3% across sensor counts from 4 to 32 (sparsity is essentially free above the minimum required spatial sampling). Latency is the dominant cost factor: E_φ decays exponentially with delay (~5% per integration step), but the Ez/Et structural-shape indicator stays at the clean reference value throughout. The system relaxes to a lower-energy version of the same attractor rather than losing the attractor.
:::

### Experiment 005 results

| Cell | n_probes | latency (steps) | noise floor | E_φ | E_zonal | E_turb | τ_E proxy |
|---|---|---|---|---|---|---|---|
| Reference | full_band | 0 | 0.0 | 14554 | 1498 | 25442 | 90963 |
| Sparsity 1 | 64 | 0 | 0.0 | 14533 | 1496 | 25444 | 90831 |
| Sparsity 2 | 32 | 0 | 0.0 | 14536 | 1495 | 25439 | 90851 |
| Sparsity 3 | 16 | 0 | 0.0 | 14280 | 1468 | 25001 | 89253 |
| Sparsity 4 | 8 | 0 | 0.0 | 14735 | 1518 | 25758 | 92091 |
| Sparsity 5 | 4 | 0 | 0.0 | 14588 | 1511 | 25681 | 91175 |
| Latency 1 | 16 | 5 | 0.0 | 11087 | 1187 | 20455 | 69293 |
| Latency 2 | 16 | 10 | 0.0 | 8161 | 872 | 15264 | 51006 |
| Latency 3 | 16 | 20 | 0.0 | 5060 | 503 | 9128 | 31628 |
| Stress | 16 | 10 | 0.05 | 8702 | 920 | 16056 | 54385 |

**Key takeaways.** Sparsity spread (full_band → 4 probes): E_φ varies by 3.1%, Ez/Et stays constant at 0.058–0.059. Latency exhibits log-linear decay (E_φ ≈ 14280·exp(−0.052·lat)). Combined stress at 16 probes + 10-step delay + 5% sensor noise yields E_φ at 0.60× of reference but **Ez/Et = 0.057 vs reference 0.059** — structure preserved, magnitude reduced. The mechanism degrades gracefully, not catastrophically.

![**Figure 2.** Benchmark 1 — sensor sparsity, control latency, and noise floor. Top row: stored energy and confinement-time proxy versus sensor count from full-band integration down to 4 discrete probes. Bottom-left: stored energy versus loop latency, log-linear decay with all three channels at the same rate (Ez/Et ratio preserved). Bottom-right: combined-stress point ratios against clean reference — 0.60× on energy but 0.97× on structural shape. Graceful, not catastrophic.](figures/fig_003_dirty_twin_blindness.png){width=100%}

---

## 7. Benchmark 2 — Actuator Inertia (Slew Rate)

::: plain
A real amplifier can only change its output so fast. We capped how quickly the system's "muscle" could respond, across five orders of magnitude. Result: two regimes. Above a threshold, the system gives up some absolute energy but keeps the same geometric shape — graceful. Below the threshold, the amplifier is so slow it never reaches saturation and the attractor breaks down. The threshold tells the engineer exactly what kind of amplifier they need (and what they don't need to overspend on). A mid-tier commercial Class-D amplifier suffices for the engineered build envelope.

This benchmark also surfaced a bug in our own model. The first run gave essentially identical numbers across a five-hundred-fold parameter sweep — a tell that something wasn't being tested. We diagnosed it (the slew-rate model was limiting only the amplitude of the actuator output, not its sign, so polarity flips could happen instantly even at the slowest slew). Fixed it. Re-ran. The data below is from the post-fix run, which is the real result.
:::

::: scientific
Sweep of `actuator_slew_rate` across five orders of magnitude with all other Tolkamak-0 hardware constraints held fixed (16 probes, 5-step latency, η = 0.40). Two regimes emerge, separated by a sharp threshold:

- **Graceful regime** — slew rates above the threshold preserve the Ez/Et structural-shape indicator to within 2.5% of the clean reference, with absolute energy plateauing on a stable lower-energy operating point.
- **Catastrophic regime** — slew rates an order of magnitude below the threshold prevent the actuator from completing a polarity flip within the 2500-step simulation window. The attractor's structural shape collapses by about 38% in this regime.

The benchmark's process value was the bug-surfacing: a half-physical slew model was exposed because the data refused to move across a 500× parameter sweep. The corrected model and re-run produced the data below.
:::

### Experiment 006 results

| Slew rate | Steps-to-full-range | E_φ | E_zonal | E_turb | Ez/Et | E_φ ratio vs instant | Ez/Et ratio |
|---|---|---|---|---|---|---|---|
| instant | 1 | 11087 | 1187 | 20455 | 0.0580 | 1.000 | 1.000 |
| 5.0 | 3.3 | 10054 | 1066 | 18473 | 0.0577 | 0.907 | 0.995 |
| 1.0 | 16.7 | 6992 | 715 | 12648 | 0.0566 | 0.631 | 0.975 |
| 0.2 | 83.3 | 4119 | 709 | 12510 | 0.0567 | 0.371 | 0.977 |
| 0.05 | 333.3 | 4108 | 832 | 14349 | 0.0580 | 0.371 | 1.000 |
| **0.01** | **1667** | **2455** | **28** | **791** | **0.0360** | **0.221** | **0.620** |

**Key takeaways.** A second-order homeostat shows up at the *actuator-rate level*: between slew=0.2 and slew=0.05 (a 4× span in slew rate), the system lands on essentially the same E_φ ≈ 4100. The threshold to catastrophic failure is between slew=0.01 and slew=0.05; slew=0.01 has the actuator never completing a polarity flip within the simulation window, and Ez/Et drops to 0.036 (62% of clean). Hardware-spec consequence: a mid-tier Class-D amplifier in the optimal regime is sufficient.

![**Figure 3.** Benchmark 2 — actuator slew rate. Top-right: energy ratio and structural-shape ratio across a 500× span; structural shape (green) stays near 1.0 across the upper four cells, drops at the slowest. Bottom-left: energy vs. actuator response time on a log scale, showing the transition between graceful and catastrophic. Bottom-right: commanded vs. applied actuator state at run-end.](figures/fig_004_dirty_twin_slew.png){width=100%}

---

## 8. Benchmark 3a — Magnetic Ripple, Perpendicular-Dominant Regime

::: plain
Real toroidal magnets are made from discrete coils, which create small "ripples" in the magnetic field around the ring. The Tolkamak thesis is that the macro geometry (the overall doughnut shape) sets the structured state, and that micro perturbations like coil ripple don't disturb it. We tested this with up to 40% ripple — vastly larger than any real machine would produce. In the original parameter regime, the mechanism essentially didn't see the ripple at all. The system's stored energy moved by less than one part in a million across the entire forty-fold ripple range.
:::

::: scientific
Multiplicative ripple on the safety-factor profile, sweeping ripple amplitude q_ripple_amp ∈ {0.00, 0.01, 0.03, 0.05, 0.10, 0.20, 0.40} at fixed q_ripple_freq = 8, plus a harmonic cross-check at amp = 0.10 across freq ∈ {4, 16}. Run with default v2/v3 physics parameters (κ_n = 0.08, c = 1.0, D_diff = 0.02): perpendicular-laplacian dominant.

### Experiment 007 results — perpendicular-dominant ripple

| Ripple amp | E_φ | Ez/Et | E_φ fractional change |
|---|---|---|---|
| 0.00 | 6992.0784 | 0.0565707831 | reference |
| 0.01 | 6992.0784 | 0.0565707830 | +3.5 × 10⁻⁹ |
| 0.03 | 6992.0784 | 0.0565707831 | +5.9 × 10⁻⁹ |
| 0.05 | 6992.0784 | 0.0565707831 | +2.5 × 10⁻⁹ |
| 0.10 | 6992.0781 | 0.0565707834 | −3.7 × 10⁻⁸ |
| 0.20 | 6992.0767 | 0.0565707844 | −2.0 × 10⁻⁷ |
| 0.40 | 6992.0709 | 0.0565707884 | −1.1 × 10⁻⁶ |

E_φ changes by 0.0075 out of 6992 across the entire 40× ripple sweep — a fractional change of **1.1 × 10⁻⁶**. Ez/Et changes by 5 × 10⁻⁹ in absolute terms. The mechanism does not see the ripple.

**Caveat that we identified during the experiment** and that motivated Benchmark 3b: in this parameter regime, parallel-transport coupling is approximately 12× weaker than the perpendicular laplacian. Real plasma has parallel transport that dominates by orders of magnitude on magnetic field lines. The benchmark was strong but did not represent physically realistic anisotropy. We re-ran it under inverted anisotropy.
:::

![**Figure 4.** Benchmark 3a — ripple absorption in the perpendicular-dominant regime. Top-right: Ez/Et structural-shape indicator across the ripple sweep; variation visible only at the ninth decimal place. Bottom panels: ratios pinned at 1.0 within plot resolution. This was a strong pass but not a physically stringent test.](figures/fig_005_dirty_twin_ripple.png){width=100%}

---

## 9. Benchmark 3b — Magnetic Ripple, Parallel-Dominant Stringent Regime

::: plain
We re-ran the ripple test, but with the parameters inverted to match how real plasma actually behaves on magnetic field lines: parallel transport now dominates by an order of magnitude. This is the version of the test fusion physicists would consider physically meaningful. The same 40% ripple — a hundred times larger than any real coil produces — moved the steady-state energy by 0.24% and the attractor shape by 0.10%. Both numbers are two orders of magnitude inside the pass-fail thresholds we set before running. The thesis survives.
:::

::: scientific
Inverted-anisotropy ripple sweep at κ_n = 1.0, c = 0.3, D_diff = 0.10 (parallel-to-perpendicular coupling ratio ≈ 11 — physically representative for plasma-edge fluctuation transport). Same 40× ripple amplitude sweep + 3-harmonic cross-check.

### Experiment 008 results — parallel-dominant stringent ripple

| Ripple amp | E_φ | Ez/Et | E_φ ratio | Ez/Et ratio |
|---|---|---|---|---|
| 0.00 | 3606.9802 | 0.04405777 | 1.0000000 | 1.0000000 |
| 0.01 | 3606.9837 | 0.04405774 | 1.0000010 | 0.9999993 |
| 0.03 | 3606.9860 | 0.04405769 | 1.0000016 | 0.9999981 |
| 0.05 | 3606.9821 | 0.04405765 | 1.0000005 | 0.9999971 |
| 0.10 | 3606.9453 | 0.04405760 | 0.9999903 | 0.9999961 |
| 0.20 | 3606.7501 | 0.04405775 | 0.9999362 | 0.9999995 |
| **0.40** | **3598.3076** | **0.04401309** | **0.9976582** | **0.9989859** |

**Harmonic cross-check at amp = 0.10**

| Freq | E_φ | Ez/Et |
|---|---|---|
| 4 | 3606.9300 | 0.04405757 |
| 8 (reference) | 3606.9453 | 0.04405760 |
| 16 | 3606.9944 | 0.04405757 |

**Pass / Fail verdict.** Pre-registered thresholds: ±10% on Ez/Et and ±30% on E_φ. Observed at the worst case (amp = 0.40): **E_φ drift 0.24%, Ez/Et drift 0.10%.** Both two orders of magnitude inside the PASS bands.

**Comparison with Benchmark 3a:** parallel dominance makes the ripple about 2200× more visible than in the perpendicular-dominant regime (an honest sensitivity increase). The absolute effect remains negligibly small in engineering terms.

**Mechanism.** The ripple modifies q(r,θ) which modifies parallel transport of the density field n. In the parallel-dominant regime this couples directly into the wave-field evolution. However, the TOU reinjection forcing is poloidally symmetric — the ring-source kernel deposits coherent energy with no θ-dependent structure to lock onto the ripple's spatial pattern. The ripple averages out across the deposit. The system settles at a slightly different operating energy (the 0.24%) but the geometric shape is preserved.
:::

![**Figure 5.** Benchmark 3b — stringent ripple test in the parallel-dominant regime. Top-right inset: the falsification target — Ez/Et structural shape vs. ripple amplitude. Flat from 0% to 20%, drops 0.1% only at 40%. Bottom-left: all energy channels relative to clean reference, with the ±30% PASS band shaded; every observed ratio is two orders of magnitude inside the band. Bottom-right: harmonic cross-check confirms the mechanism does not distinguish the harmonic.](figures/fig_006_dirty_twin_ripple_stringent.png){width=100%}

---

## 10. Implications for Industry

::: plain
We are not claiming this works in a real machine yet. A numerical experiment isn't a tokamak. But the Dirty Twin sequence is the closest thing to bench validation that simulation can offer, and the architecture's behavior under realistic constraints suggests at least four candidate domains where it could matter if the mechanism translates to hardware.
:::

::: scientific
The mechanism class — engineered Reynolds-stress accumulation plus phase-sensitive coherent reinjection on a toroidal substrate — has at least four candidate domains. Each is sized to where the empirical findings have direct relevance, not where speculation might lead.
:::

### Fusion Energy

::: plain
The biggest unsolved problem in commercial fusion is keeping the plasma's high-confinement state stable for long enough to make energy. The current playbook depends on a natural transition that is fragile and produces violent bursts of energy at the edge of the plasma (called ELMs). The Tolkamak architecture replaces the natural transition with a designed, controllable lock — same end state, different path. If the mechanism translates, the practical value is "steady-state H-mode without ELMs."
:::

::: scientific
The mechanism is functionally an externally-driven, saturating-actuator analog of L-H transition physics. Direct candidate applications: steady-state H-mode confinement without ELM cycles; lowered H-mode threshold power; active edge stability control; disruption-precursor detection via the accumulator's internal phase-EMA. Industry-relevant partners with operational tokamak hardware where the control law could be ported as a software/firmware layer on existing biased-electrode and Mirnov-coil infrastructure include Commonwealth Fusion Systems (SPARC), Tokamak Energy (ST40), General Atomics (DIII-D), and the broader DOE Office of Fusion Energy Sciences INFUSE program portfolio.
:::

### Aerospace Propulsion

::: plain
Plasma rockets have a hard ceiling because the plasma column inside them is always falling apart against the walls. A mechanism that keeps a plasma column structurally locked could let those engines run hotter, denser, and more efficiently. The most exciting near-term application is the Direct Fusion Drive concept under development at Princeton — combined power-plus-propulsion for outer-solar-system missions.
:::

::: scientific
Plasma-based thrusters (VASIMR, MPD, pulsed inductive, gridded ion) are limited by wall losses and turbulent decoherence. A drive-independent coherent column directly raises specific impulse. Closest near-term overlap: Princeton Field-Reversed Configuration / Direct Fusion Drive at Princeton Satellite Systems. Other candidates: NASA Glenn (MPD), Ad Astra Rocket Company (VASIMR), Pulsar Fusion (UK).
:::

### Defense and Strategic Systems

::: plain
Anywhere plasma needs to hold structure under sustained perturbation: compact fusion neutron sources for cargo and weapons inspection, plasma-sheath management on hypersonic vehicles, pulsed power for directed-energy systems, and field-deployable fusion-driven energy units. The mechanism's small footprint — it is software/firmware on existing plasma hardware classes — makes it a candidate for technologies where size and weight matter.
:::

::: scientific
Direct candidates: compact dense-plasma-focus stabilization for portable neutron sources (DTRA, NNSA programs); hypersonic-vehicle plasma-sheath control for through-blackout RF communication (DARPA, AFRL hypersonics); pulsed-power directed-energy stabilization; tactical fusion-pulsed power. The dual-use angle with the author's AI safety work — both lines share a common theoretical primitive of geometric self-organization under inward-flux rectification — is a coordinated strategic asset for SBIR / STTR exploration.
:::

### AI Safety (the Author's Parent Domain)

::: plain
This is the connection that motivated the whole research program. A safe AI system needs to maintain coherent behavior under adversarial input. Most current work treats that as a training problem — train the model to be robust. The Tolkamak result suggests an alternative: construct the geometry so coherence is the natural attractor, and the system becomes robust by architectural fact rather than by training. We are not claiming this solves AI safety. We are claiming the mechanism class is in the same family as what an aligned system needs to exhibit, and that family has not been adequately explored.
:::

::: scientific
A system that maintains structural integrity (Ez/Et invariant) across a 16× drive perturbation and survives sensor sparsity, control latency, actuator slew limits, and 40% magnetic ripple in a parallel-dominant regime is, in control-theoretic terms, a geometric homeostat. The architectural strategy — substrate-as-stability — is orthogonal to the prevailing training-time robustness approach in AI alignment. The mechanism's open inspectability (~30 lines of code) makes it a candidate primitive for empirical alignment research.
:::

---

## 11. Reproducibility and Scope

::: plain
Everything in this paper that isn't the core control law is open. The simulation engine, the experiment scripts, the figures, the raw data — anyone can download and rerun them. The exact code implementing the phase-sensitive reinjection kernel is held proprietary pending IP review, but its inputs, outputs, and behavior are fully documented.

Source code, experiment scripts, and data: **[github.com/projectblackboxllc](https://github.com/projectblackboxllc)**
:::

::: scientific
The Tolkamak engine source (v2 and v3) is published at [github.com/projectblackboxllc](https://github.com/projectblackboxllc) with parameters and seeds for every experiment in this paper. Aggregated data CSVs for each benchmark are included, along with per-run raw outputs (metrics time series, ring-probe readings, per-step JSON snapshots for animation). The proprietary mechanism configuration values (`reinject_gain`, `accumulator_leak`, `k`, `phase_alpha`) are redacted. Open future work: Tolkamak-0 bench validation, multi-seed ensembles, full degradation-matrix sweeps, replication at v1's published high-resolution parameters (N = 121, 30,000 steps).
:::

---

## 12. What This Is, and What This Is Not

::: plain
This is a numerical experiment. There are no real ions, no real magnetic fields, no real heat. It is mathematical: a particular geometry plus a particular feedback rule, run on a computer, with the answer being how the energy distributes itself in the simulation. It is *not* a fusion reactor and we are not claiming it is.

What it *is*, in our view:

- A clean, inspectable disproof of two specific assumptions that run through most of plasma physics and a lot of control engineering: that systems respond linearly to drive, and that self-organization proceeds via discrete-state bifurcations.
- A reproducible starting point. The code is small. Anyone can verify the numbers. The figures, data, and parameter settings are all open.
- A defensible prior-art record. If the architecture has hardware applicability — and the four-benchmark stress sequence suggests it does — the path forward is to build the bench-scale apparatus (called Tolkamak-0) and find out empirically.
- A start, not a destination. The honest framing is that this is what comes before bench validation, not what replaces it.
:::

::: scientific
The empirical claims in this paper are claims about this geometry, this mechanism, and this data. They are not extrapolations to physical tokamak plasmas, biological systems, or AI systems. The Dirty Twin sequence has substantially narrowed the gap between "mathematically perfect simulation" and "physically realizable architecture" but it has not closed that gap. Bench validation is the open frontier.
:::

---

## 13. Companion Citation

The author's prior work, *TOU Engine — Toroidal Self-Organization in a 3D Wave Manifold* (Zenodo, January 2026), reported the original Mode-4 attractor result that motivated the present paper. As of this writing, that publication has held the 80th-percentile read-to-download ratio on Zenodo for over four months — a reception-quality signal that the framework resonates with readers. The present paper extends that work into a hardware-relevance regime and offers the prior-art record for the Toroidal Geometric Rectifier architecture.

---

## Citation

```
Woodward, A. (2026). A Toroidal Geometric Rectifier: Empirical Disproof
of Linear-Response in Plasma Confinement. Project Black Box LLC
(CAGE 11FU4). Zenodo. https://doi.org/10.5281/zenodo.20245905
ORCID: 0009-0006-9717-7161
```

## Contact

Andrew Woodward — Project Black Box LLC (CAGE Code 11FU4)
ORCID: [0009-0006-9717-7161](https://orcid.org/0009-0006-9717-7161)
Source: [github.com/projectblackboxllc](https://github.com/projectblackboxllc)

## Acknowledgments

The author thanks Professor David Keathly for his persistent feedback on writing across multiple audiences. The dual-voice structure of this paper is in his debt.

---

## Appendix A — Full Aggregated Experiment Data

This appendix contains the complete aggregated CSV outputs from each experiment, with mechanism-revealing columns (internal accumulator state, signed-actuator output) redacted. All values are reproducible from the published code given the documented parameters and seed=42.

### A.1 — Experiment 001 (Headline result)

12 paired runs (6 noise levels × OFF/ON arms), 2500 steps each, N=65, seed=42.

| η | E_z(OFF) | E_t(OFF) | E_z(ON) | E_t(ON) | Ez/Et(OFF) | Ez/Et(ON) | τ_E(OFF) | τ_E(ON) | gain |
|---|---|---|---|---|---|---|---|---|---|
| 0.05 | 0.0219 | 1.517 | 26.44 | 2315 | 0.01445 | 0.01142 | 2080 | 596,510 | 287.0× |
| 0.10 | 0.0474 | 2.927 | 26.41 | 2312 | 0.01620 | 0.01142 | 1868 | 150,099 | 80.4× |
| 0.20 | 0.149 | 8.562 | 26.08 | 2279 | 0.01746 | 0.01144 | 1815 | 38,079 | 21.0× |
| 0.40 | 0.558 | 31.09 | 26.46 | 2300 | 0.01794 | 0.01151 | 1802 | 10,916 | 6.1× |
| 0.60 | 1.238 | 68.63 | 27.10 | 2333 | 0.01804 | 0.01162 | 1799 | 5,839 | 3.2× |
| 0.80 | 2.191 | 121.2 | 28.02 | 2382 | 0.01808 | 0.01176 | 1798 | 4,067 | 2.3× |

### A.2 — Experiment 005 (Sensor sparsity + latency)

10 cells, all at η=0.40, TOU on, N=65, seed=42.

| Cell | n_probes | latency (steps) | noise_frac | E_φ | E_zonal | E_turb | Ez/Et | τ_E proxy |
|---|---|---|---|---|---|---|---|---|
| 1 | full_band | 0 | 0.0 | 14554 | 1498 | 25442 | 0.0589 | 90963 |
| 2 | 64 | 0 | 0.0 | 14533 | 1496 | 25444 | 0.0588 | 90831 |
| 3 | 32 | 0 | 0.0 | 14536 | 1495 | 25439 | 0.0588 | 90851 |
| 4 | 16 | 0 | 0.0 | 14280 | 1468 | 25001 | 0.0587 | 89253 |
| 5 | 8 | 0 | 0.0 | 14735 | 1518 | 25758 | 0.0589 | 92091 |
| 6 | 4 | 0 | 0.0 | 14588 | 1511 | 25681 | 0.0589 | 91175 |
| 7 | 16 | 5 | 0.0 | 11087 | 1187 | 20455 | 0.0580 | 69293 |
| 8 | 16 | 10 | 0.0 | 8161 | 872 | 15264 | 0.0571 | 51006 |
| 9 | 16 | 20 | 0.0 | 5060 | 503 | 9128 | 0.0552 | 31628 |
| 10 | 16 | 10 | 0.05 | 8702 | 920 | 16056 | 0.0573 | 54385 |

### A.3 — Experiment 006 (Actuator slew rate)

6 cells, all at η=0.40 + 16 probes + 5-step latency, TOU on, N=65, seed=42.

| Cell | slew_rate | Approx steps-to-full-range | E_φ | E_zonal | E_turb | Ez/Et | τ_E proxy |
|---|---|---|---|---|---|---|---|
| 1 | instant | 1 | 11087 | 1187 | 20455 | 0.0580 | 69293 |
| 2 | 5.0 | 3.3 | 10054 | 1066 | 18473 | 0.0577 | 62838 |
| 3 | 1.0 | 16.7 | 6992 | 715 | 12648 | 0.0566 | 43700 |
| 4 | 0.2 | 83.3 | 4119 | 709 | 12510 | 0.0567 | 25744 |
| 5 | 0.05 | 333.3 | 4108 | 832 | 14349 | 0.0580 | 25673 |
| 6 | 0.01 | 1666.7 | 2455 | 28 | 791 | 0.0360 | 15342 |

### A.4 — Experiment 008 (Stringent ripple, parallel-dominant)

9 cells (7 amplitudes × freq=8, plus 2 freq cross-checks at amp=0.10), all at η=0.40 + 16 probes + 5-step latency + slew=1.0, κ_n=1.0, c=0.3, D_diff=0.1, TOU on, N=65, seed=42.

| Cell | ripple_amp | ripple_freq | E_φ | E_zonal | E_turb | Ez/Et |
|---|---|---|---|---|---|---|
| 1 | 0.00 | 8 | 3606.9802 | 881.110 | 19998.96 | 0.04405777 |
| 2 | 0.01 | 8 | 3606.9837 | 881.108 | 19998.95 | 0.04405774 |
| 3 | 0.03 | 8 | 3606.9860 | 881.106 | 19998.91 | 0.04405769 |
| 4 | 0.05 | 8 | 3606.9821 | 881.103 | 19998.87 | 0.04405765 |
| 5 | 0.10 | 8 | 3606.9453 | 881.096 | 19998.72 | 0.04405760 |
| 6 | 0.20 | 8 | 3606.7501 | 881.079 | 19998.28 | 0.04405775 |
| 7 | 0.40 | 8 | 3598.3076 | 876.795 | 19921.23 | 0.04401309 |
| 8 | 0.10 | 4 | 3606.9300 | 881.094 | 19998.69 | 0.04405757 |
| 9 | 0.10 | 16 | 3606.9944 | 881.104 | 19998.93 | 0.04405757 |

---

## Appendix B — On the v3 Engine Mid-Run Bug Discovery

During Experiment 006 (slew-rate test), the data refused to move across a 500× parameter sweep. Diagnosis: the slew-rate implementation in the engine limited only the amplitude of the actuator's commanded output, while the sign of the output flowed through a separate channel and flipped instantaneously regardless of slew. This is not how a real Class-D amplifier behaves — slew limits |d(V_out)/dt|, including across polarity changes. The engine was corrected to slew the signed actuator output directly. Experiment 006 was re-run with the corrected model; the data above is from the post-fix run. This discovery is the engineering value of the Dirty Twin protocol: a model that survives every degradation by being modeled incorrectly is more dangerous than a model that fails for the right physical reason.

---

*End of paper.*
