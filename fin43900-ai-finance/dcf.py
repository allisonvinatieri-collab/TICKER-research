"""Five-year FCFF discounted cash flow model (USD millions)."""

# Editable inputs
STARTING_FCFF = 436.5819
GROWTH_RATES = [0.08, 0.07, 0.06, 0.05, 0.04]
WACC = 0.09
TERMINAL_GROWTH = 0.025
NON_OPERATING_CASH = 637.999
DEBT = 0.0
DILUTED_SHARES = 44.864

# Sensitivity and reverse-DCF inputs
SENSITIVITY_WACCS = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTHS = [0.02, 0.03, 0.04]
TARGET_SHARE_PRICE = 152.08
REVERSE_SHIFT_LOWER_BOUND = -0.05
REVERSE_SHIFT_UPPER_BOUND = 0.10


def calculate_valuation(wacc=None, terminal_growth=None, growth_rates=None):
    """Return FCFF values and valuation results in USD millions."""
    if wacc is None:
        wacc = WACC
    if terminal_growth is None:
        terminal_growth = TERMINAL_GROWTH
    if growth_rates is None:
        growth_rates = GROWTH_RATES
    fcff_values = []
    fcff = STARTING_FCFF
    for growth_rate in growth_rates:
        fcff *= 1.0 + growth_rate
        fcff_values.append(fcff)

    present_value_explicit_fcff = sum(
        fcff / (1.0 + wacc) ** year
        for year, fcff in enumerate(fcff_values, start=1)
    )
    terminal_value_year_5 = (
        fcff_values[-1] * (1.0 + terminal_growth) / (wacc - terminal_growth)
    )
    present_value_terminal_value = terminal_value_year_5 / (1.0 + wacc) ** 5
    enterprise_value = present_value_explicit_fcff + present_value_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_diluted_share = equity_value / DILUTED_SHARES
    terminal_value_share_of_enterprise_value = (
        present_value_terminal_value / enterprise_value
    )
    return {
        "fcff_values": fcff_values,
        "present_value_explicit_fcff": present_value_explicit_fcff,
        "terminal_value_year_5": terminal_value_year_5,
        "present_value_terminal_value": present_value_terminal_value,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_diluted_share": value_per_diluted_share,
        "terminal_value_share_of_enterprise_value": (
            terminal_value_share_of_enterprise_value
        ),
    }


def print_sensitivity_grid():
    print("Sensitivity Grid: Value per Diluted Share")
    header = "WACC \\ Terminal Growth".ljust(24)
    header += "".join(f"{growth:>12.2%}" for growth in SENSITIVITY_TERMINAL_GROWTHS)
    print(header)

    for wacc in SENSITIVITY_WACCS:
        row = f"{wacc:.2%}".ljust(24)
        for terminal_growth in SENSITIVITY_TERMINAL_GROWTHS:
            if terminal_growth >= wacc:
                row += f"{'invalid':>12}"
            else:
                value = calculate_valuation(wacc, terminal_growth)[
                    "value_per_diluted_share"
                ]
                row += f"{value:>12.4f}"
        print(row)


def solve_uniform_growth_shift():
    """Solve for the uniform shift to all explicit growth rates by bisection."""
    lower = REVERSE_SHIFT_LOWER_BOUND
    upper = REVERSE_SHIFT_UPPER_BOUND

    if any(growth + lower <= -1.0 for growth in GROWTH_RATES):
        return None, "no solution: lower bound makes an annual growth rate <= -100%."
    if any(growth + upper <= -1.0 for growth in GROWTH_RATES):
        return None, "no solution: upper bound makes an annual growth rate <= -100%."

    def price_for_shift(shift):
        shifted_growth_rates = [growth + shift for growth in GROWTH_RATES]
        return calculate_valuation(growth_rates=shifted_growth_rates)[
            "value_per_diluted_share"
        ]

    lower_price = price_for_shift(lower)
    upper_price = price_for_shift(upper)
    target_is_bracketed = min(lower_price, upper_price) <= TARGET_SHARE_PRICE <= max(
        lower_price, upper_price
    )
    if not target_is_bracketed:
        return None, "no solution in this bracket."

    for _ in range(100):
        midpoint = (lower + upper) / 2.0
        midpoint_price = price_for_shift(midpoint)
        if midpoint_price < TARGET_SHARE_PRICE:
            lower = midpoint
        else:
            upper = midpoint

    return (lower + upper) / 2.0, None


def print_reverse_dcf():
    print("Reverse DCF: Uniform Shift to All Five Explicit Growth Rates")
    shift, error = solve_uniform_growth_shift()
    if error:
        print(f"Reverse DCF Result: {error}")
    else:
        print(f"Solved Growth Shift: {shift:.4%} ({shift * 100:.4f} percentage points)")
    print(f"Target Share Price: {TARGET_SHARE_PRICE:.4f}")
    print(
        "Held Fixed: "
        f"starting FCFF={STARTING_FCFF:.4f}; WACC={WACC:.2%}; "
        f"terminal growth={TERMINAL_GROWTH:.2%}; cash={NON_OPERATING_CASH:.4f}; "
        f"debt={DEBT:.4f}; diluted shares={DILUTED_SHARES:.4f}; "
        f"base growth rates={GROWTH_RATES}"
    )


def main():
    if TERMINAL_GROWTH >= WACC:
        print("Error: terminal growth must be less than WACC.")
        return

    if len(GROWTH_RATES) != 5:
        print("Error: provide exactly five yearly growth rates.")
        return

    valuation = calculate_valuation()
    fcff_values = valuation["fcff_values"]
    present_value_explicit_fcff = valuation["present_value_explicit_fcff"]
    terminal_value_year_5 = valuation["terminal_value_year_5"]
    present_value_terminal_value = valuation["present_value_terminal_value"]
    enterprise_value = valuation["enterprise_value"]
    equity_value = valuation["equity_value"]
    value_per_diluted_share = valuation["value_per_diluted_share"]
    terminal_value_share_of_enterprise_value = valuation[
        "terminal_value_share_of_enterprise_value"
    ]

    for year, fcff in enumerate(fcff_values, start=1):
        print(f"FCFF Year {year}: {fcff:.4f}")
    print(f"PV of Explicit FCFF: {present_value_explicit_fcff:.4f}")
    print(f"Terminal Value at Year 5: {terminal_value_year_5:.4f}")
    print(f"PV of Terminal Value: {present_value_terminal_value:.4f}")
    print(f"Enterprise Value: {enterprise_value:.4f}")
    print(f"Equity Value: {equity_value:.4f}")
    print(f"Value per Diluted Share: {value_per_diluted_share:.4f}")
    print(
        "PV of Terminal Value / Enterprise Value: "
        f"{terminal_value_share_of_enterprise_value:.4f}"
    )
    print_sensitivity_grid()
    print_reverse_dcf()


if __name__ == "__main__":
    main()
