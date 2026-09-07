# Install and start your WACC review

Start with the setup prompt. Ask the AI app to choose the route it supports.

## One setup prompt

```text
Set up WACC Builder and Validator from: https://github.com/michaelyangelo/wacc-builder-validator
The complete ready-to-upload package is also here: https://github.com/michaelyangelo/wacc-builder-validator/raw/refs/heads/main/wacc-builder-validator-skill.zip
Use the complete skill, including its references and calculation helpers. Confirm that all required package files are available and whether the helpers can execute in this app.
Install it for future use if this app supports that. Handle the download and setup yourself wherever possible.
If a manual upload is required, give me the ready-to-upload file and the exact next action. If you can only use it within this conversation, explain that clearly and load the complete package for this session.
Confirm what is ready and whether it will remain available in future conversations. Do not claim installation or successful checks that you could not perform.
```

## Use the route the app reports

**Automatic setup.** If the app supports setup for future use, let it fetch and
install the complete skill. It should say whether it will remain available
later.

**Upload.** Download the [ready-to-upload ZIP](https://github.com/michaelyangelo/wacc-builder-validator/raw/refs/heads/main/wacc-builder-validator-skill.zip)
and upload that single file exactly as supplied. Do not rename or repack it.

**Current conversation.** If the app cannot install the skill for future use,
attach that ZIP and ask it to use the complete skill for this conversation. It
must say that the setup is temporary and whether the calculation helpers can
execute. If it cannot fetch the link, download the ZIP yourself and attach it.

## First use

Attach your workbook and send:

```text
Use WACC Builder and Validator on this workbook. Review and reconstruct an existing WACC; if I ask for a new WACC, build it from first principles. Preserve the original workbook, cite exact cells, separate calculated, selected, and applied rates, and label unverified evidence.
```

Expect a concise rate summary, one rate bridge, up to three priority findings,
and a guided next step. Fresh host-installation and full-workbook walkthrough
tests remain pending, so this guide does not claim that either has been tested.

<details>
<summary>Technical details and troubleshooting</summary>

The ZIP has one top-level folder and contains the complete runtime package:

```text
wacc-builder-validator/
├── SKILL.md
├── LICENSE-APACHE
├── agents/openai.yaml
├── references/
│   ├── calculation-helpers.md
│   ├── discount-rate-method-map.md
│   ├── economic-reasonableness-gate.md
│   ├── source-access-registry.md
│   ├── usd-anchor-and-beta-coherence.md
│   ├── user-parameter-memory.md
│   ├── valuation-perimeter-and-implied-rates.md
│   └── wacc-best-practice-sop.md
└── scripts/
    ├── calculate_peer_beta.py
    ├── economic_reasonableness_gate.py
    └── solve_implied_rate.py
```

The helpers require Python 3.10 or newer and use only the standard library.
If the host cannot execute Python, the helper checks remain unverified. Do not
install `SKILL.md` alone: the references and helpers carry the method and
calculation controls.

The guided review has four sections: build the WACC; validate an existing build
against the professional SOP; test application, sensitivity, and valuation
impact; then conclude and ready the result for reporting. It keeps calculated,
selected, and applied rates separate and cites exact workbook evidence.

The skill can identify when WACC is not the right method, but it is not an
audit, fairness opinion, investment recommendation, market-data terminal, full
valuation opinion, or automatic workbook-repair tool. Naming a paid provider
does not create access; provide authorised evidence when needed.

If the app says a reference or helper is missing, attach the complete ZIP
again. If it cannot install skills or read packages, it should report that
precise limitation rather than treating a generic WACC request as setup.

</details>
