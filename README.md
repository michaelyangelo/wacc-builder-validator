# WACC Builder and Validator

This is an experimental, professional-facing skill for building WACC from
first principles and validating an existing build against a bundled
best-practice professional SOP.

It leads with construction: valuation perimeter, method choice, source-dated
inputs, cost of equity, after-tax cost of debt, capital weights, calculated
WACC, selected WACC, and the rate actually applied. When a user supplies a
workbook or calculation for review, it also performs a side-by-side comparison
with the bundled SOP and identifies defensible exceptions, gaps, omissions,
double counting, and unsupported adjustments.

The workflow is self-contained. It uses the bundled SOP and references,
user-provided evidence, and authorised capabilities available in the active AI
product.

## Install and use

Keep this repository as one complete folder. `SKILL.md`, `agents/`,
`references/`, `scripts/`, and both license files belong together. Python 3.10
or newer is required to execute the deterministic calculation helpers.

See [INSTALLATION.md](INSTALLATION.md) for Codex, Claude, and Excel setup steps
and a first-use prompt. Fresh installation and full walkthrough checks in the
named AI hosts remain pending.

## Main workflow

1. Build the WACC.
2. Validate the build and compare it with the professional SOP.
3. Test application consistency, sensitivity, and valuation impact.
4. Conclude and prepare the report.

The skill first shows an executive summary, one compact rate bridge, up to
three priority findings, and a four-section contents table. Detailed work is
shown only after the user selects a section, asks a specific question, or asks
for the full walkthrough.

## Contents

- [Skill instructions](SKILL.md)
- [Bundled professional WACC SOP](references/wacc-best-practice-sop.md)
- [Calculation-helper contract](references/calculation-helpers.md)
- `scripts/` — deterministic calculation and validation helpers

This repository is the standalone skill. Install the complete repository
folder; downloading only `SKILL.md` omits required references and helpers.

## Scope and boundaries

The skill can determine that WACC is inappropriate and route to a project,
claim-specific, APV, SOTP, impairment, lease, liability, or term-structure
method. It does not force every discount-rate problem into WACC.

Naming a paid provider does not create access. When an authorised connector is
available, the host may use it. Otherwise, the skill requests an authorised
export. It never bypasses subscriptions or invents market data.

It is not an audit, fairness opinion, investment recommendation, market-data
terminal, full valuation opinion, or automatic workbook-repair tool.

This skill is dual-licensed at your option under the MIT License or Apache
License 2.0. See [LICENSE-MIT](LICENSE-MIT) and
[LICENSE-APACHE](LICENSE-APACHE).
