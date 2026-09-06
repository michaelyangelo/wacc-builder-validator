# Regional Base-Rate Anchor and Beta/ERP Coherence

Use this reference for every WACC or CAPM-style calculation. It defines the
base-rate policy, beta/ERP matching rules, beta-effort paths, peer-data
conventions, and escalation conditions.

## Contents

1. Hard base-rate policy
2. Regional base-rate risk build
3. Premium and overlap control
4. Beta/ERP coherence gate
5. Beta-effort paths
6. Peer capital-structure convention
7. Regression-data convention
8. Default and escalation rules
9. Output and reliance rules

## 1. Hard base-rate policy

Use only these primary base-rate anchors unless the user explicitly changes
this same-user policy:

- **EU/EEA:** liquid 10-year German Bund yield.
- **Outside the EU/EEA:** liquid 10-year U.S. Treasury yield.

EU/EEA includes non-Eurozone EU members and EEA countries. These calculations
remain on the German Bund route.

Do not use another national government yield as the risk-free-rate input. Do
not convert the German Bund or U.S. Treasury yield into a synthetic local
risk-free rate. Another sovereign curve may be shown only as a diagnostic
cross-check.

Record the valuation currency and cash-flow basis before applying this regional
policy. The EU/EEA or outside-EU/EEA classification selects the base anchor;
the valuation currency and cash-flow basis determine the separately evidenced
country, sovereign, currency/inflation/basis, and other justified adjustments.

## 2. Regional base-rate risk build

For EU/EEA work, keep the German Bund as the base input even when the cash flow
is not denominated in EUR. Build the rate transparently:

```text
Ke = Rf_Bund
   + beta_matched x ERP_matched
   + country/sovereign-risk adjustment
   + currency/inflation/basis adjustment
   + size premium, when supported
   + other separately justified equity adjustments
```

The currency/inflation/basis item is an explicit adjustment, not a replacement
local risk-free rate. It may be positive, zero, or negative. Identify its
method, source, date, cash-flow currency, and economic meaning. Never add an
undocumented generic "currency premium."

Do not set this adjustment to zero merely because cash-flow, FX, or inflation
evidence is missing. Use zero only when evidence shows that the currency effect
is already captured or immaterial. Otherwise leave cost of equity and WACC
incomplete and identify the minimum evidence needed.

For work outside the EU/EEA, keep the U.S. Treasury as the base input even when
the cash flow is not denominated in USD. Build the rate transparently:

```text
Ke = Rf_USD
   + beta_matched x ERP_matched
   + country/sovereign-risk adjustment
   + currency/inflation/basis adjustment
   + size premium, when supported
   + other separately justified equity adjustments
```

If the cash-flow conversion, FX path, and terminal assumptions already contain
the relevant currency effect, the currency/inflation/basis adjustment may be
zero. Explain that result rather than adding another premium.

## 3. Premium and overlap control

For every additive adjustment, record:

- risk intended;
- formula and scaling convention;
- source and observation date;
- affected cash flow, geography, currency, segment, or claim;
- whether the risk is already reflected in ERP, beta, debt spread, FX,
  inflation, forecast cash flows, scenarios, probability weights, terminal
  growth, or another adjustment;
- lower, central, and upper values when judgement is material.

Use separate exposure as the default country-risk convention:

```text
Separate exposure: Ke = Rf + beta x mature ERP + lambda x CRP + adjustments
```

The beta-scaled total-ERP formula may be used only as a clearly labelled
alternative convention when a supported exposure-specific lambda cannot be
estimated and the selected provider or user methodology explicitly uses it:

```text
Beta-scaled total ERP: Ke = Rf + beta x (mature ERP + CRP) + adjustments
```

State that this convention assumes ordinary market beta is also a proxy for
country-risk exposure. Do not present that assumption as directly measured, and
do not add the CRP again. Do not use legal domicile as the sole country-risk
allocation. Weight exposure by supported revenue, EBITDA, assets, project cash
flow, contract counterparty, or another disclosed economic basis.

## 4. Beta/ERP coherence gate

Before calculating cost of equity, create one CAPM input bundle containing:

- beta provider and field;
- benchmark index;
- stock-return currency;
- benchmark-return currency;
- raw or adjusted beta;
- lookback period and observation frequency;
- observation or retrieval date;
- ERP provider, market universe, method, and date;
- country-risk convention;
- peer debt/equity and tax definitions where applicable.

The beta benchmark and ERP market universe must correspond. Examples:

| Beta benchmark | Corresponding ERP |
| --- | --- |
| S&P 500 in USD | U.S. ERP |
| MSCI World or MSCI ACWI in USD | Corresponding global/mature-market ERP |
| STOXX Europe 600 in EUR | ERP defined for its European market universe, with any methodological reconciliation disclosed; not automatically a eurozone ERP |
| Named local equity index | ERP defined for that named local market |

