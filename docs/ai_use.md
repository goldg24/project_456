# Evidence-based AI-use record

## Session: October 1, 2026 (America/Indianapolis)

**Tool:** ChatGPT Work coding assistant. This work ran in the assistant's execution workspace, not a GitHub Codespace. No claim of a Codespace agent session is made.

**User goal and supplied evidence:** User requested a personal public course repository and continuation of the accepted Iso E Super CSTR proposal. They provided the Stage 1 announcement and instructor Stage 0 feedback; the detailed statement and course template were unavailable. User created goldg24/project_456 manually.

**AI actions:** Read the full original Stage 0 transcript; inspected accumulation and energy-balance material in supplied lectures; checked GitHub ownership and access; screened patent sources; derived and implemented a three-state lumped CSTR; ran startup and warming/cooling steps; recorded CSV trajectories and checks. The full transcript and course PDFs are not republished here.

**AI decisions requiring student review:** Treat catalyst activity as fixed; use pseudo-first-order one-to-one irreversible cyclization; lump all products; omit jacket inventory; choose effective jacket temperature as the physical input; choose all numerical parameters provisionally, including assumed exothermic heat release.

**Corrections and rejected suggestions:** Preserved states as in-vessel storage rather than feed/outlet conditions. Rejected an unrelated pharmaceutical cyclization patent as a numerical source. Avoided equating conversion with purity. Noted that steady inputs alone do not establish stability and that the product balance is dependent under the fixed-total special case.

**Evidence:** `results/checks.json` and CSV files contain the numerical results. The simulation asserts physical states, conservation against the exact total-inventory solution, small equilibrium residuals, negative real parts of local Jacobian eigenvalues, and agreement under tighter solver tolerances. These checks verify implementation under the assumptions, not experimental fidelity.

**Student review status:** Pending. The student has accepted the Stage 0 topic and simplified conversion output, but has not yet reviewed or approved this session's equations, estimates, predictions, or output.

**Remaining record:** Add actual Codespace URL/name, coding-agent prompts and responses, commands and execution outputs, commit identifiers, accepted/rejected suggestions, and student reasoning after performing the required Codespace work. Do not backdate this workspace run as Codespace activity. This summary is not a verbatim transcript; retain/export the full interaction if the final rubric requires one.

**Tokens and cost:** Exact token counts and billed cost are not exposed for this session. No numerical estimate is claimed. If required, follow the course estimation method and cite the provider pricing page and separate input/output/cached rates actually used.

## Visual dashboard extension — October 1, 2026

User requested a complete visual screen for inputs and outputs over time. AI added a local Streamlit/Plotly dashboard with an inspection slider, reactor schematic, scheduled jacket step, chart playback, parameter controls and CSV/JSON export. Dashboard trajectories use the existing model rather than a separate visual approximation. Chart animation and the inspection snapshot operate independently and are labeled accordingly.

Verification performed in the assistant workspace: fixed-input baseline reproduces prior endpoint; warming and cooling change conversion in the predicted directions; step-state continuity and exact step timing pass; inventory conservation passes; invalid step timing is rejected. Streamlit AppTest rendered the dashboard without exceptions and applied a changed form setting without exceptions. Browser playback and the Windows launch script have not been exercised on the student's computer. No Codespace run or student review is claimed.

Framework API references inspected: https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart and https://docs.streamlit.io/develop/api-reference/execution-flow/st.form . These support UI implementation only, not physical model validation.
