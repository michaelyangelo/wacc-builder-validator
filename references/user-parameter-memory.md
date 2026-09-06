# Same-User Parameter Memory

Use memory to preserve one user's preferred discount-rate review approach
across invocations, times, and projects. Do not use it to standardise different
users or to carry project data forward.

## Memory scope

Read available context in this order:

1. persistent memory explicitly associated with the same user and this Skill;
2. the current conversation and its review register;
3. an authorised user-provided or internal methodology profile;
4. the Skill defaults when no user preference exists.

Never read, infer, or reuse another user's profile.

## Reusable preferences

Remember compatible choices such as:

- preferred base-rate policy, including the German Bund anchor for every
  EU/EEA calculation and the U.S.-Treasury anchor for every calculation
  outside the EU/EEA;
- treatment of valuation currency and cash-flow basis through separate
  country, sovereign, currency/inflation/basis, and other justified
  adjustments rather than another national government rate;
- ERP provider, dataset definition, and regional convention;
- beta Path Q, P, or R; target benchmark and matched ERP; peer-selection,
  weighting, unlevering, cross-benchmark normalization, and relevering
  convention;
- preferred five-year monthly and two-year weekly regression settings,
  minimum observations, price type, currency, and data-quality thresholds;
- target capital-structure and debt/cash definitions;
- cost-of-debt evidence hierarchy;
- country, sovereign, currency, and double-counting treatment;
- DLOM and DLOC treatment;
- calculation precision and rounding convention;
- preferred bridge, source table, and reporting format;
- preferred project-versus-parent presentation and claim-by-claim/APV policy;
- preferred implied-rate timing and terminal-normalization convention;
- preferred before/after comparison format;
- preference for screenshots as supplementary evidence for load-bearing public
  sources when available.
- approved internal policies or user corrections.

Treat a one-off project override as project-specific unless the user explicitly
asks to make it their future preference.

## Never reuse as memory

Do not carry forward:

- old market observations or publication dates;
- company, transaction, asset, peer, or security data;
- workbook values, formulas, links, cells, or findings;
- calculated, selected, or applied rates;
- cash flows, valuation results, sensitivities, or scenarios;
- project-specific overrides;
- confidential evidence outside the context and permissions that make it
  available.

The remembered item is the source or method definition, not its old numerical
value.

## Invocation procedure

1. Check same-user Skill memory before selecting parameters.
2. Compare remembered preferences with the current purpose, valuation date,
   currency, jurisdiction, discounted object, cash-flow basis, and evidence.
3. Apply compatible preferences without asking the user to repeat them.
4. Retrieve or verify current-project observations under
   `source-access-registry.md`.
5. Briefly disclose a remembered preference when it materially affects the
   result.
6. If a preference is incompatible or unsafe, explain the conflict and ask
   before changing it.
7. Apply an explicit user change immediately and record it as persistent only
   when the user asks or clearly states an ongoing preference.

## Memory limitations

Use only memory that the host actually exposes. Do not claim to remember across
sessions when no persistent-memory capability is available. In that case,
maintain the profile only within the current conversation and offer a concise
copyable preference profile if the user needs continuity elsewhere.

Do not silently edit this Skill or its permanent source registry from user
memory. Proposed permanent policy changes require an explicit maintenance
update.
