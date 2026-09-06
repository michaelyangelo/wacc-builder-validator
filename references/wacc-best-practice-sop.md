# Best-Practice Professional WACC SOP

Use this reference to build a WACC and to benchmark an existing user or
workbook build. It is a disciplined professional baseline, not a claim that one
formula fits every industry, valuation purpose, or capital structure.

This file is the canonical end-to-end workflow. Use the specialist references
for detail rather than expanding the checklist here:

- `usd-anchor-and-beta-coherence.md` — mandatory regional base-rate policy,
  beta/ERP coherence, beta paths, country-risk conventions, and peer data;
- `discount-rate-method-map.md` — formulas, adjustments, rate bridges, and
  Excel output;
- `valuation-perimeter-and-implied-rates.md` — valuation object, cash-flow and
  claim classification, method switches, and implied rates;
- `economic-reasonableness-gate.md` — diagnostics and reliance status;
- `source-access-registry.md` — source hierarchy, dates, fields, and access.

## SOP sequence

### 1. Define the valuation object

- Fix the valuation date, perimeter, ownership basis, and claim.
- Confirm that the cash flow is nominal, post-tax, unlevered FCFF.
- Confirm currency, geography, duration, and terminal-value convention.
- Switch to cost of equity, project rate, APV, SOTP, waterfall, or claim-by-
  claim analysis when WACC does not match the discounted object.

### 2. Freeze the evidence date and source pack

- Use the latest permitted observation on or before the valuation date.
- Record provider, dataset/field, instrument, currency, units, and date.
- Verify the exact company, security, index, peer, rating scale, and source.
- Apply the evidence classes defined in `../SKILL.md`; do not create a parallel
  evidence taxonomy.

### 3. Build the risk-free and exposure adjustments

- Apply the mandatory EU/EEA German-Bund and outside-EU/EEA U.S.-Treasury
  policy in `usd-anchor-and-beta-coherence.md`.
- Record the valuation currency and cash-flow basis and separately evidence the
  adjustments required by that policy.
- Reconcile overlap with FX, inflation, forecasts, scenarios, debt spread, and
  terminal assumptions.

### 4. Build cost of equity

- Select and lock beta Path Q, P, or R under
  `usd-anchor-and-beta-coherence.md`; reporting-stage language alone does not
  change an agreed method.
- Match beta and ERP and apply the selected peer debt/cash convention
  consistently.
- Add country, size, liquidity, or company-specific adjustments only when
  evidenced, relevant, and not already captured.

### 5. Build marginal cost of debt

- Start from the required Bund or U.S.-Treasury base.
- Add a current issuer, issue, comparable, or supported rating spread matched
  for currency, seniority, maturity, security, and rating scale.
- Treat coupons and historical interest expense as diagnostics, not the primary
  marginal debt cost.
- Apply the supported marginal tax rate and state any tax-shield limitation.

### 6. Build capital weights

- Use same-date ordinary-equity market value and book value of debt under the
  mandatory house policy. Use market value of debt only when the user asks for
  it, then apply that basis consistently and show the effect of the change.
- Address cash, leases, pensions, minorities, preferreds, convertibles,
  warrants, shareholder loans, and non-recourse/project debt explicitly.
- Use a target or peer capital structure only when the selection policy is
  documented and economically appropriate.
- Do not force a conventional WACC while a material hybrid claim is unresolved.

### 7. Calculate and reconcile

- Show cost of equity, pre-tax debt cost, after-tax debt cost, capital weights,
  calculated WACC, selected WACC, and applied WACC separately.
- Use visible formulas and preserve units and rounding.
- Reconcile overrides, ranges, manual overlays, and differences between the
  calculated, selected, sensitivity-midpoint, and applied rates.

### 8. Test application and economic reasonableness

- Match nominal/real, pre-/post-tax, levered/unlevered, currency, timing,
  duration, geography, and valuation date.
- Investigate when pre-tax or after-tax debt cost is above ordinary-equity cost,
  comparing like-for-like claim, currency, date, maturity, and tax bases. Treat
  the ordering as a diagnostic, not a universal hard rule.
- Check country, currency, size, liquidity, and specific-risk double counting.
- Run bounded sensitivity and quantify valuation or decision impact.
- Use market-implied or transaction evidence only as a separately labelled
  cross-check with matched perimeter, claim, date, and cash-flow basis.
- State readiness: ready to use, ready with caveats, or not ready to rely on.

## Existing-build comparison contract

When a user supplies a workbook or calculation for review:

1. Reconstruct the user's build exactly before proposing changes.
2. Map each SOP stage to the user's cells, formulas, sources, or missing data.
3. Classify each stage as `Aligned`, `Defensible exception`, `Gap`, `Not
   applicable`, or `Not testable`.
4. Explain why any exception may be industry- or purpose-specific.
5. Quantify the WACC impact in basis points when it can be calculated without
   invented inputs.
6. Separate mechanical errors from methodological judgement and evidence gaps.
7. Preserve the user's original workbook and assumptions unless editing is
   explicitly requested.

Do not call a difference a defect merely because the user used another accepted
method. The comparison should identify where the build is weaker, stronger, or
simply different from this SOP and what that means for reliance.

