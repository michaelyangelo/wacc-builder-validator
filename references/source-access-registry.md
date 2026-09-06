# Market-Data Source Access Registry

This is the maintainable source list for the Skill. It describes where to look,
not a promise that the runtime can access every source.

## Contents

1. Source hierarchy and observation dates
2. Exact public locations
3. Beta, ERP, and return-series source bundles
4. Section 1 build and Section 4 source behavior
5. Damodaran and licensed providers
6. Internal data and source experience
7. Capital-stack, forecast, and same-date controls

## Deterministic source hierarchy

Use this order unless the user supplies a documented internal policy:

1. authorised internal policy or user-mandated source;
2. primary official government, central-bank, regulator, issuer, or filing
   source;
3. connected and authorised licensed professional provider;
4. established valuation dataset or research source such as Damodaran Online;
5. secondary websites only to discover a primary source, never as the silent
   final source.

Within a review, lock the provider and dataset/series once selected. For the
same user, reuse a compatible remembered provider and dataset definition under
`user-parameter-memory.md`, but retrieve the observation appropriate to the
current valuation date. Do not change source merely because another website is
easier to retrieve.

## Observation-date rule

1. Use an observation on the valuation date when available.
2. If the market was closed or the series was not published, use the latest
   available observation before the valuation date.
3. Do not use an observation after the valuation date without explicit user
   approval and a visible exception note.
4. Do not substitute today's data for a historical valuation date.
5. When the user supplies a frozen evidence pack, use it without browsing for
   replacement data.

## Exact public locations

