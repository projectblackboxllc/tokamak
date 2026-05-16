#!/usr/bin/env python3
"""Experiment 003 — Disruption precursor detection (Tolkamak v2).

STATUS: STUB. Implementation deferred until Experiments 001, 002 land.

QUESTION
========
Can the TOU phase_ema or accumulator value serve as an early-warning
precursor for energy-collapse events analogous to tokamak disruptions?

DESIGN (planned)
================
- Trigger controlled kink-like perturbations at a known step
- Trigger sawtooth-like (radial energy redistribution) events
- Measure precursor lead time: step at which phase_ema z-score crosses
  threshold vs step of energy collapse
- Both TOU on (precursor available) and TOU off (control)
- Report ROC curve for binary classification

ARTIFACTS (planned)
===================
- data/exp_003_disruption.csv
- figures/fig_003_disruption_precursor.png
- reports/report_003_disruption_precursor.md
- videos/frame_data/exp_003_frames.json
"""
print("exp_003_disruption — STUB. See file docstring for design.")
