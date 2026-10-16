# ANF executed valuation output

Command run: `python anf_project1.py`  
Units: USD millions except per-share data. Valuation date: September 9, 2026.

| Year | Revenue | EBIT | FCFF | Ending cash | Balance-sheet gap | Cash-flow tie |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5,529.61 | 742.07 | 422.85 | 1,182.39 | 0.000 | 0.000 |
| 2 | 5,750.79 | 795.77 | 484.44 | 1,666.82 | 0.000 | 0.000 |
| 3 | 5,923.31 | 844.66 | 533.07 | 2,199.90 | 0.000 | 0.000 |
| 4 | 6,101.01 | 870.00 | 556.23 | 2,756.13 | 0.000 | 0.000 |
| 5 | 6,284.04 | 896.10 | 580.99 | 3,337.12 | 0.000 | 0.000 |

| Enterprise-to-equity bridge | Amount |
|---|---:|
| PV of explicit FCFF | 1,978.96 |
| PV of terminal value | 5,954.47 |
| Enterprise value | 7,933.43 |
| Add: valuation-date excess cash | 284.58 |
| Less: interest-bearing debt | 0.00 |
| Equity value | 8,218.01 |
| Diluted shares (millions) | 44.864 |
| **Value per diluted share** | **$183.18** |

Terminal value is 75.1% of enterprise value. Automated checks passed: FY2025 base-year balance-sheet reconciliation, annual balance sheets, cash-flow ties, and expected DCF directions when WACC or terminal growth changes.

| WACC / terminal growth | 2.0% | 2.5% | 3.0% |
|---|---:|---:|---:|
| 8.0% | $201.52 | $215.94 | $233.24 |
| 9.0% | $173.09 | $183.18 | $194.94 |
| 10.0% | $151.79 | $159.16 | $167.59 |

At the September 9, 2026 price of $152.08, the reverse DCF requires a **-6.62 percentage-point** uniform reduction to the five forecast revenue-growth rates, holding other assumptions fixed.
