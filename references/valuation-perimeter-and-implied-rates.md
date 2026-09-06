# Valuation Perimeter and Implied Rates

Use this reference when the rate method may be wrong for the valuation object,
when the capital stack contains hybrid or ring-fenced claims, or when inferring
a rate from market value and forecast cash flows.

## Contents

1. Valuation perimeter
2. Claim and capital-stack scan
3. Cash-flow classification
4. Method selection
5. Project versus parent analysis
6. Market-implied rates
7. Transaction double-counting
8. Terminal normalization
9. Output and reliance language

## 1. Valuation perimeter

Record the following before choosing a rate:

- valuation date;
- legal entity and economic perimeter;
- asset, project SPV, subsidiary, segment, parent, or consolidated group;
- ownership basis: consolidated, attributable, minority, or specific interest;
- enterprise value, ordinary equity value, preferred value, debt value, or
  liability value;
- operating, financing, tax, and cash-flow boundaries;
- currency in which the relevant cash flows are denominated or economically
  fixed.

Record legal domicile, listing location, valuation currency, and cash-flow
basis. Apply the mandatory regional base-rate and separate-adjustment policy in
`usd-anchor-and-beta-coherence.md`; this file does not redefine it.

If the perimeter cannot be established from the workbook, filings, or user
brief, label the result provisional and ask one blocking question only when
the answer could change the method.

## 2. Claim and capital-stack scan

Search the workbook and supporting sources for:

- ordinary shares;
- preferred shares and RCPS;
- convertibles and exchangeables;
- warrants and embedded options;
- perpetual securities;
- shareholder loans;
- senior, subordinated, mezzanine, and PIK debt;
- liquidation preferences;
- redemption rights;
- protected or guaranteed returns;
- project partners and minority interests;
- project-level non-recourse financing;
- parent guarantees and cross-defaults;
- sale-and-leaseback or similar financing obligations.

For each material claim record:

- principal or notional amount;
- ranking and recourse;
- cash distribution or coupon;
- maturity and redemption terms;
- conversion, warrant, or dilution rights;
- protection or return formula;
- whether it is issued, committed, or funded;
- evidence source and date.

Do not treat a preferred distribution, redemption IRR, coupon, expected return,
and ordinary-equity required return as interchangeable.

## 3. Cash-flow classification

Classify the actual cash flow being discounted:

| Classification | Required matching basis |
| --- | --- |
| FCFF | Enterprise value and WACC/enterprise discount rate |
| FCFE | Equity value and cost of equity |
| Project operating cash flow | Project operating or asset rate |
| Project cash after project debt | Project-equity return |
| Preferred distributions | Preferred claim return |
| Cash after tax and debt service | Equity-like; not direct FCFF |
| Liability or lease payments | Matched liability/borrowing rate |
| Provider-labelled FCF | Definition must be reconciled |

Check whether cash flow is before or after:

- interest;
- principal repayment;
- preferred distributions;
- taxes;
- working capital;
- project debt service;
- asset-sale proceeds;
- probability weighting;
- maintenance and growth capital expenditure.

If the definition is ambiguous, do not silently convert it into FCFF or FCFE.
Use an explicit scenario label or stop the implied-rate calculation.

## 4. Method selection

Use conventional WACC only when material claims and cash flows are compatible
with a debt/equity capital-weight calculation.

Use APV when operating value and financing effects should be separated.

Use claim-by-claim or waterfall analysis when securities have materially
different ranking, distributions, protection, redemption, or optionality.

Use project-versus-parent analysis when project assets have ring-fenced cash
flows or non-recourse financing but the parent also has corporate overhead,
growth options, refinancing risk, or expensive junior capital.

Use SOTP when segments have different currencies, geographies, contracts,
financing, or risk profiles.

Use a market-implied rate only after confirming the value and cash-flow basis.

## 5. Project versus parent analysis

Keep these labels separate:

- project operating rate;
- project-equity return;
- subsidiary or hold-company rate;
- parent-company market-implied rate;
- segment rate;
- consolidated cross-check.

