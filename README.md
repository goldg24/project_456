# CHE 456 — Iso E Super precursor cyclization

**Stage 1 working draft, not a submission-ready or experimentally validated process model.**

This project represents the accepted Stage 0 concept: a jacketed CSTR for acid-catalyzed precursor cyclization, with conversion inferred from a calibrated precursor-concentration analyzer. The current model uses three storage states and a lumped one-step reaction. It does not predict desired-isomer purity or degradation.

## Run

```bash
python -m pip install -r requirements.txt
python src/simulate.py
```

Outputs are written to `results/`: trajectories, plots, and quantitative verification checks. Requires Python 3.11 or newer.

## Current evidence

| Run | Jacket K | Reactor steady K | Conversion | Settling min |
|---|---:|---:|---:|---:|
| Fixed-input startup | 330 | 327.259 | 0.55535 | 66.25 |
| Warming step from baseline | 340 | 329.727 | 0.59565 | 75.50 |
| Cooling step from baseline | 320 | 324.776 | 0.51343 | 77.25 |

Settling means all state errors remain within 0.01 mol/L for each concentration and 0.1 K for temperature. These absolute bands are 1% of declared scales (1 mol/L, 1 mol/L, 10 K), not 1% of each step amplitude. Each step is a separate run starting at the baseline equilibrium. No feedback controller is used.

## Before submission

- Obtain the official Stage 1 statement and course template; reconcile this draft with their required structure. This repository was initially created manually, and is not confirmed to have been created from the required template.
- Run the coding agent and simulation in a GitHub Codespace. A draft development-container configuration is included, but no Codespace run has been performed or verified.
- Replace or justify the illustrative parameters with source-specific estimates, especially kinetics and reaction enthalpy. Check acceptable operating temperatures and catalyst conditions for the selected chemistry.
- Review the model and its limitations yourself, and add your actual decisions and Codespace evidence to the AI-use record.

See [model derivation](docs/model.md), [parameter provenance](docs/parameters.md), and [AI-use record](docs/ai_use.md).
