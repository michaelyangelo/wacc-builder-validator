# Install and start your WACC review

Choose one host. Local Codex installation and Claude skill upload are the
available routes described here. Fresh end-to-end tests in those hosts are
still pending, so this guide does not claim a personally tested route.

Before starting, download the complete repository using **Code → Download ZIP**
on [GitHub](https://github.com/michaelyangelo/wacc-builder-validator), then
extract it. Rename the folder that directly contains `SKILL.md` (commonly
`wacc-builder-validator-main`) to `wacc-builder-validator`; do the same for
another branch suffix. Do not leave it double-nested after extracting. Keep
`SKILL.md`, `agents/`, `references/`, `scripts/`, and
`LICENSE-APACHE` together.

## Codex: install into a project folder

1. Open the project folder where you want to use the skill.
2. Create this folder inside it if needed: `.agents/skills`.
3. Copy the complete extracted `wacc-builder-validator` folder into
   `.agents/skills`.
4. Check that this file now exists:
   `your-project/.agents/skills/wacc-builder-validator/SKILL.md`.
5. Open the project in Codex and start a new task. If the skill is not shown,
   restart Codex.
6. Attach the workbook, then send the starter prompt below.

## Claude: upload the complete skill

1. In Claude, open **Customize → Skills**.
2. Select **+ → Create skill → Upload a skill**.
3. Upload a ZIP whose top-level folder is `wacc-builder-validator` and that
   contains `SKILL.md`, `agents/`, `references/`, and `scripts/`.
4. Enable the uploaded skill, start a new conversation, and attach the workbook.
5. Send the starter prompt below.

Your organisation may need to enable Skills or code execution before these
controls appear. See [Claude’s skill instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Starter prompt

```text
Use $wacc-builder-validator to review the WACC in the attached workbook.
Reconstruct the existing calculation. Keep the original workbook unchanged and
show calculated, selected, and applied rates separately.
```

On Claude, use **WACC Builder and Validator** if the host does not support the
`$wacc-builder-validator` form.

### Your first response

When the workbook has enough evidence, expect a compact rate summary, one rate
bridge, up to three priority findings, and the next review sections. If a key
input or workbook reference is missing, expect a request for that evidence.

## Optional: Excel routes

Claude for Excel may be useful when the same account has the skill enabled and
the add-in can access the workbook. Ask it to cite the exact input, formula,
and applied-rate cells before relying on the result. Its ability to run this
skill’s bundled Python helpers has not been verified.

There is no ready-to-import Microsoft 365 Copilot agent in this repository.
The repository ZIP is not a Copilot installer.

## Troubleshooting

<details>
<summary>The skill is not visible</summary>

Check the folder nesting or enabled state, then restart the host if needed.
For Codex, the `SKILL.md` path must match the path shown above.
</details>

<details>
<summary>A reference or helper is missing</summary>

Reinstall the complete folder or ZIP. Do not install `SKILL.md` on its own.
</details>

<details>
<summary>The host cannot execute Python</summary>

The deterministic helpers remain unverified in that host. Use a host with
Python execution support, or ask for an evidence-backed review without claiming
the helpers ran.
</details>

<details>
<summary>How do I check the installation?</summary>

Ask the assistant to open `references/calculation-helpers.md`, identify the
three bundled scripts, and run each with `--help` if execution is available.
Then check one cited input, formula, and applied-rate cell in your own workbook.
</details>

For a fuller review, include the valuation date, company or asset, cash-flow
currency, purpose, and any source rules you already use. The skill uses only
authorised evidence; supply an authorised export when a needed provider is not
available.
