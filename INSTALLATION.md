# WACC Builder and Validator — installation and first-use instructions

Version 0.1.1. Setup documentation checked on 6 September 2026. Local helper
validation is complete; fresh installation and full walkthrough checks in the
named AI hosts remain pending.

This skill helps you build or review a WACC, follow its sources and
calculations, and distinguish the calculated rate from the rate selected and
actually used.

## 1. Download the complete skill

Use the repository at
[michaelyangelo/wacc-builder-validator](https://github.com/michaelyangelo/wacc-builder-validator).
Select **Code → Download ZIP**, or clone the repository.

Keep `SKILL.md`, `agents`, `references`, `scripts`, and the Apache-2.0 license file
together. Downloading only `SKILL.md` omits the calculation and validation
resources.

You need an AI host that can read the full skill folder and execute Python 3.10+
for the deterministic helpers. Workbook review also needs workbook access;
live public-data retrieval needs browsing. Licensed data requires your own
authorised connection or export. No third-party Python libraries or API keys
are required to run the bundled helpers.

## 2. Codex — install the standalone skill

1. Download and extract this repository.
2. Rename the extracted folder `wacc-builder-validator` if the download added a
   branch suffix such as `-main`.
3. Choose the project/work folder you will open in Codex.
4. Inside that folder, create `.agents/skills` if it does not already exist.
5. Copy the complete `wacc-builder-validator` folder into it. The resulting
   file must be
   `your-project/.agents/skills/wacc-builder-validator/SKILL.md`.
6. Open that project in Codex and start a new task. If the skill does not appear,
   restart Codex.
7. Use the activation prompt below. Let Codex use the bundled files and Python
   helpers when needed.

```text
Use $wacc-builder-validator to review the WACC in the attached workbook.
Start by reconstructing its existing calculation. Keep the original workbook
unchanged and show calculated, selected, and applied rates separately.
```

An alternative is to ask Codex's skill installer to install the skill from this
repository. See [OpenAI's local skill guidance](https://learn.chatgpt.com/docs/build-skills).

## 3. Claude — upload the standalone skill

1. Enable **Code execution and file creation** in Settings → Capabilities.
   Managed accounts may need an organisation administrator to enable skills.
2. Download this repository and keep it as one complete folder. If needed,
   rename the extracted folder `wacc-builder-validator`, then compress that
   folder as a ZIP.
3. Open **Customize → Skills**.
4. Select **+ → Create skill → Upload a skill** and upload the ZIP.
5. Enable the uploaded skill.
6. Start a new conversation, attach your workbook or paste your inputs, and say:

```text
Use the WACC Builder and Validator skill to review this WACC.
Reconstruct the existing build, identify unsupported inputs or application
mismatches, and give me the compact opening bridge before the detailed walkthrough.
```

If the upload control is unavailable, check account or organisation
permissions. These steps follow
[Claude's custom-skill instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## 4. Claude for Excel

1. Enable the standalone skill in the Claude account used by the add-in.
2. Open the workbook in Excel and open Claude for Excel.
3. Ask it to use **WACC Builder and Validator** on the current workbook.
4. Request a review first. Ask it to cite the exact input, formula, and
   applied-rate cells so you can check that it has access to this workbook.
5. To create an output worksheet, explicitly request:
   “Create the provisional WACC bridge in one new worksheet. Preserve the
   original sheets.”

Claude documents enabled Skills in its Excel workflow. That platform capability
does not establish that this particular skill's Python helpers have run in the
add-in: check the helper results as part of the first-use review. See
[Claude for Excel](https://claude.com/docs/office-agents/excel).

## 5. Start your first review

Attach a workbook you are authorised to use, or paste the calculation and its
sources. Include the valuation date, company or asset, cash-flow currency,
purpose, and any preferred methodology or source rules you already use.

```text
Use WACC Builder and Validator to review this existing calculation.
The valuation date is 31 January 2025 and the cash flows are nominal,
post-tax EUR FCFF. This is a review of the supplied evidence pack:
do not fetch replacement market inputs. Reconstruct the calculation,
show the calculated, selected, and applied rates, and identify the
most important gaps. Do not edit the workbook.
```

When sufficient inputs exist, expect a concise summary, one coded rate bridge,
up to three priority findings, and the four walkthrough sections. When material
inputs are missing, expect an evidence request rather than invented inputs.

Continue with:

- **Section 1** — build the rate;
- **Section 2** — validate the existing calculation against the bundled SOP;
- **Section 3** — test application, sensitivity, and valuation impact;
- **Section 4** — produce the concise reporting output.

You can interrupt with “why,” “show me,” “compare,” “challenge,” or “mark open.”

## 6. Check the installation before relying on it

Ask the assistant to open the bundled calculation-helper contract and identify
all three scripts. If execution is available, have it run each script with
`--help` and state explicitly if any helper could not run.

Next, test your own workbook: check one input citation, one formula citation,
and the actual applied-rate cell yourself. Successful helper execution confirms
the local setup; it does not verify every formula in a real workbook.

## 7. Troubleshooting and updates

| Problem | Next step |
| --- | --- |
| Skill not visible | Check folder nesting, enabled state, and permissions; restart the host if needed |
| Missing supporting reference | Reinstall the complete skill folder |
| No Python execution | Use a host with execution support; unexecuted checks remain unverified |
| Provider unavailable | Supply an authorised export with the needed fields and dates |
| Solver rejects terminal_cash_flow | Use `terminal_cash_flow_next_year`; see the helper reference |
| Solver rejects mixed signs | Leave the implied-rate check unresolved or use a separately validated method |
| Agent gives only a formula | Explicitly invoke the installed skill and ask for its opening bridge and walkthrough |

To update an installation, replace it with one complete version of the skill
folder. Do not mix scripts from one version with references from another.
