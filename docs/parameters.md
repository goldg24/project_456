# Parameter provenance — unresolved values are explicit

All current numerical values are **illustrative engineering assumptions**, not extracted Iso E Super process data. They demonstrate a reproducible dynamic model while source validation remains pending.

| Parameter | Value | Units | Present basis / required route |
|---|---:|---|---|
| V | 100 | L | Representative project-scale working volume; justify from chosen vessel dimensions. |
| q | 100/30 | L/min | Selected with V for a 30 min residence time; obtain operating data or justify scale. |
| CA_feed | 1 | mol/L | Assumed feed dilution; establish precursor/catalyst/solvent composition. |
| CP_feed | 0 | mol/L | Assumed product-free feed. |
| T_feed | 320 | K | Assumed feed condition; verify chemistry compatibility. |
| rho | 0.85 | kg/L | Placeholder liquid-mixture density; use actual mixture data. |
| cp | 2 | kJ/(kg K) | Placeholder liquid-mixture heat capacity; use mixture data. |
| UA | 1.5 | kJ/(min K) | Assumed effective conductance, equivalent to 25 W/K; source U and estimate area A separately from dimensions/correlations. |
| delta_H | −20 | kJ/mol precursor | Assumed exothermic reaction; both sign and magnitude require thermochemical evidence. |
| k_ref | 0.05 | 1/min | Illustrative pseudo-first-order kinetics at fixed catalyst activity; requires measured/fitted data for the selected precursor and acid. |
| T_ref | 330 | K | Reference temperature for illustrative k. |
| Ea | 60 | kJ/mol | Illustrative activation energy; not a patent-derived value. |
| R | 0.008314462618 | kJ/(mol K) | Universal gas constant expressed in these units. |
| Tj | 330; steps 340/320 | K | Assumed utility conditions, to be checked against reaction and utility constraints. |

## Inspected sources and exactly what they support

1. Original Stage0_Conversation.pdf, pages 4–7: project scope, student choices, storage quantities, estimated minute-to-hour time scale, and conversion/purity distinction. It supplies no numerical parameters.
2. Supplied CHE 456 Topic 03 Dynamic Modeling lecture: component and energy accumulation structure and ideal mixing assumptions. It does not supply this project's kinetics or heat-transfer parameters.
3. US6160182A, *Process for obtaining mixtures of isomeric acyloctahydronaphthalenes*: https://patents.google.com/patent/US6160182A/en . Its abstract describes acid-catalyzed cyclization of myrcene Diels–Alder adducts and mixtures of perfumery-relevant isomers. It supports the chemistry direction, not the numerical k_ref, Ea, delta_H, or CSTR operating values used here. Detailed example extraction and kinetic fitting have not been completed.
4. US11807664, *Method for producing cyclic organic compound*: https://patents.justia.com/patent/11807664 . Screened and rejected as an Iso E Super parameter source: its scope is pharmaceutical macrocyclic/peptide chemistry. Search results mentioning CSTR and Arrhenius kinetics do not justify transferring its values to this project.

## Next parameter work

Select a specific precursor, acid, catalyst loading, solvent and temperature interval. Seek conversion-versus-time data at multiple temperatures for that exact chemistry. A single end-point yield is insufficient to establish both reaction order and activation energy. If usable kinetics are unavailable, document the assumed law, ranges, sensitivity, and instructor acceptance rather than claiming literature validation. Derive q and V from scale/time goals, and UA from a documented vessel area and a suitable heat-transfer correlation. Use the actual mixture for density and heat capacity. A product SDS alone cannot provide precursor kinetics or reaction enthalpy.
