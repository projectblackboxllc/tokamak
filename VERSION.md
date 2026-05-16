# VERSION.md — Append-Only Release Log

## v1.0 — 2026-05-06
- `tou_tokamak.py` (v1 engine)
- Original Zenodo result: 80% noise, q₀=1.05, q₁=3.0, 30,000 steps
- Mode 4 rank 1 (non-DC), signal 261,794
- Mode-4/DC ratio = 0.026 (geometric invariant)

## v2.0-dev — 2026-05-16 (in progress)
- `tou_tokamak_v2.py` adds adiabaticity α, curvature drive κ_B, zonal-flow diagnostics, τ_E estimator, JSON frame export
- Scientific folder hierarchy introduced (figures/, reports/, data/, papers/, videos/, analysis/, experiments/)
- Experiment 001 (L-H transition) building

## v2.0 — 2026-05-16 (Experiment 001 first pass)
- Engine `tou_tokamak_v2.py` validated end-to-end.
- Analysis modules added: `analysis/{ring_modes,zonal_flow,confinement_time,disruption_precursor}.py`.
- Experiment 001 orchestrator + post-processor + 12-run sweep (N=65, 2500 steps, six noise levels, paired TOU on/off).
- **Result (revised from L-H hypothesis):** TOU mechanism is a saturating homeostat. Drive-induced variation reduced by ~44× to ~77× depending on metric. τ_E gain 287× at low drive, 2.3× at high drive.
- Artifacts produced: data/exp_001_lh_transition.csv (aggregate, 6 rows), figures/fig_001_lh_phase_diagram.png, figures/fig_002_homeostat_attractor.png, reports/report_001_lh_phase_diagram.md (rewritten), reports/report_002_homeostat_attractor.md, papers/plain_language/v1.0/tolkamak_plain_v1.0.md, papers/technical/v1.0/tolkamak_technical_v1.0.md, papers/plain_language/v1.0/linkedin_post_draft.md, CITATION.cff, videos/frame_data/exp_001_frames.json, videos/render_frames.py.
- README appended with v2 section (original v1 README preserved).
- Experiments 002/003/004 left as stubs.
