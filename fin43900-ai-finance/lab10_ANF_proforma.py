"""Five-year three-statement model and DCF for Abercrombie & Fitch (ANF).

All figures are USD millions unless stated otherwise.  Opening balances are
January 31, 2026 (FY2025 Form 10-K).  The model is deliberately small and
transparent for course use; edit the INPUTS section to test assumptions.
"""

# ---------------------------------------------------------------------------
# INPUTS
# ---------------------------------------------------------------------------
REVENUE_GROWTH = [0.05, 0.04, 0.03, 0.03, 0.03]
GROSS_MARGIN = [0.61, 0.615, 0.62, 0.62, 0.62]
SGA_TO_GROSS_PROFIT = [0.78, 0.775, 0.77, 0.77, 0.77]
INVENTORY_DAYS = [106, 106, 106, 106, 106]
DEPRECIATION_TO_PPE = [0.23, 0.23, 0.23, 0.23, 0.23]
CAPEX_TO_REVENUE = [0.045, 0.045, 0.045, 0.045, 0.045]
TAX_RATE = [0.28, 0.28, 0.28, 0.28, 0.28]

# Peer-review record
# Partner attack: Why start revenue growth at 5% when FY2025 comparable sales
# were only 3%, and what would change that assumption?
# Answer: I used 5% because FY2025 reported sales grew 6%, while planned store,
# digital, and partnership expansion can add growth above comparable sales. I
# would lower it to 3% if comparable sales remain flat or negative, or if tariff
# pressure prevents new stores and channels from adding enough incremental sales.
#
# My attack on my Apple partner: How does your terminal-growth assumption avoid
# treating installed-base and Services growth as permanent, and what evidence
# would make you reduce it?
# Partner answer: [Paste your partner's two-sentence response here.]

WACC = 0.09
TERMINAL_GROWTH = 0.025
MINIMUM_CASH = 500.000
DILUTED_SHARES = 48.476

# FY2025 income-statement base
BASE_REVENUE = 5_266.292

# Opening balance sheet, January 31, 2026
opening = {
    "cash": 759.540,
    "marketable_securities": 25.036,
    "receivables": 146.757,
    "inventory": 601.218,
    "other_current_assets": 117.913,
    "ppe": 674.079,
    "lease_rou_assets": 997.399,
    "other_assets": 219.932,
    "accounts_payable": 377.465,
    "accrued_expenses": 465.549,
    "income_taxes_payable": 21.721,
    "current_lease_liabilities": 241.265,
    "long_term_lease_liabilities": 926.830,
    "other_liabilities": 88.633,
    "equity": 1_420.411,
    "debt": 0.000,
}


def ratio(numerator, denominator):
    return numerator / denominator


# Working-capital and other balance-sheet links based on FY2025 ending values.
RECEIVABLES_TO_REVENUE = ratio(opening["receivables"], BASE_REVENUE)
OTHER_CA_TO_REVENUE = ratio(opening["other_current_assets"], BASE_REVENUE)
OTHER_ASSETS_TO_REVENUE = ratio(opening["other_assets"], BASE_REVENUE)
AP_TO_COGS = ratio(opening["accounts_payable"], BASE_REVENUE * (1 - 0.6147))
ACCRUED_TO_REVENUE = ratio(opening["accrued_expenses"], BASE_REVENUE)
TAX_PAYABLE_TO_TAX = ratio(opening["income_taxes_payable"], BASE_REVENUE * 0.6147 * 0.78 * 0.28)


def total_assets(state):
    return sum(state[key] for key in (
        "cash", "marketable_securities", "receivables", "inventory",
        "other_current_assets", "ppe", "lease_rou_assets", "other_assets"
    ))


def total_liabilities(state):
    return sum(state[key] for key in (
        "accounts_payable", "accrued_expenses", "income_taxes_payable",
        "current_lease_liabilities", "long_term_lease_liabilities",
        "other_liabilities", "debt"
    ))


