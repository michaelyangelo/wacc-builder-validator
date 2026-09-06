# Build a WACC you can explain and defend

Build a source-backed WACC or review one you already have. Follow the inputs
and assumptions, check the calculation, and see how the calculated rate
compares with the rate actually used in your model.

Start with a compact rate summary and the main points to review. Then work
through the details, ask questions, and prepare your conclusion.

Choose your AI tool below to get started.

## Get started

Use the complete repository folder: `SKILL.md`, `agents/`, `references/`,
`scripts/`, and the Apache-2.0 license file belong together. Downloading only
`SKILL.md` leaves out the method and calculation helpers.

Follow the short, host-specific steps in [INSTALLATION.md](INSTALLATION.md).
The supported starting routes are local Codex installation and Claude skill
upload. Fresh end-to-end tests in those hosts are still pending.

## What you will see first

With enough evidence, the skill opens with a concise summary, one rate bridge,
up to three priority findings, and the next review sections. If material
evidence is missing, it asks for that evidence instead of inventing inputs.

## What the review covers

1. Build or reconstruct the WACC.
2. Check it against the bundled professional SOP.
3. Test whether the selected rate is applied consistently and assess valuation impact.
4. Prepare a concise conclusion.

The skill separates the calculated, selected, and applied rates so that a
reasonable calculation is not confused with how the rate was used in the model.

## Contents

- [Skill instructions](SKILL.md)
- [Installation and first-use guide](INSTALLATION.md)
- [Bundled professional WACC SOP](references/wacc-best-practice-sop.md)
- [Calculation-helper contract](references/calculation-helpers.md)
- `scripts/` — deterministic calculation and validation helpers

## Boundaries

The skill can identify when WACC is not the right method and route to a more
appropriate approach. It is not an audit, fairness opinion, investment
recommendation, market-data terminal, full valuation opinion, or automatic
workbook-repair tool.

It uses authorised evidence and capabilities available in the host. Naming a
paid provider does not create access; where needed, supply an authorised export.

This skill is licensed under the Apache License 2.0. See
[LICENSE-APACHE](LICENSE-APACHE).
