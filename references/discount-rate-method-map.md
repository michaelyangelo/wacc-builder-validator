# Discount-Rate Method Map

Use this file for method classification and transparent reconstruction. The
main Skill controls interaction, evidence labels, and reliance language.

## Contents

1. Coded rate-bridge format
2. Common formulas
3. Rate/application rule
4. Background sensitivity
5. Excel and Section 4 output
6. Risk and adjustment map
7. Valuation object, capital stack, and implied-rate methods

## Coded rate-bridge format

Use one table for direct inputs and calculated outputs:

| Code / formula | Parameter or result | Value | Source |
| --- | --- | ---: | --- |
| `a` | Risk-free rate | 3.0% | Bundesbank |
| `b` | Equity risk premium | 4.5% | Damodaran Online |
| `c` | Beta | 1.2x | Peer analysis |
| `d = a + (b x c)` | Cost of equity | 8.4% | Calculated |

Continue the same code chain through capital weights, after-tax cost of debt,
calculated rate, selected rate, and applied rate. Keep units visible. Do not
repeat the inputs in a separate calculation table. Use a short source label in
the executive bridge. Do not add a status column.

## Common formulas

### CAPM-style cost of equity

Apply the mandatory regional base-rate policy, beta/ERP coherence gate, and
country-risk convention in `usd-anchor-and-beta-coherence.md`:

`Ke = Rf_regional + beta_matched x ERP_matched + separately supported adjustments`

Possible additions such as country, size, liquidity, or company-specific risk
must be identified separately and checked for overlap.

Do not restate or combine country-risk formulas here. Use exactly one convention
selected under the coherence reference and do not double count CRP.

### Size premium

Use a size premium only when the selected modified-CAPM or build-up method and
the subject company's size evidence support it. Do not add a size premium to
every public-company WACC by default.

For a supported calculation:

`Ke_adjusted = Rf + beta x ERP + size premium + other documented equity adjustments`

Carry `Ke_adjusted` into WACC through the equity weight. Do not add the size
premium directly to debt cost or to the final weighted WACC.

Before using the premium, identify:

- subject-company status: public, private, listed but illiquid, small-cap, or
  micro-cap;
- size measure: market capitalisation, MVIC, assets, revenue, employees, or
  another documented measure;
- size portfolio, decile, breakpoint, currency, geography, and dataset date;
- whether the reported figure is a premium over the risk-free rate or over CAPM;
- whether the source is open research, licensed data, internal evidence, or a
  user-provided assumption;
- why the premium is relevant to the subject company and valuation purpose.

Do not equate a Fama/French SMB factor or a historical small-versus-large return
spread with a current valuation size premium without reconciling the definition,
portfolio construction, time period, and market. Check for double counting with
beta, ERP, liquidity, country risk, company-specific risk, and forecast
adjustments. If only open historical or academic evidence is available, label
the result research-derived and provisional and show a reasonable range.

### WACC

`WACC = E/(D+E) x Ke + D/(D+E) x Kd x (1 - tax rate)`

Include preferred or hybrid capital only when it is actually part of the model.
Use same-date market value of ordinary equity and book value of debt under the
mandatory house policy. Use market value of debt only when the user asks for it;
show the source, date, and effect of changing the debt basis.

### Cost of debt

Use the regional anchor selected under `usd-anchor-and-beta-coherence.md`:

`Kd = Rf_regional + supported sovereign/currency-basis adjustment + issuer credit spread + documented debt-specific adjustments`

Check seniority, maturity, currency, security, liquidity, and whether the
spread is already reflected in an observed borrowing rate.

Use the following evidence hierarchy:

1. current issuer bond spread or yield matched for seniority, maturity, and the
   required regional base;
2. current lender quote or issuer credit curve expressed over the required
   regional base;
3. recent issuance spread or yield reconciled to the required regional base;
4. current comparable traded spread or rating-based spread plus the required
   regional base and supported sovereign/currency-basis adjustment;
5. existing coupon, historical interest expense, or accounting debt cost only
   as a diagnostic cross-check, never the primary WACC debt cost.

Do not confuse historical coupon, effective interest expense, average embedded
debt cost, and current marginal borrowing cost.

If the required regional-base debt spread or supported proxy is unavailable,
leave cost of debt unresolved and do not calculate headline WACC.

### Unlevering and relevering beta

Read `usd-anchor-and-beta-coherence.md` and use one disclosed path.

For peer `i`:

`beta_u_i = beta_l_i / [1 + (1 - tax_i) x (D_i / E_i)]`

When all peer betas use the same benchmark and ERP, aggregate the unlevered
betas directly. When they use different benchmarks, preserve each matched
beta/ERP pair and normalize the unlevered risk contribution:

```text
risk_contribution_i = beta_u_i x ERP_i
risk_contribution_target = sum(weight_i x risk_contribution_i)
beta_u_target_basis = risk_contribution_target / ERP_target
beta_l_target = beta_u_target_basis x
                [1 + (1 - tax_target) x (D_target / E_target)]
```

This does not pretend that relevering changes the benchmark. It converts the
matched peer risk contributions onto the selected target-ERP basis before
relevering.

For regression multi-verification, calculate periodic simple total returns:

`return_t = adjusted_level_t / adjusted_level_(t-1) - 1`

Then:

`beta = covariance(stock returns, benchmark returns) / variance(benchmark returns)`

Use one common benchmark and return currency for all peers where possible.
Run five-year monthly and two-year weekly variants when data are sufficient.
Use `scripts/calculate_peer_beta.py` for the deterministic calculation. Show
observation count, alpha, R-squared, beta standard error, exclusions, weighting,
and a median cross-check behind the detailed route.