def run_model():
    if TERMINAL_GROWTH >= WACC:
        raise ValueError("Terminal growth must be below WACC.")

    prior = opening.copy()
    revenue = BASE_REVENUE
    forecast = []
    unlevered_fcfs = []

    for year in range(5):
        revenue *= 1 + REVENUE_GROWTH[year]
        gross_profit = revenue * GROSS_MARGIN[year]
        cogs = revenue - gross_profit
        total_sga = gross_profit * SGA_TO_GROSS_PROFIT[year]
        depreciation = prior["ppe"] * DEPRECIATION_TO_PPE[year]
        cash_sga = total_sga - depreciation
        ebit = gross_profit - total_sga
        taxes = max(0.0, ebit * TAX_RATE[year])
        net_income = ebit - taxes
        capex = revenue * CAPEX_TO_REVENUE[year]

        current = prior.copy()
        current["receivables"] = revenue * RECEIVABLES_TO_REVENUE
        current["inventory"] = cogs * INVENTORY_DAYS[year] / 365
        current["other_current_assets"] = revenue * OTHER_CA_TO_REVENUE
        current["ppe"] = prior["ppe"] + capex - depreciation
        current["other_assets"] = revenue * OTHER_ASSETS_TO_REVENUE
        current["accounts_payable"] = cogs * AP_TO_COGS
        current["accrued_expenses"] = revenue * ACCRUED_TO_REVENUE
        current["income_taxes_payable"] = taxes * TAX_PAYABLE_TO_TAX

        change_nwc = (
            (current["receivables"] - prior["receivables"])
            + (current["inventory"] - prior["inventory"])
            + (current["other_current_assets"] - prior["other_current_assets"])
            + (current["other_assets"] - prior["other_assets"])
            - (current["accounts_payable"] - prior["accounts_payable"])
            - (current["accrued_expenses"] - prior["accrued_expenses"])
            - (current["income_taxes_payable"] - prior["income_taxes_payable"])
        )
        operating_cash_flow = net_income + depreciation - change_nwc
        free_cash_flow = operating_cash_flow - capex

        # No forecast repurchases or dividends: retained earnings increase by NI.
        current["equity"] = prior["equity"] + net_income
        current["cash"] = prior["cash"] + free_cash_flow

        # If cash would breach the floor, a revolver draw supplies only the gap.
        revolver_draw = max(0.0, MINIMUM_CASH - current["cash"])
        current["cash"] += revolver_draw
        current["debt"] = prior["debt"] + revolver_draw

        balance_check = total_assets(current) - total_liabilities(current) - current["equity"]
        unlevered_fcf = ebit * (1 - TAX_RATE[year]) + depreciation - capex - change_nwc
        unlevered_fcfs.append(unlevered_fcf)
        forecast.append({
            "year": year + 1, "revenue": revenue, "gross_profit": gross_profit,
            "cash_sga": cash_sga, "depreciation": depreciation, "ebit": ebit,
            "taxes": taxes, "net_income": net_income, "capex": capex,
            "operating_cash_flow": operating_cash_flow, "free_cash_flow": free_cash_flow,
            "unlevered_fcf": unlevered_fcf, "cash": current["cash"],
            "debt": current["debt"], "equity": current["equity"],
            "balance_check": balance_check, "revolver_draw": revolver_draw,
        })
        prior = current

    pv_explicit = sum(fcf / (1 + WACC) ** (i + 1) for i, fcf in enumerate(unlevered_fcfs))
    terminal_value = unlevered_fcfs[-1] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    pv_terminal = terminal_value / (1 + WACC) ** 5
    enterprise_value = pv_explicit + pv_terminal
    equity_value = enterprise_value + prior["cash"] + prior["marketable_securities"] - prior["debt"]
    value_per_share = equity_value / DILUTED_SHARES
    return forecast, {
        "pv_explicit": pv_explicit,
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_share": value_per_share,
    }


def main():
    forecast, valuation = run_model()
    print("ANF Five-Year Three-Statement Model (USD millions)")
    print("Year   Revenue     EBIT       Net income Capex      Ending cash  Balance check")
    for row in forecast:
        print(
            f"{row['year']:>4}  {row['revenue']:>10.2f}  {row['ebit']:>10.2f}  "
            f"{row['net_income']:>10.2f}  {row['capex']:>9.2f}  {row['cash']:>11.2f}  "
            f"{row['balance_check']:>13.6f}"
        )
    print("\nCheck block")
    for row in forecast:
        status = "OK" if abs(row["balance_check"]) < 0.01 and row["cash"] >= MINIMUM_CASH else "FAIL"
        draw_note = f"; revolver draw {row['revolver_draw']:.2f}" if row["revolver_draw"] else ""
        print(f"Year {row['year']}: {status}{draw_note}")
    print("\nDCF valuation")
    print(f"PV of explicit FCFF: {valuation['pv_explicit']:.2f}")
    print(f"PV of terminal value: {valuation['pv_terminal']:.2f}")
    print(f"Enterprise value: {valuation['enterprise_value']:.2f}")
    print(f"Equity value: {valuation['equity_value']:.2f}")
    print(f"Value per diluted share: ${valuation['value_per_share']:.2f}")


if __name__ == "__main__":
    main()
