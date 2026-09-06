# Calculation helpers

Read this reference before running a bundled helper. These scripts perform
bounded calculations and checks; they do not fetch data, inspect a workbook,
verify a provider, or establish that a qualitative financial judgment is true.
Retain the evidence contract and the mandatory house methodology in SKILL.md.

## Run a helper

Python 3.10 or newer is required. All three helpers use only the Python
standard library. Run them from the installed skill folder, or use absolute
paths to the script and input file.

Use `python3` where the host names Python that way. All accept `--input -` for
JSON on standard input. Success writes JSON to standard output with exit code 0.
Invalid data or an unreadable file writes a JSON error to standard error with
exit code 2; no result should be used. Command syntax errors also exit with 2.
A gate result of BLOCKED is a successfully completed check, not a script error.
Always inspect the returned status and evidence gaps, not just the exit code.

The beta helper also retains its older positional-file invocation.
Python callers can use `assess(payload)` in the gate or beta module and
`_solve(payload)` in the solver; invalid inputs raise the module's `InputError`.

## Units

- Rates, premiums, tax rates, debt weight, and terminal-value shares are
  fractions: `0.09` means 9%, `0.25` means 25%. Beta is a multiple.
- Basis-point thresholds are in basis points: `100` means one percentage point.
- Monetary amounts must use one currency and scale within a calculation.
  For each peer, debt and equity must use the same currency and scale.
- Dates use `YYYY-MM-DD`. Periods are years from the valuation date.
- Use finite JSON numbers. Numeric fields never accept strings such as
  `"9%"`, `"Unverified"`, booleans, NaN, or Infinity.

## Reverse DCF: solve_implied_rate.py

| Input | Contract |
| --- | --- |
| `value_basis` | Required: `enterprise` or `equity` |
| `cash_flow_type` | Required: FCFF for enterprise; FCFE for equity |
| `value` | Required positive value in the same currency/scale as cash flows |
| `cash_flows` | Required ascending list; plain numbers mean years 1, 2, 3…; objects contain `period` and `amount`, with omitted period defaulting to its 1-based position |
| `timing` | `end` by default; `mid_year` subtracts 0.5 from each explicit period; effective periods must remain positive |
| `terminal_cash_flow_next_year` | Optional normalized period n+1 cash flow, already grown; requires terminal_growth |
| `terminal_growth` | Required with terminal cash flow, otherwise omitted; must exceed −100% |
| `rate_bracket` | Optional `[lower, upper]` in decimal units; upper > lower, lower > −100%, and lower > growth when a terminal value exists |

The terminal value is `terminal_cash_flow_next_year / (r - g)` and is discounted
at the end of the final explicit period, including under mid-year explicit
timing. Do not use this helper for another terminal-timing convention.
Normalized year-n cash flow 100 at 2% growth means an input of 102.

The former `terminal_cash_flow` key is rejected because its year was ambiguous.
Migrate by establishing the input year from evidence; multiply a year-n amount
by `1 + g` exactly once before passing it as next-year cash flow.

Without terminal value the default bracket is 0–100%. With terminal value its
lower bound is `max(0, g + 0.000001)` and its upper bound is
`max(1, lower + 1)`. These are search bounds, not a reasonable-rate opinion.
If no root exists in that bracket, supply a justified bracket. Negative rates
require an explicit admissible bracket.

The supported cash-flow class has at most one negative-to-positive sign change,
including the initial negative value being solved against. Nonnegative forecasts
and leading forecast losses followed by nonnegative receipts are supported.
A later negative cash flow after positive receipts, or a negative perpetuity,
is rejected: the helper cannot guarantee a unique rate for those cases.
Do not treat a grid search or one returned root from another ad hoc calculation
as proof of uniqueness.

Output includes `implied_rate`, `implied_rate_percent`, value `residual`,
`explicit_cash_flow_pv`, `terminal_value_pv`, `terminal_value_share`,
the terminal inputs/timing, used bracket, and `uniqueness_basis`.
The value residual tolerance is `max(1e-11, abs(value) * 1e-12)`.
Terminal-value share can exceed 1 when explicit-period present value is negative.
The rate remains market-implied under the supplied assumptions.

## Peer beta: calculate_peer_beta.py

| Input | Contract |
| --- | --- |
| `valuation_date` | Required ISO date; no observations or source dates after it |
| `target_benchmark` | Required exact benchmark identifier/name |
| `target_erp_market` | Required description of ERP market universe |
| `target_return_currency` | Required return currency |
| `target_erp` | Required positive ERP fraction |
| `target` | Required object with nonnegative debt, positive equity, and tax_rate in [0, 1) |
| `peers` | Required nonempty list; select and evidence the peer set under the skill's beta-path rules |

Each peer needs `name` (or receives a generated label), `source_erp` (>0),
`debt` (>=0), `equity` (>0), `tax_rate` ([0,1)), `benchmark`,
`return_currency`, `erp_market`, and `source`. Optional `weight` is positive
and defaults to 1; supplied weights are normalized in the weighted mean.

For observed beta, also supply `levered_beta`, `source_date`, `frequency`,
`lookback`, and `beta_adjustment` (for example raw or the provider's named
adjustment). Preserve actual metadata; do not invent it to satisfy the helper.

For regression, supply `observations` instead of levered_beta. Each observation
contains date, stock level, and market level; both levels must be positive.
Also supply `price_type` (adjusted_close or total_return) and `frequency`:

- `five_year_monthly`: one observation per month across 60 calendar-month
  intervals, normally 61 levels; at least 60 usable adjacent-period returns.
- `two_year_weekly`: one observation per week across 103–105 week intervals,
  reflecting an approximately two-year window; at least 60 usable returns.

