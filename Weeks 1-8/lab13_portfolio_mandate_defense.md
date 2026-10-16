# Lab 13 — Portfolio Mandate Defense

## Sort before building

| Statement | Type | Reason |
|---|---|---|
| S1 | Hard constraint | Seven-year horizon and annual rebalancing set operating limits. |
| S2 | Objective | CPI + 4% net over rolling five years describes the desired investment result. |
| S3 | Hard constraint | It requires one year of payouts in cash or daily-liquid government securities. |
| S4 | Preference | The benchmark is a comparison point, not an allocation limit. |
| S5 | Hard constraint | It prohibits borrowing, short sales, and derivatives. |
| S6 | Hard constraint | It sets an 8% single-issuer maximum, with stated exemptions. |
| S7 | Hard constraint | It caps annual turnover unless the committee approves more. |
| S8 | Hard constraint | It requires at least 90% to be redeemable within five business days. |
| S9 | Unverifiable promise | It gives neither a loss measurement nor a breach rule. |
| S10 | Missing | It supplies no preference or pilot optimization target. |

## Checker and verification

The checker is [mandate.py](mandate.py). Run it with:

```powershell
python mandate.py
```

It produces the required known-answer values: A passes, B fails three rules, and C fails one rule. The calendar-year loss rule always reads `requires CIO clarification`.

For the required probe, I temporarily changed A to Cash = -2 and Global equity index fund = 64, ran the checker, and restored the inputs. A's lowest weight was -2.0 and failed long-only; its reserve-eligible weight was still 10.0 and all other checkable rules passed.

## Candidate D: attack on the checker

Candidate D is 90% Cash and 10% Global equity index fund. It passes every implemented check, but the CIO could reasonably reject it because it is unlikely to support the CPI + 4% net-of-costs objective (S2) over rolling five-year periods. The objection holds: S2 decides it, but it cannot be tested without an agreed return model, cost assumption, and breach treatment.

Against a partner's candidate D, I would cite the particular statement it conflicts with; for a very conservative all-liquid candidate, I would cite S2.

## Question for the CIO before optimization

Should the pilot optimize expected return, probability of meeting CPI + 4% net over rolling five-year periods, or risk-adjusted return relative to the 60/40 benchmark, and what capital-market assumptions and risk measure should it use? For example, if the answer is probability of meeting S2, I would favor a diversified growth allocation; if it is minimizing shortfall risk, I would hold more high-quality government securities and cash.

## Investment policy statement (IPS)

An IPS is the client-approved document that converts investment goals, circumstances, governance, and limits into a mandate for portfolio decisions and monitoring. Its objective says what success is; its constraints say what is permitted; its benchmark and monitoring rules make review possible.

S1 is horizon/rebalancing governance; S2 is the return objective; S3 is spending and reserve liquidity; S4 is the benchmark; S5 is permitted-investment policy; S6 is diversification; S7 is implementation governance; S8 is liquidity; S9 is risk policy that needs a defined measure and breach process; and S10 records absent preferences and an absent optimization choice.

## Reflection

A portfolio can pass every checkable rule yet still be wrong because the rules do not determine trade-offs, expected return, cost, or a complete risk policy. The type I was least sure of was S1: the horizon is client context, while annual rebalancing is an operating constraint; I classified the combined statement as a hard constraint because the checker/implementation can enforce the rebalancing cadence.