If the provider does not disclose the benchmark, currency, frequency, or
lookback, label the beta `Provisional fallback`. Do not present a selected rate
as ready to rely on from that beta. Find the metadata, choose a peer route, or
escalate to regression multi-verification.

Do not assume that unlevering or relevering changes a beta's market benchmark.
When peer betas use different benchmarks, normalize their unlevered risk
contributions before aggregation as described below.

## 5. Beta-effort paths

Keep these paths inside Section 1 and Section 2. They are not additional
top-level walkthrough sections.

### Path Q - Quick matched observed beta

Use only when the user explicitly asks for or accepts a quick/provisional
calculation. Limited public evidence alone does not authorise automatic use.

1. Obtain an observable company or industry beta.
2. Identify its benchmark, return currency, period, frequency, and adjustment.
3. Select the ERP corresponding to that benchmark.
4. Apply the EU/EEA or outside-EU/EEA base-rate policy.
5. Add separately justified country, currency/basis, size, or other premiums.

If a displayed company beta's benchmark cannot be identified, do not put it in
cost of equity or WACC by default. Seek a disclosed matched industry beta and
ERP from one dated dataset, such as the relevant Damodaran global or regional
industry bundle. If no matched pair is available, leave the beta component
unresolved and recommend Path P or R. Use an unmatched mechanical scenario
only when the user explicitly requests it. Quick never qualifies a material
external conclusion as ready to rely on.

An industry beta fallback is still Path Q. Do not relabel it Path P. State the
industry, region, dataset date, beta field, and ERP field, and confirm that both
come from one coherent provider methodology or are explicitly reconciled.

### Path P - Peer-normalized bottom-up beta

This is the default professional path when named peer data are available but a
full return-series regression is not proportionate.

Actively identify a defensible peer set from business-description and segment
evidence. Do not treat the absence of a user-supplied peer list as permission
to fall back immediately to Path Q.

For a normal professional WACC request, attempt to identify at least three
named operating peers. If this cannot be done, record the search performed and
the specific evidence gap, block the beta component, and offer Path Q as a
user-selected provisional fallback; do not run it automatically.

For each peer `i`:

```text
beta_u_i = beta_l_i / [1 + (1 - tax_i) x (D_i / E_i)]
risk_contribution_i = beta_u_i x ERP_i
```

If every beta uses the same benchmark and ERP, aggregate `beta_u_i` directly.
If peer betas use different local benchmarks, first aggregate matched risk
contributions:

```text
risk_contribution_target = sum(weight_i x risk_contribution_i)
beta_u_target_basis = risk_contribution_target / ERP_target
beta_l_target = beta_u_target_basis x
                [1 + (1 - tax_target) x (D_target / E_target)]
```

This preserves the beta/ERP pairing before expressing the result on the chosen
S&P 500, MSCI World, MSCI ACWI, or other supported target-market basis.
Treat cross-benchmark risk-contribution normalization as an interpretive
professional approximation, not as a directly observed common-index beta.
Use Path R as a common-index validation when warranted; do not silently replace
an agreed Path P result.

Show weighted average and median cross-checks. Disclose weighting and peer
exclusions. Do not average levered betas or mix gross-debt, net-debt, lease, or
tax definitions silently.

### Path R - Regression multi-verification

Select this path up front for the highest-effort calculation, material external
reliance, or when Path Q or Path P fails the coherence gate. A later reporting
request alone does not change the selected path.

1. Choose one target benchmark and matching ERP before collecting prices.
2. Use the same benchmark, return currency, price definition, end dates, and
   frequency for all peers where data permit.
3. Prefer adjusted prices or total-return series. Convert peer and benchmark
   values to the same currency before calculating returns when required.
4. Run both standard windows when data are sufficient:
   - five years of month-end observations: target 60 aligned returns, requiring
     at least 61 price levels;
   - two years of week-end observations: use all aligned weekly observations
     and require at least 60 usable returns; do not discard valid weeks merely
     to force exactly 60.
5. Regress each peer's returns against the chosen benchmark returns.
6. Record raw beta, alpha, R-squared, standard error, observation count, missing
   periods, price adjustments, stock splits, liquidity concerns, and exclusions.
7. Unlever each peer using its own same-date market-equity value, selected debt
   basis, and tax convention.
8. Aggregate unlevered betas, show median and weighted average, then relever to
   the supported target capital structure.
9. Pair the final beta with the ERP for the exact regression benchmark.
10. Compare the five-year monthly and two-year weekly results and explain the
    selected result or range.

Use `scripts/calculate_peer_beta.py` for deterministic return regression,
unlevering, cross-benchmark normalization, aggregation, and relevering.

## 6. Peer capital-structure convention

Use an apple-to-apple peer dataset:

- market capitalisation measured on one common date or the latest common prior
  trading date;