Monthly/weekly series must end within 35/10 days respectively before the
valuation date and contain unique ascending valid dates. These limits allow
normal reporting/trading-calendar differences; they do not establish that an
observation was the final traded price of its period. Verify period-end
selection and actual security/price provenance separately.

The regression requires the target benchmark and return currency for all
series. Returns across missing periods are excluded, never forward-filled
or treated as ordinary one-period returns. `minimum_returns` may increase the
60-return floor, not reduce it. Run monthly and weekly windows separately and
compare them under Path R. A successful single regression does not establish
that both Path R windows or the full review were completed.

Output includes each peer's metadata, levered/unlevered and normalized beta,
weight, and regression diagnostics when applicable: observations, alpha,
R-squared, beta standard error/t-statistic, first/last dates, and excluded gap
returns. Aggregate outputs include weighted and median unlevered/relevered beta
on the target ERP basis. `cross_benchmark_approximation` identifies differing
source benchmarks/ERP descriptions. Observed cross-benchmark normalization
remains the disclosed approximation in the house policy.

`calculation_only: true` and `source_and_erp_coherence: requires_evidence_review`
mean exactly that: the script checks numbers and metadata presence/cadence.
It does not prove that an ERP is appropriate for the named index, that prices
are genuine total returns, or that the peer selection is financially appropriate.

## Economic gate: economic_reasonableness_gate.py

One call covers one valuation object/claim, schedule, currency, tax basis, and
timing convention. All supplied rates must refer to that same application;
use separate calls for different applications. `terminal_growth`, if supplied,
declares a Gordon-growth terminal model for this schedule and is tested against
each supplied rate.

| Input | Contract |
| --- | --- |
| `calculated_rate` | Required finite rate greater than −100% |
| `selected_rate` / `applied_rate` | Optional finite rates greater than −100%; omit or use null when absent |
| `method_evidence_supported` | Method and valuation-object evidence reviewed |
| `cash_flow_evidence_available` | Matching cash-flow evidence available |
| `application_basis_supported` | Supplied rates match this claim, currency, tax/leverage and timing basis |
| `selected_rate_evidence_supported` / `applied_rate_evidence_supported` | Evidence for the actual selection/application, each independently required when supplied |
| `debt_cost_policy_match` | Required for applicable WACC debt; unknown must not pass |
| `hybrid_treatment_resolved` | Required for WACC; supported also means the scan established no material unresolved claims |
| `debt_weight` | Optional fraction in [0,1]; an evidenced zero makes debt-cost checks not applicable |

These seven evidence fields accept `supported`, `unsupported`, or `unknown`.
Boolean true/false are aliases for supported/unsupported; omission or null
means unknown. `not_applicable` is permitted only for debt_cost_policy_match
when debt_weight is zero. Keep the supporting source register; these are
assertions by the caller, not script verification of source documents.

Other controls use true, false, or null, not text. Set the applicable trigger
flags explicitly; the helper cannot infer omitted source usage from a rate:

| Controls | Effect |
| --- | --- |
| `conventional_wacc_requested` / `professional_wacc_requested` | Apply WACC evidence and regional house-policy requirements |
| `region_basis` / `base_rate_anchor` / `cash_flow_currency` | eu_eea + bund or outside_eu_eea + us_treasury; actual currency remains required for WACC |
| `beta_used` / `beta_erp_match` | Require a supported pairing when beta is used |
| `unmatched_scenario_explicitly_requested` | Allows an unknown pairing only as an explicitly requested unverified scenario; never ready to rely on |
| `market_source_bundle_used` / `source_bundle_coherent` | Coherence must be true when the bundle is used |
| `external_market_inputs_used` / `latest_available_source_vintage_used` | Appropriate source vintage must be affirmed when external inputs are used |
| `market_security_values_used` / `security_source_match` | Subject/security identity must match |
| `rating_spread_proxy_used` / `rating_scale_mapping_supported` | Rating mapping must be supported |
| `currency_basis_adjustment_supported` | Required when the cash-flow currency differs from the regional anchor |
| `country_risk_overlap` / `basis_mismatch` | True blocks reliance |
| `new_mechanical_wacc_from_blocked_inputs` | True blocks an invented mechanical result from unresolved inputs |
| `beta_path` / `quick_path_explicitly_selected` | Path Q/P/R; Q remains provisional and requires explicit selection for professional WACC |
| `beta_range_used` / `beta_range_basis_supported` | A used range needs a supported basis |
| `external_reliance_requested` / `highest_effort_requested` / `material_decision` / `beta_coherence_problem` | Identify when Path R validation is warranted under the existing policy |
| `regression_data_available` | Flags warranted regression not run when data exist; a reporting request alone does not switch paths |
| `capital_stack_issue` | Flags a material capital-stack diagnostic; does not substitute for required hybrid-treatment evidence |

Optional numeric diagnostics: `risk_free_rate`, `cost_of_equity`,
`pre_tax_cost_of_debt`, `after_tax_cost_of_debt`, `terminal_growth` (>−100%),
`terminal_value_share`, `market_implied_rate`, and nonnegative
`market_gap_warning_bps`. A terminal share above 1 or below 0 is preserved
and flagged for explanation, not clamped.

Output: `status`, `reliance_state`, `hard_blocks`, `flags`, `missing_evidence`,
normalized `evidence_states`, `diagnostics`, and `rate_assessments` for
calculated/selected/applied. Every per-rate assessment retains the supplied
number, its status, reasons, missing evidence, and terminal diagnostics.

BLOCKED takes precedence over NOT TESTABLE, which takes precedence over
CAUTION/PASS. Missing required evidence, absent selected/applied rates, or
unverified scenarios prevent a reliance approval. CAUTION with complete
required evidence can be Ready with caveats; Path Q remains provisional.
The helper never selects, applies, edits, or silently normalizes a rate.
