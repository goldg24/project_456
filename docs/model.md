# Model scope and derivation

## Recovered Stage 0 choices

The original Stage0_Conversation.pdf, pages 4–7, selects one jacketed continuous stirred reactor for acid-catalyzed cyclization of a myrcene-derived precursor. The student chose jacket heating/cooling, then simplified the output from desired-isomer fraction to precursor conversion. No numerical kinetic, reactor, or thermal parameters were chosen in that conversation.

## Boundary, states, and assumptions

The boundary contains the well-mixed reactor liquid. The jacket is an imposed thermal boundary; its inventory is not inside the model. Constant density, heat capacity, liquid volume, equal inlet/outlet volumetric flow, fixed catalyst activity, and negligible shaft work and ambient heat loss are assumed. This is a conceptual CSTR adaptation, not a claim that the referenced patent uses this reactor configuration.

| State | Stored quantity and accumulation |
|---|---|
| CA, mol/L | Precursor inventory nA = V CA; feed adds it, outflow removes it, and cyclization consumes it. |
| CP, mol/L | Lumped cyclization-product inventory nP = V CP; reaction generates it and outflow removes it. |
| T, K | Sensible thermal energy relative to a reference, rho cp V (T − Tdatum); feed enthalpy, reaction heat, and jacket heat transfer change it. |

For a one-to-one lumped reaction A → P, CA + CP follows its own transport balance. At a constant total-feed concentration and matching initial total, CP is algebraically recoverable from CA. Thus three physical inventories are tracked, but this special case has only two independent degrees of freedom. The assignment permits two to six states; check whether its full statement requires an explicitly minimal state vector.

## Inputs, disturbances, and measurements

- Physical manipulated input: effective jacket utility temperature Tj (K), assumed directly imposed by a fast utility loop. Utility valve dynamics and jacket thermal storage are omitted.
- Fixed feed conditions / potential disturbances: q, CA_feed, CP_feed, and T_feed. These are boundary inputs, not vessel states.
- Output: X_app = 1 − CA / CA_feed, inferred from an assumed calibrated online NIR/IR concentration measurement. No chemistry-specific sensor calibration has been established. Perfect mixing makes outlet and reactor concentrations equal.
- During startup X_app is a concentration-based indicator and can include inventory effects. It is interpreted as feed-to-outlet conversion at steady state with the fixed feed and volume assumptions.

## Equations

Conservation structure follows the supplied Topic 03 Dynamic Modeling lecture: accumulation = inlet − outlet + generation, with energy accounted for separately.

With D = q/V and fixed catalyst activity absorbed into k:

```
k(T) = k_ref exp[−Ea/R (1/T − 1/T_ref)]
r = k(T) CA

dCA/dt = D (CA_feed − CA) − r
dCP/dt = D (CP_feed − CP) + r
dT/dt  = D (T_feed − T) − delta_H r/(rho cp)
         + UA (Tj − T)/(rho cp V)
```

Arrhenius temperature dependence makes this nonlinear. Pseudo-first-order irreversible kinetics and the exothermic sign are modeling assumptions, not established properties of the specific chemistry. A negative delta_H makes the reaction contribution positive. Heat flows into the liquid when Tj > T. All terms in the concentration balances have mol/(L min); all terms in the temperature balance have K/min.

## Predictions and checks

Before the runs, the assumed positive activation energy suggests warming the jacket increases reactor temperature, rate, and steady conversion near the chosen baseline. Cooling should reverse these changes. The chosen modest reaction heat and thermal removal suggest settling, but a constant input does not by itself prove a nonlinear reactor stable.

Residence time V/q = 30 min. The nonreactive thermal time constant is 1/[q/V + UA/(rho cp V)] = 23.72 min; reaction coupling changes the actual modes. Simulation checks a 300 min horizon, root-based equilibrium, scaled endpoint residuals, physical states, inventory conservation, local Jacobian eigenvalues, and agreement at tighter numerical tolerances. Local stability is not a global uniqueness or runaway-safety proof.

This one-step model cannot distinguish desired isomers from byproducts. Its CP must not be labeled pure Iso E Super, and increased conversion is not evidence of increased purity. Adding a sourced competing reaction is a possible later extension.
