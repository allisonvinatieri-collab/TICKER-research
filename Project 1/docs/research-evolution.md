# Project 1 — Edition B Research Evolution

Edition A is preserved unchanged in `Project1_EditionA_ANF.md`. This document is the post-checkpoint update and should be combined with the unchanged Edition A in `Research-Evolution.pdf`.

| Changed item | Edition A | Edition B | Primary driver of change | Evidence or test |
|---|---|---|---|---|
| Recommendation | Watch/defer | Watch/defer; now supported by a reconciled FCFF range and explicit triggers | Own analysis, course instruction, AI-assisted code review | Growth remains uneven by brand; the final FCFF DCF still requires assumptions about growth breadth and margin recovery. |
| Valuation architecture | Initial bridge and research plan; no final operating forecast | One linked five-year ANF three-statement/FCFF engine | Own analysis, course instruction, AI-assisted implementation support | `anf_project1.py` ties annual cash flow to cash, balances each year, and reports the EV-to-equity bridge. |
| Per-share convention | FY2025 diluted weighted-average shares of 48.476m | 44.864m diluted shares for the September 9, 2026 valuation-date analysis | Source update and own reconciliation | Q2 FY2026 10-Q share evidence in `ANF_reverseDCF_9-10-2026.md`; final model uses one stated basis. |
| Cash bridge | Cash and debt identified, but no final excess-cash policy | $284.576m valuation-date excess cash; no projected cash added to EV | Own analysis, AI-output check | Cash + marketable securities − $500m operating-cash floor. Adding Year-5 cash would double count forecast FCFF. |
| Risk/limitation | Balanced growth and margin durability were uncertain | Same core risk, now quantified by a revenue downside and reverse DCF | Own analysis | Downside revenue path reduces final value from $183.18 to $173.14; market price implies a -6.62 percentage-point uniform revenue-growth shift. |

## Assumption-challenge record

| Load-bearing driver | Value / basis | Challenge | Evidence that would change it |
|---|---|---|---|
| Revenue growth | 5%, 4%, 3%, 3%, 3%; FY2025 reported sales growth was 6% but comparable sales were 3% | Growth was concentrated in Hollister while Abercrombie declined | Brand-level comparable sales: lower the path if Abercrombie remains negative or Hollister slows materially. |
| Gross margin | 61.0% rising to 62.0%; partial recovery from tariff and mix pressure | Recovery may not occur if tariff, product, or channel pressure persists | Quarterly gross-margin and management tariff/mix commentary. |
| WACC / terminal growth | 9.0% / 2.5% | DCF terminal value is 75.1% of EV | Range of 8–10% WACC and 2–3% terminal growth; reassess macro/sector risk. |
| Excess cash | $284.576m; cash plus securities less $500m operating floor | The operating-cash floor is judgmental | Cash needs, working-capital volatility, and capital-return policy. |
| Lease treatment | Operating leases remain operating | Capitalizing leases without adjusting EBIT would be inconsistent | Rebuild both EBIT and bridge if a debt-like lease convention is adopted. |

## AI output check

An AI-assisted review identified that the development pro-forma added Year-5 cash to enterprise value. The output was **corrected**, not accepted: final FCFF valuation adds valuation-date excess cash only. The independent finance check and exact before/after record appear in `docs/validation-and-ai-use.md`.

## What changed from Edition A to Edition B, and why?

The recommendation did not materially change: ANF remains watch/defer. The analysis changed materially because the initial research plan became a linked FCFF model with a consistent valuation-date share basis and excess-cash bridge. The evidence supports potential value above the saved price, but not sufficient confidence that the forecast's growth and margin conditions will occur. An ANF-specific peer cross-check remains required before final submission.
