# Validation and AI-use record — ANF Project 1

This working record must match the frozen `Validation-and-AI-Use.pdf` submitted to Brightspace. It is not complete until the student verifies the bracketed items below.

## Validation results

| Check | Result | Evidence |
|---|---|---|
| Synthetic/known-answer bridge | Pass | `Project1_EditionA_ANF.md` reconciles the course synthetic EV-to-equity bridge to $820.0m equity value and $8.20/share. |
| Independent source/definition check | Pass | FY2025 Form 10-K identifies $759.540m cash and no interest-bearing borrowings; see `Project1_EditionA_ANF.md` and `sources.md`. |
| Base-year balance-sheet reconciliation | Pass | `anf_project1.py` asserts opening assets less liabilities less equity is within $0.01m. |
| Forecast articulation | Pass | `anf_project1.py` reports annual balance-sheet gaps and cash-flow ties of $0.000m. |
| DCF monotonicity | Pass | Script asserts 8% WACC value > 9% > 10%, and 2% terminal-growth value < 2.5% < 3%. |
| Enterprise-to-equity bridge | Pass | The script adds valuation-date excess cash of $284.576m and subtracts $0 interest-bearing debt; it does not add Year-5 cash. |
| Changed-input test | Pass | `lab11_ANF_sensitivity.py` reports lower revenue-growth and gross-margin paths reduce EBIT, FCFF, and value/share; restored-base test passes. |
| Highest-risk test / cold run | Pass on 2026-10-15 | `python anf_project1.py` ran from the project root with Python 3 and no dependencies. **Student must perform and date one fresh-environment cold run while recording Video 2.** |
| Peer-policy/definition consistency | Pass | `docs/peer-policy.md` defines a two-peer set and identical GAAP EV/EBIT and P/E conventions; `python peer_valuation.py` reproduces the table. |

## Locked Changed-Input Record

The human-authored prediction and pre-run timestamp appear in `lab11_ANF_sensitivity_record.md`:

- Locked timestamp: 2026-09-29T14:00:31-04:00.
- Input: revenue-growth path, base 5%, 4%, 3%, 3%, 3% to downside 3%, 2%, 1%, 1%, 1% (percent of prior-year revenue).
- Predicted direction: lower revenue, EBIT, FCFF, and value/share; no initiation expected.
- Actual result: in the final engine, Year-5 EBIT fell from $896.10m to $812.88m; FCFF fell from $580.99m to $543.41m; value/share fell from $183.18 to $173.14. `python anf_sensitivity.py` reproduces this result.
- Diagnosis: direction passed. The original development output used an inconsistent projected-cash bridge and 48.476m share basis; the final result uses valuation-date excess cash and 44.864m diluted shares.
- Decision effect: the scenario reinforces watch/defer because ANF's valuation and operating case weaken when growth fails to broaden.

## AI-use disclosure and checked output

| Item | Record |
|---|---|
| Tool | ChatGPT/Codex, used after the Edition A checkpoint. |
| Use | Code review, model consolidation, document drafting, and research-organization assistance. |
| AI output checked | The prior pro-forma bridge added projected Year-5 cash to enterprise value. |
| Independent check | FCFF discounts operating cash generation; adding future accumulated cash to EV separately double counts it. The final script therefore uses valuation-date excess cash only. |
| Disposition | **Corrected.** The reconciled base value is $183.18/share, versus the former $233.01/share development output. |
| Student ownership | **[Student must confirm:]** I verified all reported finance facts against the cited filings and own the assumptions, recommendation, and final submission. |

## Final student checks

- [ ] Confirm the Edition A Brightspace receipt and preserve Edition A unchanged.
- [ ] Independently re-open the cited peer filings and confirm each entered value before freezing the record.
- [ ] Run the finalized changed-input test with `anf_project1.py` if the final sensitivity numbers will be quoted.
- [ ] Record the clean cold run and complete the dated cold-run log.
- [ ] Replace bracketed text; export this exact record to PDF at submission.