| Need | Preferred official location | Dataset or series rule |
| --- | --- | --- |
| USD government curve | [U.S. Treasury Daily Treasury Par Yield Curve Rates](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve) | Use the 10-year observation on or immediately before the valuation date unless another maturity is supported. |
| EU/EEA German Bund base | [Bundesbank — Yields of current Federal securities](https://www.bundesbank.de/en/statistics/overview-of-the-statistical-series/-/3-yields-of-current-federal-securities-914558); [direct CSV API](https://api.statistiken.bundesbank.de/rest/data/BBSSY/D.REN.EUR.A630.000000WT1010.A?format=csv&lang=en) | Use `BBSSY.D.REN.EUR.A630.000000WT1010.A` for the daily current 10-year Federal bond yield. |
| EUR fitted government curve | [Bundesbank — Daily term structure on listed Federal securities](https://www.bundesbank.de/en/statistics/money-and-capital-markets/interest-rates-and-yields/daily-term-structure-on-listed-federal-securities-651570) | Use only when the methodology calls for a fitted 10-year curve measure; do not silently substitute it for the current 10-year Bund series. |
| Euro-area curves and short rates | [ECB Data Portal — financial markets and interest rates](https://data.ecb.europa.eu/key-figures/financial-markets-and-securities/financial-markets-and-interest-rates) | Capture exact series key, measure, maturity, and compounding convention. |
| SOFR | [Federal Reserve Bank of New York — SOFR](https://www.newyorkfed.org/markets/reference-rates/sofr) | Capture observation date, publication date, tenor, and definition. |
| UK curves | [Bank of England — yield curves](https://www.bankofengland.co.uk/statistics/yield-curves) | Diagnostic cross-check only for WACC under the same-user regional-anchor policy; capture curve type, maturity, observation date, and compounding. |
| US filings and company facts | [SEC EDGAR](https://www.sec.gov/edgar/search-and-access) and [SEC data APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | Capture issuer, form, accession number, filing date, period, and exact field/page. |
| Damodaran current valuation datasets | [Damodaran Online — current data](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html) | Capture exact dataset, regional scope, update date, and methodology. |
| Damodaran industry beta data | [Damodaran current data](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datacurrent.html); [global industry beta table](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/BetasGlobal.html) | Capture global/regional scope, industry definition, levered/unlevered field, debt/equity convention, dataset date, and the ERP basis used with the beta. |
| Damodaran size-premium research | [Damodaran data index](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html); [public cost-of-equity chapter](https://pages.stern.nyu.edu/~adamodar/pdfiles/acf3E/ch4.pdf) | Capture the exact file or paper, historical window, size definition, market, whether the figure is over CAPM or the risk-free rate, and the dataset or publication date. Treat open historical research as research-derived, not automatically as a current valuation input. |
| Open academic size-factor cross-check | [Ken French Fama/French benchmark factors](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_bench_factor.html) | SMB is a small-minus-big return factor, not automatically a valuation size premium. Capture portfolio construction, market, period, and factor definition before using it as a cross-check. |
| Damodaran country risk | [Country Default Spreads and Risk Premiums](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html) | Capture country, rating/default-spread method, CRP/ERP field, and dataset date. |
| Damodaran historical implied ERP | [Historical Implied Equity Risk Premiums](https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/histimpl.html) | Use the latest observation on or before the valuation date and retain the ERP definition. |
| US macro series aggregator | [FRED API](https://fred.stlouisfed.org/docs/api/fred/) | Record the FRED series ID and underlying original publisher. |
| Global macro and sovereign data | [IMF Data](https://www.imf.org/en/Data), [World Bank Data](https://data.worldbank.org/), [OECD Data Explorer](https://data-explorer.oecd.org/), [BIS Data Portal](https://data.bis.org/), [Eurostat](https://ec.europa.eu/eurostat/web/main/data/database) | Capture dataset, series, definition, geography, currency, units, and observation date. |

Prefer official downloadable XLSX, CSV, API, or SDMX data. Use search results
only to find the official page. Record retrieval date separately from
observation date.

Always retain source, observation, publication, and retrieval dates in the
working source register. Do not display a source-date table or date column in
the executive summary unless the user asks. Surface a date without being asked
only when staleness or inconsistent dates could materially affect the result.
Selecting the source-review section counts as a request for the detailed dates.

## Beta, ERP, and return-series source bundles

Read `usd-anchor-and-beta-coherence.md` before selecting beta or ERP data. Lock
one source bundle for the valuation date and capture:

| Field | Required metadata |
| --- | --- |
| Risk-free anchor | U.S. Treasury or Bund series, maturity, observation date |
| Displayed beta | provider, field, benchmark, return currency, raw/adjusted, period, frequency, observation date |
| ERP | provider, market universe/index, implied/historical method, observation date, publication date |
| Country risk | provider, country/exposure basis, CRP or total-ERP field, lambda/scaling convention, date |
| Price history | security and benchmark identifiers, adjusted/total-return field, currency, frequency, corporate-action treatment, dates |
| Peer capital structure | market cap date, debt definition, cash treatment, leases/hybrids, tax convention, currency/FX date |

Apply the Path Q/P/R selection and matching rules in
`usd-anchor-and-beta-coherence.md`. For sourcing:

- Path Q requires the displayed beta's benchmark, currency, period, frequency,
  adjustment, and matched ERP; an unexplained `Beta (5Y)` is insufficient;
- Path P should use one provider/field convention where practical and retain
  each peer's matched ERP when benchmarks differ;
- Path R should use an authorised provider or user export containing:

  - peer and benchmark identifiers;
  - adjusted-close or total-return observations;
  - FX observations when required;
  - five-year monthly and two-year weekly histories ending on the valuation date;
  - same-date market capitalisation, book debt by default, cash, leases,
    hybrids, and tax fields;
  - field names, currencies, corporate-action settings, and applied filters.

Public price or index pages may support a provisional regression only when the
exact observations, identifiers, adjustment method, and benchmark definition
can be retained. Do not scrape around access restrictions or infer missing
corporate-action adjustments.

Before accepting any market price or security statistic, verify the exact
company name, ticker, exchange, security class, and valuation date on the source
page or export. Reject a source whose URL, page identity, or instrument does not
match the subject even when the displayed number appears plausible.

This is an affirmative gate: the source itself must expose enough identity to
confirm the instrument. A search-result snippet, unlabeled number, conflicting
URL slug, or page for another issuer is not acceptable. If identity cannot be
confirmed, omit the number and request an authorised exchange/provider export.

For Damodaran ERP, country-risk, and industry-beta inputs, prefer one official
dated workbook or table bundle. Do not use a social post, newsletter, or search
snippet for a numerical input when the official table or workbook is available.
If different Damodaran files imply different mature-market ERP bases, reconcile
the difference explicitly before combining them; otherwise the bundle fails.

Use the latest official observation or dated file available on or before the
valuation date, not merely the annual HTML table. For a date after a mid-year
update, inspect the official update page for linked NYU files such as
`ctrypremJulyYY.xlsx` and `ERPJulyYY.xlsx`, then cite the NYU file used. The
update post is discovery/methodology evidence; the linked file is the numerical
source. Record why an older vintage is used when the latest file is inaccessible.

For issuer spread proxies, record rating agency, national or global scale,
issuer or issue rating, seniority, currency, and mapping method. Never map a
domestic `AA+` label directly into a global USD spread table merely because the
letters match.

## Section 1 build-source pack

For each material parameter, identify the current value, exact source, source
reliability, relevance, date, currency, geography, and definition. Allow the
user to refine the parameter with preferred assumptions or replace it with
authorised internal or user-provided data.

Retain lower, central, and upper parameter values in the working review when
the evidence supports a reasonable range. Section 3 uses those ranges for
sensitivity and valuation impact.

## Section 4 source behavior

Supply the exact workbook reference, public dataset, licensed field, internal
document, or user-provided assumption required by the Section 4 structure in
`discount-rate-method-map.md`. Do not redefine the report or Excel layout here.
Keep dates in the working register and surface them when requested or when
timing materially limits reliance.

## Damodaran Online

Use the official NYU Stern Damodaran pages for implied ERP, historical ERP,
country-risk premiums, industry betas, default spreads, and archived datasets.
Capture the exact spreadsheet or page and its dataset date. Treat Damodaran as
transparent research/dataset evidence, not as a live market terminal.

Use the latest dated Damodaran release available on or before the valuation
date. Do not use a later monthly ERP or annual beta/CRP update merely because it
is newest at the retrieval date. When the same user has a remembered Damodaran
dataset definition, reuse that definition when it remains applicable, but
retrieve the valuation-date observation rather than an old project's value.

When combining Damodaran beta, ERP, and CRP, prefer fields from one dated
official workbook or reconcile the conventions explicitly. Use a LinkedIn post,
newsletter, or secondary summary for explanation only when the official table
or workbook containing the numerical input is available.

## Licensed providers

Potential providers include Bloomberg, S&P Capital IQ Pro, LSEG Workspace,
FactSet, Kroll Cost of Capital Navigator, Moody's, S&P Ratings, and Fitch.

Kroll's current size-premium fields are licensed data. Treat Kroll like the
other paid providers in this list: use them only through a connected and
authorised capability or an authorised user export. Public Kroll research may
be cited as research, but it is not evidence that the current subscription
dataset was accessed.

Runtime procedure:

1. inspect connected and authorised provider capabilities;
2. call the exact capability if available;
3. request only required peers, fields, dates, and identifiers;
4. record provider, product, field name, identifier, date, currency, and licence
   status;
5. if unavailable, ask for an authorised XLSX/CSV export;
6. if only PDF/image is supplied, mark extraction and verification limits.

For beta Path R, request price histories and peer capital-structure fields in
one same-date bundle. Use this minimum request:

```text
Please provide an authorised XLSX/CSV export for the named peers and selected
benchmark containing adjusted or total-return prices, FX where needed, market
capitalisation, gross book interest-bearing debt by default, cash, lease
liabilities, hybrid claims, tax rate, field identifiers, currencies, and dates.
Use market value of debt only when requested. Include five years of month-end
and two years of week-end observations ending on the valuation date.
```

For EU/EEA cost-of-debt work, first seek current issuer spread or
yield-to-maturity reconciled to the Bund anchor. For work outside the EU/EEA,
first seek current issuer USD-bond or credit-spread evidence and build from the
U.S. Treasury anchor. In both routes, add supported sovereign/currency-basis
and issuer adjustments. Use a local-currency issuer yield only as a diagnostic
cross-check. Use rating-based spreads as a disclosed fallback. Treat stated
coupons as historical contractual terms, not current marginal borrowing costs.

For size-premium work, also capture the subject-company size measure, portfolio
or decile, market, currency, valuation date, dataset date, and whether the
premium is measured over CAPM or over the risk-free rate. Do not combine a
licensed size premium with an open SMB factor or another liquidity premium
without reconciling the definitions.

Never bypass a subscription or claim to have accessed a paid source without a
connected capability or user-provided export.

Known provider names and discovery aliases:

| Provider | Search aliases |
| --- | --- |
| Bloomberg | Bloomberg, Bloomberg Terminal, B-PIPE |
| S&P Capital IQ Pro | Capital IQ, CapIQ, S&P CIQ |
| LSEG Workspace | LSEG, Refinitiv, Workspace, Eikon |
| FactSet | FactSet |
| Kroll Cost of Capital Navigator | Kroll, Cost of Capital Navigator, Duff & Phelps |
| S&P RatingsDirect | RatingsDirect, S&P Ratings |
| Moody's | Moody's, Moody's Ratings |
| Fitch | Fitch, Fitch Ratings |

Naming a provider does not prove that its capability is installed. If no
provider-specific capability is available, request an authorised export rather
than calling an unrelated Skill.

## Internal data

Possible internal evidence includes treasury curves, debt schedules, bank
quotes, approved peer groups, valuation policy, tax models, prior transaction
models, management forecasts, board materials, and adviser correspondence.

Use this citation form:

`[Internal: owner/function — document or system — as-of date — version — page, tab, cell, or section]`

Label internal data **Internal-observed** only when the underlying document or
export is available. Otherwise label it **User-provided**.

## Source experience log

When a source is used or corrected, record:

- provider and dataset;
- supported input type;
- geography and currency;
- public, licensed, or internal status;
- update frequency;
- strengths and known limitations;
- last verification date;
- preferred, approved, fallback, or prohibited status;
- user corrections.

Do not silently promote a source or infer that an organisation approves it.

## Capital-stack and instrument evidence

For preferred, hybrid, project-finance, or parent-level claims, prefer:

1. instrument prospectus, circular, term sheet, or subscription agreement;
2. issuer annual or interim financial statements;
3. stock-exchange or regulator filing;
4. transaction announcement and completion notice;
5. financing and covenant disclosures;
6. project-finance documentation or lender material supplied by the user;
7. authorised licensed-provider data;
8. secondary reporting only for discovery.

Capture whether an amount is issued, committed, or funded. Distinguish coupon,
distribution rate, expected return, protected IRR, redemption return, and
ordinary-equity required return. A security's headline return is not
automatically a WACC input.

## Analyst forecast and free-cash-flow evidence

Before using a provider or analyst "FCF" series in an implied-rate calculation,
identify whether it is FCFF, FCFE, post-interest cash flow, cash after debt
service, or another provider-specific definition. Capture the provider's field
definition, period, forecast date, and source documentation. If the definition
cannot be established, mark the implied-rate result provisional and do not call
it market-implied WACC.

## Same-date bridge control

For market-implied calculations, record and reconcile the dates for:

- market capitalisation or enterprise value;
- FX conversion;
- gross debt, cash, and net debt;
- forecast cash flows;
- completed transactions;
- terminal assumptions.

Do not silently combine a current market value with an old net-debt bridge or a
forecast date that has already incorporated a transaction. State the roll or
adjustment when exact same-date data is unavailable.

## Public-evidence wording

When a search does not identify an instrument or disclosure, say **no public
evidence found** as of the stated retrieval date. Do not state that an
instrument does not exist merely because the public search did not find it.

If a user-provided file names a provider or dataset but the Skill has not
accessed that source directly, label the evidence:

`User-provided claim: [provider/dataset] - not independently verified`

Only label it **External-observed** after direct access. Preserve the exact
provider, dataset or series, observation date, and retrieval date consistently
in the bridge, source register, and conclusion.

Screenshots may preserve load-bearing visual evidence when the source page or
table is difficult to cite, but they supplement the official page, file, or
dataset. Never fabricate a screenshot or use one to conceal an unavailable
source.

