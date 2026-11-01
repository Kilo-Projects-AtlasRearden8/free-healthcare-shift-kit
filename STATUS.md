# STATUS

## What was built

Free Healthcare Shift Kit — a free printables kit (Markdown + static HTML site) for healthcare workers: brain sheets, shift handover templates, CE (continuing education) trackers, and medication logs. Education only, printable, no account needed. Credit: Asdale Dynamics, LLC (Indiana, formed October 2026). MIT License.

Deliverables (Markdown + printable HTML for each sheet):

| Sheet | HTML | Markdown |
|---|---|---|
| Brain sheet | `brain-sheet.html` | `brain-sheet.md` |
| Shift handover template | `handover-template.html` | `handover-template.md` |
| CE tracker | `ce-tracker.html` | `ce-tracker.md` |
| Medication log | `medication-log.html` | `medication-log.md` |

Supporting files:
- `index.html` — static HTML landing page listing all sheets with how-to-use instructions
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`
- `README.md` — contents, how to use, credit to Asdale Dynamics, LLC, license
- `.gitignore` — OS/editor junk only
- `tests/validate.py` — static validation (HTML tag balance, required markers, secrets scan, copyright/credit checks)

Style: clear, warm, polished, tested, local-first, no secrets or personal data. Each sheet has an education-only disclaimer, print CSS that hides on-screen controls, and an Asdale Dynamics, LLC credit footer.

## How to run

No build step, no install, no account needed.

1. Open `index.html` (or any sheet `.html` file) directly in a browser (Chrome, Edge, Safari, Firefox).
2. Fill in the fields in the browser.
3. Print with `Ctrl+P` / `Cmd+P`. Print styles hide the "Print this sheet" button and on-screen controls, producing a clean worksheet.
4. Markdown (`.md`) versions can be read/printed from any markdown viewer or copied into your own notes.

Nothing is saved server-side; data lives only in the browser until printed.

## Verification results

- File inventory: 5 HTML + 4 Markdown + LICENSE + README + .gitignore + tests/validate.py
- HTML structure: all 5 `.html` files parse with balanced tags (Python HTMLParser); each has `<!DOCTYPE html>` in the first 200 bytes
- Required markers present on every sheet: `Asdale Dynamics, LLC`, `Education only`, `@media print`, `no-print` (index.html is a landing page, exempt from `no-print`)
- Secrets/scan: grep for `api key|secret key|password|access token|private key|sk_live|sk_test` across all files (excluding `tests/validate.py` itself and LICENSE) — no matches (no secrets, API keys, or personal data)
- Copyright line: `LICENSE` line 3 exactly `Copyright (c) 2026 Asdale Dynamics, LLC`
- Asdale credit: present in `README.md` and in the credit footer of every HTML and Markdown sheet
- Education-only disclaimer: present at the top of every sheet
- `.github/workflows`: not present (none created)
- Validation command: `python3 tests/validate.py` — all checks passed (0 failures)

## Known gaps

- Sheets are single-page-optimized; long CE logs or medication lists may flow to a second page when printed.
- No automated test suite beyond `tests/validate.py` and no CI (none requested; `.github/workflows` explicitly avoided).
- No account/login/sync — data lives only in the browser until printed; nothing is saved server-side.
- Not tested in every browser; print CSS uses standard `@media print` with `-webkit-print-color-adjust` / `print-color-adjust` for broad compatibility.