See `calculation-helpers.md` for the exact input contract. The regression helper
checks the calendar window and uses only returns between adjacent periods;
returns spanning missing periods are excluded. It requires at least 60 usable
returns and a common regression benchmark and return currency. Its output is
a calculation, not independent verification of source identity, price
adjustments, or the economic beta/ERP pairing. Keep those evidence checks.

### Real and nominal conversion

`1 + nominal rate = (1 + real rate) x (1 + inflation rate)`

Do not mix a real rate with nominal cash flows, or vice versa.

### Pre-tax equivalent rate

Do not reverse-engineer a pre-tax equivalent rate without showing the exact
cash-flow and tax convention used. The conversion is method-dependent and may
not be a simple division when taxes vary over time.

### Term structure

For spot, forward, or duration-matched methods, preserve the period, maturity,
compounding, day-count, interpolation, and discount-factor convention.

## Rate/application rule

- Use WACC for unlevered enterprise cash flows.
- Use cost of equity for levered equity cash flows.
- Use debt or liability-specific rates only for matching debt, lease, provision,
  pension, or liability cash flows.

Do not substitute one rate for another without reconciling the cash-flow basis.

## Background sensitivity

Run a bounded sensitivity before finalising the executive conclusion. Vary the
material inputs for the selected method, normally risk-free rate, ERP, beta,
size premium when applicable, credit spread, and capital weights. During Section 1, develop lower, central,
and upper values for each material parameter. During Section 3, use those
ranges to quantify the discount-rate and valuation impact. If Section 3 is
selected before Section 1, develop the needed parameter ranges in the
background.

In the executive summary, disclose only:

- the indicative discount-rate range;
- the high-level valuation impact; and
- the single largest rate driver, when material.

Show the detailed sensitivity only when requested or when Section 3 is selected.

## Default Excel bridge

When the user asks for an Excel output without explicitly requesting a full or
detailed report, create only one new worksheet named `Provisional WACC Bridge`
(add a safe numeric suffix if that name already exists). This is the default
artifact, including when the user has chosen Section 4 in chat.

The worksheet must contain only one compact coded bridge with these columns:

| Code / formula | Parameter or result | Value | Source |
| --- | --- | ---: | --- |

Enter direct inputs in input cells and use real Excel formulas for every
calculated value. Formulas must reference the bridge input cells or exact
source-workbook cells; do not paste calculated values as static numbers. Keep
calculated, selected, and applied rates separate. If selected or applied rates
were not supplied, label them `Not supplied` or `Unverified` rather than
inventing values.

Do not add a source-audit block, findings sheet, sensitivity sheet,
comparables, checks, navigation, or report narrative to the default workbook.
Do not overwrite or alter the model's original calculation sheets.

After creating the bridge, offer one optional next action: `create full Excel report`.
Do not create the expanded output unless the user explicitly chooses that action
or asks for an equivalent full/detailed Excel report.

## Section 4: Conclude and ready to report

Produce a stripped-down report with two blocks.

### Block 1 — Discount-rate bridge

Include only:

- method and cash-flow/application basis;
- core direct inputs;
- core calculated components;
- capital weights when applicable;
- calculated, selected, and applied rates.

Use:

| Code / formula | Parameter or result | Value | Source |
| --- | --- | ---: | --- |

Keep the code chain complete from direct input to final rate. Exclude route
instructions, long findings, methodology essays, detailed sensitivity tables,
review questions, and optional enhancements. Do not add a status column.

### Block 2 — Parameter sources

Place this immediately below the bridge:

| Code | Parameter | Value | Data source |
| --- | --- | ---: | --- |

Include every direct input used by a formula. Do not list calculated rows as
independent sources. Show source dates only when requested or when timing is a
material limitation. Do not add a status or evidence-class column.

### Expanded Excel implementation

Only when the user explicitly requests a full/detailed Excel report:

1. create a new report-only worksheet without overwriting an existing sheet;
2. put direct inputs in dedicated cells and assign their codes in the adjacent
   formula/code column;
3. put working Excel formulas in calculated result cells, referencing the
   report input cells or exact source-workbook cells;
4. prefer a workbook link such as `='WACC'!B5` for workbook-observed inputs;
5. enter external or user-provided values as inputs and identify their sources
   in the source block;
6. keep calculated, selected, and applied rates separate.

Keep material unresolved evidence gaps in the conclusion rather than adding a
status column to either table.

## Risk and adjustment map

For each adjustment, record: risk intended, evidence, value/rate location,
materiality, and overlap risk.

- country/sovereign risk;
- currency and inflation;
- credit spread and debt seniority;
- size and liquidity;
- concentration and project stage;
- construction, contract, regulatory, or customer risk;
- company-specific or scenario risk;
- control and marketability.

Country and currency items must be reconciled with the base government rate,
ERP, debt spread, FX assumptions, forecast adjustments, and scenarios.

## DLOM and DLOC treatment

DLOM and DLOC normally belong in the value bridge, not the WACC formula.
Confirm the value basis, ownership level, control rights, marketability,
application order, evidence, and overlap with other discounts or premiums.

## Evidence, valuation objects, and implied rates

Use the evidence classes in `../SKILL.md`, the existing-build comparison statuses
in `wacc-best-practice-sop.md`, and the reliance statuses in
`economic-reasonableness-gate.md`. Do not create a fourth overlapping taxonomy.

Use `valuation-perimeter-and-implied-rates.md` as the authority for valuation
object and claim labels, capital-stack method switches, cash-flow
classification, market-implied-rate reconstruction, transaction
double-counting, and terminal normalization. This file supplies formulas and
output structures only.
