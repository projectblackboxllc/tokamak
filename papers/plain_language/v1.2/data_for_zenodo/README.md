# Zenodo data bundle — Tolkamak v1.2

Companion data files for the Zenodo deposit *A Toroidal Geometric Rectifier: Empirical Disproof of Linear-Response in Plasma Confinement* (Tolkamak Whitepaper v1.2).

## Contents

| File | Experiment | Description |
|---|---|---|
| `exp_001_lh_transition.csv` | Experiment 001 | Headline drive sweep. 6 noise levels × OFF/ON paired runs. Steady-state E_zonal, E_turb, Ez/Et ratio, τ_E proxy, dominant ring mode for each cell. |
| `exp_005_dirty_twin_blindness.csv` | Experiment 005 | Sensor sparsity + control-loop latency benchmark. 10 cells: 6-point sparsity sweep + 3-point latency sweep at 16 probes + 1 combined stress cell. |
| `exp_006_dirty_twin_slew.csv` | Experiment 006 | Actuator slew-rate benchmark. 6 cells across a 500× span of slew rate, post-bugfix (signed-output slew model). |
| `exp_007_dirty_twin_ripple.csv` | Experiment 007 | Magnetic ripple benchmark, perpendicular-dominant regime. 7-amplitude sweep + 2 freq cross-checks at amp=0.10. |
| `exp_008_dirty_twin_ripple_stringent.csv` | Experiment 008 | Magnetic ripple benchmark, parallel-dominant regime (parallel/perpendicular coupling ratio ≈ 11). Same 9-cell layout as exp_007. |

Each row in each CSV is one simulation run. Columns are the parameter settings for that run (noise amplitude, sparsity setting, slew rate, ripple amplitude, etc.) and the measured steady-state energy quantities (E_φ, E_zonal, E_turb, Ez/Et, τ_E proxy, dominant ring mode).

## Reproducibility

All cells were run with seed = 42, N = 65, 2500 integration steps, dt = 0.12. Full parameter documentation is in §2 ("Methodology and Parameters") of the whitepaper. The simulation engine that generated these CSVs is in development at github.com/projectblackboxllc.

## Redactions (what's NOT here)

The original aggregated CSVs in the source repo include a small number of additional columns that expose internal mechanism state (the accumulator's integrated flux value at run-end and the actuator's settled command/signed-output values). Those columns are stripped from the files in this folder before publication.

The redaction policy:

| Column type | In source `data/` | In this folder | Reason |
|---|---|---|---|
| Parameter settings | ✓ | ✓ | open |
| Measured energies (E_φ, E_zonal, E_turb) | ✓ | ✓ | open |
| Derived metrics (Ez/Et, τ_E, gain ratios) | ✓ | ✓ | open |
| Dominant ring mode info | ✓ | ✓ | open |
| `final_inj_cmd` | ✓ | — | mechanism state (saturating-actuator command) |
| `final_inj_applied` | ✓ | — | mechanism state (settled actuator output, v3 pre-bugfix model) |
| `final_signed_output` | ✓ | — | mechanism state (settled actuator output, v3 corrected model) |
| `final_acc` | ✓ | — | mechanism state (accumulator integral at run-end) |
| `run_dir`, `off_run_dir`, `on_run_dir` | ✓ | — | local filesystem paths, not useful externally |

Per-run output directories (full time-series of mechanism state, ring-probe time series, frame snapshots, per-run metadata, per-run diagnostic figures) are NOT released — they would enable reverse-engineering of the proprietary accumulator+reinjector control law.

The `_redact.py` script in this folder is the exact filter that produced these CSVs from the source. It is included so the redaction is auditable.

## Citation

Woodward, A. (2026). *A Toroidal Geometric Rectifier: Empirical Disproof of Linear-Response in Plasma Confinement.* Project Black Box LLC (CAGE 11FU4). Zenodo. https://doi.org/10.5281/zenodo.20245905 · ORCID: 0009-0006-9717-7161.