- gross interest-bearing debt by default for beta unlevering;
- cash excluded from debt unless a documented method explicitly uses net debt;
- gross debt is the default because it requires fewer potentially stale or
  inconsistent peer cash inputs; use net debt only when the selected method
  requires it and same-date cash is available consistently for all peers and
  the target;
- leases treated consistently for every peer and the target;
- preferred, convertible, pension, minority, or hybrid claims treated
  consistently or separated;
- book value of debt used under the mandatory house policy, including when a
  market value is observable; use market value of debt only when the user asks
  for it, then apply that basis consistently across peers and target and show
  the before/after effect;
- effective tax treatment applied consistently, with statutory tax as a
  disclosed fallback;
- one currency-conversion date and source for aggregation weights.

Calculate each peer's D/E individually. Do not unlever every peer with a common
average D/E. Use the target's supported capital structure for final relevering;
use a peer-average target only when that is the documented selection policy.

Do not calculate headline conventional WACC while a material convertible,
preferred, warrant, protected return, or other hybrid remains included as
ordinary debt or equity. Resolve the claim treatment or produce a capital-claim
bridge instead.

## 7. Regression-data convention

Use actual traded-price observations, not a displayed beta, for Path R. Keep:

- security and benchmark identifiers;
- trading venue and primary listing;
- adjusted-close or total-return definition;
- date, timezone, currency, and FX series;
- corporate-action treatment;
- missing or non-synchronous observations;
- liquidity and stale-price checks;
- source provider and field identifiers;
- retrieval date and licence status.

Align observations by common period end. Do not forward-fill missing stock or
benchmark prices merely to reach the minimum sample. Exclude or qualify a peer
when the usable series fails the required data-quality checks.

## 8. Default and escalation rules

Select and recommend one path before calculating the rate:

- default to **Path P** for a normal professional WACC request with named peers;
- use **Path Q** only after the user explicitly chooses a quick/provisional
  result; when Path P data are unavailable, offer Q rather than auto-running it;
- select **Path R** up front when the user asks for the toughest, highest-effort,
  multi-verified, or externally relied-on analysis; the decision is material;
  Path Q/P coherence fails; or regression verification is otherwise warranted.

Path R validation is warranted before reliance when:

- beta metadata are missing or different peer benchmarks cannot be normalized;
- beta and ERP fail the coherence gate;
- peer results vary materially by index or lookback;
- the rate is decision-critical or intended for external reliance;
- the economic-reasonableness gate identifies a material contradiction;
- the user asks for the toughest, highest-effort, or multi-verified route.

Once the user has reviewed or agreed a Path P or Q result, a later request for
`ready to report`, Section 4, or polished output does not authorise a silent
Path R recalculation. State that higher-reliance validation would require Path
R and offer it under the active interaction rules. If the user selects it, or
the existing path fails a blocking coherence rule, identify the method change
and show the prior and revised inputs, rate, and valuation impact when
available.

If licensed data are unavailable, request a minimum authorised export. Preserve
verified partial components, but do not silently downgrade to Path Q.

Do not create beta ranges from unrelated sectors, a total-market beta, or an
arbitrary percentage overlay. Every lower/central/upper beta must have a named
methodological or empirical basis consistent with the selected path.

Do not use historical interest expense, an embedded accounting debt cost, or a
local issuer yield as the primary debt-cost input. If a current issuer spread
or supported proxy reconciled to the required German-Bund or U.S.-Treasury
anchor cannot be obtained, show the debt component as unresolved and do not
calculate headline WACC.

A local or domestic rating can support a USD spread proxy only after its scale,
seniority, issuer/issue basis, and mapping to the selected global spread table
are documented. A label such as `AA+` is not automatically comparable across
rating agencies or national and global scales.

## 9. Output and reliance rules

Record in the working review:

- base-rate policy and observation;
- beta path Q, P, or R;
- beta benchmark and ERP market universe;
- source bundle and dates;
- country-risk convention;
- currency/basis adjustment and overlap check;
- peer capital-structure convention;
- five-year monthly and two-year weekly comparison when Path R is used.

The opening remains concise. Show only the chosen beta path, matched beta/ERP,
core rate bridge, and one material limitation. Put regression diagnostics,
alternative paths, and full peer tables behind Section 1, Section 2, `show me
beta`, or `compare beta routes`.

Do not convert a provisional mechanical result into a selected or applied rate.
When the economic application cannot be tested, say that the calculation is
available but the selected/application conclusion remains provisional; do not
respond with only `Not testable`.

Before using a market price, security statistic, filing, or historical series,
affirmatively verify the exact company name, ticker, exchange, security class,
and valuation date in the page, file, or structured response. A conflicting
page title, URL identity, ticker, or instrument invalidates the number; missing
identity leaves it unverified and unusable.

