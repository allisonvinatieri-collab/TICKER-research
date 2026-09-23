"""Five-year ABG pro forma and equity valuation (USD millions)."""

YEARS = [2026, 2027, 2028, 2029, 2030]

ASSUMPTIONS = {
    "growth": 0.018,
    "gross_margin": 0.1705,
    "sga_ratios": [0.665, 0.655, 0.645, 0.645, 0.645],
    "depreciation_rate": 82.4 / 3070.4,
    "impairment": 120.0,
    "capex": 250.0,
    "tax_rate": 0.255,
    "inventory_days": 2135.8 / (17999.0 - 3071.7) * 365,
    "floor_plan_ratio": 2027.0 / 2135.8,
    "other_wc_rate": 0.008,
    "minimum_cash": 25.0,
    "revolver_limit": 850.0,
    "revolver_rate": 0.06,
    "debt_repayment": 150.0,
    "buyback": 150.0,
    "floor_plan_rate": 0.0467,
    "term_debt_rate": 0.0544,
    "cost_of_equity": 0.10,
    "terminal_growth": 0.025,
    "shares": 17.951349,
}

OPENING = {
    "revenue": 17999.0, "inventory": 2135.8, "ppe": 3070.4,
    "other_assets": 6371.6, "cash": 40.4, "floor_plan": 2027.0,
    "debt": 3572.0, "revolver": 0.0, "other_liabilities": 2127.5,
    "equity": 3891.7,
}


def assert_balanced(year, gap, cash, minimum_cash):
    """Reject a projected balance sheet that does not balance or lacks minimum cash."""
    if abs(gap) > 0.05:
        raise AssertionError(f"FY{year}E is not balanced: gap {gap:.1f}")
    if cash < minimum_cash - 0.05:
        raise AssertionError(f"FY{year}E cash {cash:.1f} is below minimum {minimum_cash:.1f}")


def print_table(title, rows):
    print(f"\n{title}")
    print(f"{'USD millions':<28}" + "".join(f"FY{year}E{'':>7}" for year in YEARS))
    for label, key in rows:
        print(f"{label:<28}" + "".join(f"{model[year][key]:>12.1f}" for year in YEARS))


model = {}
opening = OPENING.copy()

for index, year in enumerate(YEARS):
    a = ASSUMPTIONS
    revenue = opening["revenue"] * (1 + a["growth"])
    gross_profit = revenue * a["gross_margin"]
    sga = gross_profit * a["sga_ratios"][index]
    depreciation = opening["ppe"] * a["depreciation_rate"]
    impairment = a["impairment"]
    operating_income = gross_profit - sga - depreciation - impairment
    interest = (opening["floor_plan"] * a["floor_plan_rate"]
                + opening["debt"] * a["term_debt_rate"]
                + opening["revolver"] * a["revolver_rate"])
    pretax_income = operating_income - interest
    tax = max(0.0, pretax_income) * a["tax_rate"]
    net_income = pretax_income - tax

    inventory = (revenue - gross_profit) * a["inventory_days"] / 365
    floor_plan = inventory * a["floor_plan_ratio"]
    ppe = opening["ppe"] + a["capex"] - depreciation
    change_revenue = revenue - opening["revenue"]
    other_wc = a["other_wc_rate"] * change_revenue
    other_assets = opening["other_assets"] + other_wc - impairment
    debt = opening["debt"] - a["debt_repayment"]
    other_liabilities = opening["other_liabilities"]
    equity = opening["equity"] + net_income - a["buyback"]

    fcfe = (net_income + depreciation + impairment - a["capex"]
            - (inventory - opening["inventory"]) - other_wc
            + (floor_plan - opening["floor_plan"]) - a["debt_repayment"])
    cash_before_revolver = opening["cash"] + fcfe - a["buyback"]
    revolver = opening["revolver"]
    if cash_before_revolver < a["minimum_cash"]:
        draw = min(a["minimum_cash"] - cash_before_revolver,
                   a["revolver_limit"] - revolver)
        revolver += draw
        cash = cash_before_revolver + draw
    else:
        repayment = min(revolver, cash_before_revolver - a["minimum_cash"])
        revolver -= repayment
        cash = cash_before_revolver - repayment

    assets = inventory + ppe + other_assets + cash
    liabilities_and_equity = floor_plan + debt + revolver + other_liabilities + equity
    gap = assets - liabilities_and_equity
    model[year] = locals().copy()
    opening = {key: model[year][key] for key in OPENING}

print_table("Income Statement", [
    ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
    ("Depreciation", "depreciation"), ("Impairment", "impairment"),
    ("Operating income", "operating_income"), ("Interest", "interest"),
    ("Tax", "tax"), ("Net income", "net_income"),
])
print_table("Balance Sheet", [
    ("Inventory", "inventory"), ("PP&E", "ppe"), ("Other assets", "other_assets"),
    ("Cash", "cash"), ("Floor plan", "floor_plan"), ("Term debt", "debt"),
    ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
])
print_table("Cash Flow", [("Free cash flow to equity", "fcfe")])

print("\nChecks")
for year in YEARS:
    row = model[year]
    print(f"FY{year}E  assets - liabilities - equity: {row['gap']:.1f}; "
          f"cash at or above minimum: {row['cash'] >= ASSUMPTIONS['minimum_cash']}")
    assert_balanced(year, row["gap"], row["cash"], ASSUMPTIONS["minimum_cash"])

discount_rate = ASSUMPTIONS["cost_of_equity"]
pv_fcfe = sum(model[year]["fcfe"] / (1 + discount_rate) ** (index + 1)
              for index, year in enumerate(YEARS))
terminal_fcfe = model[2030]["fcfe"] + ASSUMPTIONS["debt_repayment"]
terminal_value = (terminal_fcfe * (1 + ASSUMPTIONS["terminal_growth"])
                  / (discount_rate - ASSUMPTIONS["terminal_growth"]))
pv_terminal = terminal_value / (1 + discount_rate) ** 5
equity_value = pv_fcfe + pv_terminal

print("\nValuation")
print(f"Equity value: ${equity_value:,.2f} million")
print(f"Share of value after 2030: {pv_terminal / equity_value:.1%}")
print(f"Value per share: ${equity_value / ASSUMPTIONS['shares']:.2f}")