Do not apply a parent rate mechanically to every project. Do not use a low
project rate to value expensive parent-level claims without allocating the
capital stack.

For a mixed group, show:

1. project or segment values;
2. project debt and non-recourse claims;
3. parent debt and preferred claims;
4. corporate overhead and other assets;
5. residual ordinary equity value.

## 6. Market-implied rates

Before reverse-solving, confirm:

- value date;
- market capitalisation or enterprise value date;
- FX date and currency conversion;
- net debt date and definition;
- FCFF or FCFE classification;
- forecast periods;
- annual versus mid-year timing;
- terminal growth;
- normalized terminal cash flow;
- transaction and asset-sale treatment.

For enterprise value, use FCFF. For equity value, use FCFE. If neither basis
is clear, report a scenario range rather than a single implied rate.

When `scripts/solve_implied_rate.py` is available, use it. The default
end-year equation is:

`Value = sum(FCF_t / (1+r)^t) + [TerminalFCF_(n+1) / (r-g)] / (1+r)^n`

Here `TerminalFCF_(n+1)` is the normalized cash flow after the final explicit
period `n`, and `g` is terminal growth. Do not discount the terminal value by
`n+1` periods or reuse an unnormalized disposal/milestone cash flow. If the
model uses mid-year convention, state that convention and use the same timing
for every explicit cash flow.

The solver input is `terminal_cash_flow_next_year`: supply the already-grown,
normalized `TerminalFCF_(n+1)` amount. It is not multiplied by growth again.
The ambiguous old `terminal_cash_flow` field is rejected. For example, final-year
normalized cash flow 100 and growth 2% require an input of 102. See
`calculation-helpers.md` for runnable inputs, rate-bracket defaults, and errors.

The helper discounts terminal value at the end of the final explicit period
even when explicit cash flows use mid-year timing. Use it only when that matches
the valuation. It supports nonnegative cash flows and leading forecast losses
followed by nonnegative receipts, with a nonnegative terminal cash flow.
It rejects a negative cash flow after positive receipts because the implied
rate may not be unique. Do not hand-solve around that rejection or present
one sampled root as unique; use a separately validated method or leave the
implied-rate check unresolved.

Report the unrounded rate, residual, terminal-value share, and sensitivity
inputs before presenting a rounded executive figure.

If the evidence provides both a stated enterprise/equity value and rounded
components that can recreate it, freeze the stated value as the primary solve
input. Recalculate the components as a separate bridge check and disclose any
rounding difference. If no stated value exists, calculate from the components
using their available precision.

The conclusion should say:

> The result is a market-implied discount rate under the stated cash-flow,
> timing, terminal, and capital-structure assumptions.

It should not say that the market has directly published or observed a WACC.

## 7. Transaction double-counting

For each material transaction, classify it as:

- completed before the valuation date;
- completed after the valuation date;
- signed but unclosed;
- included in the forecast;
- included in cash/net debt;
- included in terminal value;
- excluded.

Then reconcile whether the transaction affects both forecast cash flow and the
value/debt bridge. Remove or disclose duplicate treatment.

## 8. Terminal normalization

For lumpy project, FPSO, infrastructure, or backlog cash flows:

- identify non-recurring sale proceeds;
- separate contract milestone cash from recurring operations;
- normalize maintenance and replacement capital expenditure;
- check whether terminal cash flow includes a completed disposal;
- test terminal growth against long-run nominal economic assumptions;
- show terminal value as a percentage of total value.

At minimum, test terminal growth and normalized terminal cash flow. Add timing
or transaction sensitivities when they materially affect the inferred rate.

## 9. Output and reliance language

Use the evidence classes in `../SKILL.md` and the reliance status from
`economic-reasonableness-gate.md`; do not create another status taxonomy here.
Describe a reverse-solved result as **market-implied under the stated
assumptions**, not as an observed WACC. Never state that a single WACC is
reliable when the valuation object, claim, or cash-flow basis remains
unresolved.
