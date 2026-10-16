# ANF comparable-company policy

## Purpose and date discipline

This is a cross-check, not a mechanical average with the FCFF DCF. Market prices use September 9, 2026 closes. Financial-statement inputs use the latest filing that was public by that date; each peer must state the filing date, reporting period, units, and source.

## Inclusion rules

A peer must be a U.S.-listed, apparel-focused specialty retailer with:

1. meaningful owned consumer brands and store/digital retail operations;
2. a fiscal year-end and financial disclosures that permit an enterprise-value and equity-value multiple on a comparable basis;
3. no pending transaction, financial distress, or accounting discontinuity that makes its market price non-operating; and
4. sufficient data to compute market capitalization, net debt, EV/EBIT, and price/earnings using the same definitions.

## Preliminary roster

| Ticker | Status | Reason |
|---|---|---|
| AEO | Candidate | U.S. specialty apparel retailer with American Eagle and Aerie brands; latest available Form 10-Q was filed September 10, 2026, **after** the September 9 valuation-date close, so use its prior public filing for a strictly contemporaneous set or roll the entire valuation date forward. |
| URBN | Candidate | Multi-brand specialty retailer; its Form 10-Q was filed September 9, 2026. Confirm the filing timestamp and market-information cutoff before using it. |
| GES | Exclude unless separately qualified | Licensing and wholesale exposure make its operating model less comparable to ANF's predominantly owned-brand retail model. |
| Off-price, department-store, luxury, and athleticwear issuers | Exclude | Different merchandise model, customer proposition, margins, inventory economics, or growth drivers. |

## Definitions and calculation rules

- **Equity value:** valuation-date unadjusted closing price × latest basic shares outstanding. If diluted shares are used, use them consistently and disclose the method.
- **Enterprise value:** equity value + interest-bearing debt + preferred equity + noncontrolling interests − cash and short-term investments. Operating lease liabilities remain excluded when EBIT includes operating lease expense.
- **EV/EBIT:** enterprise value divided by the latest completed fiscal-year GAAP EBIT, with no non-GAAP adjustments.
- **P/E:** valuation-date price divided by latest completed fiscal-year GAAP diluted EPS.

## Required peer-data table before final submission

| Ticker | Price / date | Shares / source | Cash | Debt | FY GAAP EBIT | FY GAAP diluted EPS | EV/EBIT | P/E |
|---|---|---|---:|---:|---:|---:|---:|---:|
| ANF | $152.08 / 2026-09-09 | 44.864m diluted; Q2 FY2026 10-Q | 784.576 | 0.000 | 699.140 | $10.46 | 8.64x | 14.54x |
| AEO | $16.89 / 2026-09-09 | 167.573m basic; Q1 FY2026 10-Q filed 2026-06-09 | 103.300 | 85.000 | 226.200 | $1.09 | 12.43x | 15.50x |
| URBN | $77.58 / 2026-09-09 | 85.601m basic; Q1 FY2027 10-Q filed 2026-06-09 | 413.342 | 0.000 | 605.634 | $5.06 | 10.28x | 15.33x |

The peer mean is **11.36x EV/EBIT** and **15.41x P/E**, versus ANF at 8.64x and 14.54x. This is a cross-check only: AEO's lower-margin AE business and URBN's broader brand portfolio differ materially from ANF. The figures are reproduced by `python peer_valuation.py`.

### Data sources

- ANF: FY2025 [Form 10-K](https://www.sec.gov/Archives/edgar/data/1018840/000101884026000012/anf-20260131.htm), filed March 26, 2026 (FY EBIT, EPS, cash); Q2 FY2026 [Form 10-Q](https://www.sec.gov/Archives/edgar/data/1018840/000101884026000047/anf-20260801.htm) (diluted shares).
- AEO: FY2025 [Form 10-K](https://www.sec.gov/Archives/edgar/data/919012/000119312526132097/aeo-20260131.htm), filed March 30, 2026 (FY EBIT and EPS); Q1 FY2026 [Form 10-Q](https://www.sec.gov/Archives/edgar/data/919012/000119312526255712/aeo-20260502.htm), filed June 9, 2026 (cash, credit-facility debt, shares).
- URBN: FY2026 [Form 10-K](https://www.sec.gov/Archives/edgar/data/912615/000119312526137916/urbn-20260131.htm), filed March 31, 2026 (FY EBIT and EPS); Q1 FY2027 [Form 10-Q](https://www.sec.gov/Archives/edgar/data/912615/000119312526263929/urbn-20260430.htm), filed June 9, 2026 (cash, marketable securities, shares, and no interest-bearing debt presented).
- September 9 unadjusted closing prices: [AEO](https://stockanalysis.com/stocks/aeo/history/) and [URBN](https://stockanalysis.com/stocks/urbn/history/). Record the ANF price source already in `ANF_reverseDCF_9-10-2026.md`.

## Interpretation rule

Explain differences in growth breadth, margins, capital structure, and earnings quality. Do not average the DCF and peer outputs. A peer multiple that reflects stronger brand breadth or a different operating model is context, not a price target.
