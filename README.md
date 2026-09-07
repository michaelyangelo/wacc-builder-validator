# Build a WACC you can explain and defend

Build a source-backed WACC or review one you already have. Follow the inputs
and assumptions, check the calculation, and see how the calculated rate
compares with the rate actually used in your model.

## Start here

Copy this one prompt into the AI app where you want to use the skill. You do
not need to know its setup process or choose a brand first.

```text
Set up WACC Builder and Validator from: https://github.com/michaelyangelo/wacc-builder-validator
The complete ready-to-upload package is also here: https://github.com/michaelyangelo/wacc-builder-validator/raw/refs/heads/main/wacc-builder-validator-skill.zip
Use the complete skill, including its references and calculation helpers. Confirm that all required package files are available and whether the helpers can execute in this app.
Install it for future use if this app supports that. Handle the download and setup yourself wherever possible.
If a manual upload is required, give me the ready-to-upload file and the exact next action. If you can only use it within this conversation, explain that clearly and load the complete package for this session.
Confirm what is ready and whether it will remain available in future conversations. Do not claim installation or successful checks that you could not perform.
```

The app should choose the route it supports:

- **Automatic setup:** it fetches and installs the complete skill, then tells
  you whether it will remain available later.
- **Upload:** download the [ready-to-upload ZIP](https://github.com/michaelyangelo/wacc-builder-validator/raw/refs/heads/main/wacc-builder-validator-skill.zip)
  and upload it exactly as supplied. Do not rename or repack it.
- **Current conversation:** if the app cannot install it for future use, attach
  that ZIP and ask it to use the complete skill for this conversation only. It
  must say that the setup is temporary and whether the helpers can execute.

If a required capability is missing, the app should state the precise gap
instead of implying that setup or checks succeeded.

## First use

Attach your workbook and send:

```text
Use WACC Builder and Validator on this workbook. Review and reconstruct an existing WACC; if I ask for a new WACC, build it from first principles. Preserve the original workbook, cite exact cells, separate calculated, selected, and applied rates, and label unverified evidence.
```

Expect a concise rate summary, one rate bridge, up to three priority findings,
and a guided next step. See [INSTALLATION.md](INSTALLATION.md) for the route
details and optional technical notes.

Fresh host-installation and full-workbook walkthrough tests are still pending.

The skill is a guided WACC review tool. It is not an audit, fairness opinion,
investment recommendation, market-data terminal, full valuation opinion, or
automatic workbook-repair tool. The repository publishes a skill package; it
is not a Microsoft 365 Copilot agent or ChatGPT plugin.

This skill is licensed under the Apache License 2.0. See
[LICENSE-APACHE](LICENSE-APACHE).
