# Economic-Reasonableness Gate

## Contents

- [Purpose](#purpose)
- [Execution order](#execution-order)
- [Required inputs and evidence states](#required-inputs-and-evidence-states)
- [Checks](#check-0--input-stack-coherence)
- [Gate statuses](#gate-statuses)
- [Front-end output policy](#front-end-output-policy)
- [User commands](#user-commands)
- [Excel behavior](#excel-behavior)

## Purpose

Run this gate after calculating a rate and before presenting it as selected or
ready to use. The gate asks what the rate means economically, not merely
whether the arithmetic works.

Read `usd-anchor-and-beta-coherence.md` first. A calculation that violates the
base-rate or beta/ERP policy is mechanically reproducible but not method-ready.

Do not use a universal WACC floor. A low rate may be correct for a low-risk
asset, while a high rate may be wrong for a protected cash flow. Use the gate
to identify consequences, missing support, and contradictions.

## Execution order

1. Complete the method, perimeter, capital-stack, beta/ERP coherence, and
   evidence checks.
2. Calculate the mechanical rate and keep calculated, selected, and applied
   rates separate.
3. Run this gate silently before the executive opening.
4. Apply the output policy below.
5. Show detailed diagnostics only when necessary to prevent misuse or when the
   user asks `why`, `show me economic check`, `compare rates`, or `sensitivity`.

Do not expose hidden chain-of-thought. Provide concise conclusions and the
supporting calculations or evidence when explanation is required.

## Required inputs and evidence states

Use only inputs that are available and labelled:

- valuation object and claim;
- cash-flow definition and matching value basis;
- calculated rate and rate type;
- EU/EEA or outside-EU/EEA classification and base-rate anchor;
- beta Path Q, P, or R; beta benchmark and ERP market universe;
- country-risk convention and currency/inflation/basis adjustment;
- debt-cost anchor and marginal-spread evidence;
- subject name, ticker, exchange, and source-identity match;
- source-bundle coherence and any rating-scale mapping;
- selected and applied rates, if supplied;
- risk-free rate and cost of equity, where relevant;
- terminal growth and terminal cash flow, if a DCF is available;
- enterprise/equity value and forecast cash flows, if a reverse DCF is
  possible;
- material hybrid claims, financing rights, or capital-stack exceptions;
- external comparison rates or multiples, only with source and date.

If an input is missing, mark the relevant check `Not testable`. Do not invent a
terminal growth rate, enterprise value, forecast, market-implied rate, or
comparison multiple.

Run `scripts/economic_reasonableness_gate.py` using the contract in
`calculation-helpers.md` when Python execution is available. Supply one claim,
cash-flow schedule, currency, tax basis, and timing basis per call. Use separate
calls when rates apply to different objects or schedules. Evidence states are
assertions backed by the working source register; the script cannot independently
verify a workbook, provider, or qualitative judgment.

The helper requires affirmative method, cash-flow, and application-basis evidence.
For WACC it also requires capital-stack treatment and applicable debt-cost
evidence. Zero debt weight makes debt cost not applicable. Supplied selected and
applied rates need their own supporting evidence. Missing evidence remains
unknown; placeholder text belongs in the report, never in numeric JSON fields.

## Check 0 — Input-stack coherence

Before interpreting the calculated result, verify:

- the calculation passes the mandatory regional base-rate and separate-
  adjustment policy in `usd-anchor-and-beta-coherence.md`;
- the beta/ERP bundle passes the coherence gate in that reference;
- country risk is included once under one disclosed convention;
- cost of debt uses the required regional anchor and current supported issuer
  spread or proxy, not historical interest expense;
- each market-price and security source matches the exact subject instrument;
- the external inputs form one coherent, valuation-date source bundle;
- a domestic rating is not mapped to a global USD spread table without a
  documented scale, seniority, currency, and mapping basis;
- peer betas use each peer's own comparable D/E and tax inputs under the
  selected book- or user-requested market-debt convention;
- any available Path R validation not performed for external reliance is
  disclosed without silently changing the agreed beta path.

Block reliance when the mandatory regional-anchor policy fails, beta and ERP
are knowingly mismatched, or a material currency/basis adjustment is omitted.
Also block headline WACC when debt-cost policy, source identity, source-bundle,
rating-mapping, or material hybrid-claim treatment is unresolved. An unknown
displayed-beta benchmark is allowed only in an explicitly requested unmatched
scenario. Path Q requires explicit user selection. Block unsupported beta
ranges and stale source vintages.

## Check 1 — Claim-specific return meaning and component ordering

For a conventional WACC, show the components separately:

- cost of equity;
- `Ke - Rf`, the equity risk premium implied by the calculation;
- after-tax cost of debt;
- WACC and its blended financing meaning.

Do not call `WACC - Rf` the equity investor's required return. For preferred,
convertible, warrant, project-equity, or other claims, examine the return and
priority of that claim separately.

Treat an unusually low implied equity premium as a diagnostic signal only. It
requires independent support from cash-flow stability, contractual protection,
peer or market evidence, or documented policy. It does not by itself prove
that the rate is wrong.

Compare pre-tax cost of debt, after-tax cost of debt, and ordinary-equity cost
when all three are available. Ordinarily investigate when either debt cost is
materially above ordinary-equity cost. Do not make the ordering a universal
hard rule: distress and recovery assumptions, claim seniority, subsidies,
convertibility, guarantees, tax effects, currency, date, maturity, or
inconsistent measurement bases may explain the result. Compare like-for-like
claims and bases, show the difference in basis points, and identify the
explanation or leave it unresolved.

## Check 2 — Valuation consequences

When terminal growth and a rate are available, calculate the terminal-value
multiple and label its denominator:

```text
TV / next-year FCFF = 1 / (r - g)
TV / current-year FCFF = (1 + g) / (r - g)
```

Also calculate, when the necessary inputs exist:

- terminal value as a percentage of enterprise or equity value;
- implied terminal EV/EBITDA;
- implied terminal P/E or FCF yield;
- sensitivity to the rate and terminal growth;
- distance between the rate and terminal growth.

If `r <= g`, block reliance on the result. A narrow distance or high terminal
concentration is a warning, not automatic proof of error. Compare the result
with the model's own forecast and independently sourced peer or transaction
evidence when available.

Apply these checks separately to calculated, selected, and applied rates. A
valid calculated rate does not approve a different selected or applied rate.
Keep an observed invalid applied rate visible and identify its failed check.
Terminal value can exceed 100% of total value when explicit-period present value
is negative. Explain that diagnostic; do not cap the ratio or reject it merely
for exceeding 100%.

## Check 3 — Market-implied cross-check

When a same-date enterprise/equity value, matching FCFF/FCFE schedule, timing,
net debt, and terminal assumptions are available, run the bundled reverse-DCF
solver.

Record:

- bottom-up calculated rate;
- market-implied rate under the stated assumptions;
- difference in basis points;
- value date and cash-flow definition;
- whether accepting the bottom-up rate implies market mispricing or a forecast
  difference.

Do not call a market-implied rate an observed WACC. If the cash-flow schedule
or value basis is missing, mark this check `Not testable`.

## Check 4 — Risk-location map

For each material risk, record where it is priced:

| Risk | Forecast | Scenario | Terminal growth | Discount rate | Unpriced | Overlap |
| --- | --- | --- | --- | --- | --- | --- |

Check at least:

- country and sovereign risk;
- currency and inflation;
- size and liquidity;
- company-specific and execution risk;
- project, regulatory, customer, and contract risk;
- risk from completed or expected transactions.

Do not count the same risk in the rate and cash flows without an explicit
reconciliation.

## Check 5 — Capital-claim and application gate

Downgrade or block the output when:

- enterprise value is paired with FCFE or equity value with FCFF;
- a project rate is presented as a parent-company rate;
- a material convertible, RCPS, warrant, preferred, or protected claim is
  treated as ordinary debt or ordinary equity without analysis;
- the rate's currency, tax basis, leverage basis, or timing does not match the
  application;
- a calculated rate is presented as selected or applied without evidence.

Use APV, claim-by-claim, waterfall, project-versus-parent, or SOTP treatment
when one WACC cannot represent the material claims and risks.

## Gate statuses

Use the following internal statuses:

- **PASS:** no material economic inconsistency was found using available
  evidence;
- **CAUTION:** the calculation is usable only with a concise limitation;
- **BLOCKED:** a material contradiction or method mismatch prevents reliance;
- **NOT TESTABLE:** required cash-flow, value, terminal, market, or claim
  evidence is missing.

Combine this status with the Skill's reliance state. `PASS` does not make an
unverified selected or applied rate ready to use. `NOT TESTABLE` normally keeps
the result provisional and not ready to rely on; it describes the missing
economic check, not the availability of a mechanical calculation. `BLOCKED`
prevents approval of the affected rate. Preserve independently observed selected
or applied rates as facts even when their application is blocked.

## Front-end output policy

### PASS

Present the normal executive summary and bridge. Do not mention the gate.

### CAUTION

Add one concise limitation, for example:

> The calculation is mechanically consistent but remains provisional because
> the current capital structure and terminal-value assumptions are not fully
> supported.

### BLOCKED

Show the mechanical rate but not as the selected rate:

> Calculated WACC: 3.55%. Status: not ready to rely on as the selected rate.
> The result is affected by an unresolved capital-claim or valuation-basis
> issue.

Give only the single most important reason. Keep the supporting calculations
behind `why` or `show me economic check`.

### NOT TESTABLE

Show the strongest available mechanical or provisional calculation, then state
which economic application cannot yet be tested and the minimum evidence or
stronger beta path needed next. Do not respond with only `Not testable`, and do
not invent a replacement selected rate.

## User commands

- `why` — explain the flagged conclusion with concise evidence and formulas;
- `show me economic check` — show terminal multiples, risk-location map,
  reverse-DCF comparison, and source dates where available;
- `compare rates` — compare bottom-up, market-implied, project, segment, or
  claim-specific rates without treating them as interchangeable;
- `compare beta routes` — compare Path Q, P, and R inputs, benchmark/ERP pairs,
  betas, cost of equity, WACC, data quality, and reliance state;
- `sensitivity` — show bounded rate, growth, and valuation consequences;
- `challenge` — ask one professional question about the most important open
  economic issue.

## Excel behavior

Follow the default and expanded Excel structures in
`discount-rate-method-map.md`. Do not create a separate gate worksheet. If the
gate blocks reliance, place one concise status and reason in the existing
selected/applied-rate rows; include detailed diagnostics only in an explicitly
requested expanded report.

