# CHE 456 — Iso E Super precursor cyclization

**Stage 1 working draft, not a submission-ready or experimentally validated process model.**

This project represents the accepted Stage 0 concept: a jacketed CSTR for acid-catalyzed precursor cyclization, with conversion inferred from a calibrated precursor-concentration analyzer. The current model uses three storage states and a lumped one-step reaction. It does not predict desired-isomer purity or degradation.

## Interactive visual dashboard

Launch from the project folder:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Use `python` instead of `py` in a Codespace or on Linux/macOS. On Windows, you can also double-click `run_visual.bat`; it installs the dependencies and launches the dashboard. Keep the terminal open while using it, and press Ctrl+C to stop it.

The dashboard opens at http://localhost:8501. If a browser tab does not open automatically, paste that address into your browser.

- Set startup or an initially settled reactor, jacket temperatures, a step time and simulation duration.
- Adjust feed flow, working volume, feed concentration/temperature and heat-transfer conductance.
- Press **Run simulation** to apply the input settings.
- Use the inspection-time slider to update the vessel schematic and readouts. Chart **Play** animates the plots separately; **Full result** restores the complete trajectories.
- Hover/zoom the input, reactor temperature, inventories and conversion plots. Download each experiment as CSV plus a JSON record of its assumptions and checks.

Changing settings in the form does not change the displayed experiment until Run simulation is pressed. Scheduled steps are integrated as separate intervals so the solver does not smear the discontinuity. The dashboard uses the same `src/model.py` balances as the headless simulation.

ZIP downloads are snapshots: if you downloaded the repository before the dashboard was added, download and extract the latest ZIP to get `app.py` and the updated requirements. ZIP folders are not Git clones and cannot be updated using `git pull`.

## Headless simulation

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
