# Abercrombie & Fitch (ANF) FCFF DCF

| Per-share comparison | Price |
|---|---:|
| DCF value per diluted share | **$193.27** |
| Most recent ANF closing price (September 9, 2026) | **$152.08** |

The DCF value is **1.27×** the market price, which is inside the requested **0.5×–2×** range.

## Conditional call

**Watch-defer.** Initiate if ANF trades below about **$193.27**, because the price would then demand a uniform FCFF-growth shift below this model's forecast path; otherwise defer. **Monitor:** operating margin in the next quarterly report.

## Floor

| Item | Result |
|---|---:|
| Company DCF value per diluted share | $193.2670 |
| Current price used | $152.08 |
| Sensitivity-grid low: 11% WACC / 2% terminal growth | $145.0495 |
| Sensitivity-grid high: 9% WACC / 4% terminal growth | $235.8274 |
| Price-implied uniform FCFF-growth shift | -6.0765 percentage points |

The implied shift makes the five explicit FCFF growth rates approximately 1.92%, 0.92%, -0.08%, -1.08%, and -2.08%. This diagnostic extends the reverse-DCF search below the script's classroom lower bound of -5 percentage points; `python dcf.py` correctly retains and reports no solution in its required bracket.

| Input | Value | Basis | Status |
|---|---:|---|---|
| Starting FCFF ($m) | 436.5819 | TTM EBIT after tax + D&A - capex | Resolved |
| Year 1 growth | 8.0% | DCF assumption | Resolved |
| Year 2 growth | 7.0% | DCF assumption | Resolved |
| Year 3 growth | 6.0% | DCF assumption | Resolved |
| Year 4 growth | 5.0% | DCF assumption | Resolved |
| Year 5 growth | 4.0% | DCF assumption | Resolved |
| WACC | 9.0% | DCF assumption | Resolved |
| Terminal growth | 2.5% | DCF assumption | Resolved |
| Non-operating cash ($m) | 637.999 | Cash plus marketable securities | Resolved |
| Debt ($m) | 0.000 | No interest-bearing debt reported | Resolved |
| Diluted shares (m) | 44.864 | Latest reported diluted weighted-average shares | Resolved |

Sources: [Abercrombie & Fitch Q2 FY2026 Form 10-Q](https://www.sec.gov/Archives/edgar/data/1018840/000101884026000047/anf-20260801.htm) (cash, shares, and interim operating data); [FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1018840/000101884026000012/anf-20260131.htm) (annual operating data and capex); [ANF price history](https://www.investing.com/equities/aberc-fitch-a-historical-data) (September 9, 2026 close). Model inputs are assumptions unless a source is named.
