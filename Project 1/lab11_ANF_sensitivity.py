"""One-at-a-time sensitivity analysis for the ANF Lab 10 pro-forma.

Uses the linked Lab 10 model without changing its saved base inputs.  All
figures are USD millions except per-share values and percentages.
"""

from copy import deepcopy
import lab10_ANF_proforma as model


# Separate, immutable base inputs.  Ranges are independent percentage-point
# changes to each year of the specified input path.
BASE_INPUTS = {
    "revenue_growth": [0.05, 0.04, 0.03, 0.03, 0.03],
    "gross_margin": [0.61, 0.615, 0.62, 0.62, 0.62],
}

SCENARIOS = {
    "Revenue growth (-2.0 pp each year)": {
        "driver": "revenue_growth",
        "values": [0.03, 0.02, 0.01, 0.01, 0.01],
        "units": "% of prior-year revenue",
    },
    "Revenue growth (base)": {
        "driver": "revenue_growth",
        "values": BASE_INPUTS["revenue_growth"],
        "units": "% of prior-year revenue",
    },
    "Revenue growth (+2.0 pp each year)": {
        "driver": "revenue_growth",
        "values": [0.07, 0.06, 0.05, 0.05, 0.05],
        "units": "% of prior-year revenue",
    },
    "Gross margin (-2.0 pp each year)": {
        "driver": "gross_margin",
        "values": [0.59, 0.595, 0.60, 0.60, 0.60],
        "units": "% of revenue",
    },
    "Gross margin (base)": {
        "driver": "gross_margin",
        "values": BASE_INPUTS["gross_margin"],
        "units": "% of revenue",
    },
    "Gross margin (+2.0 pp each year)": {
        "driver": "gross_margin",
        "values": [0.63, 0.635, 0.64, 0.64, 0.64],
        "units": "% of revenue",
    },
}


def reset_base_inputs():
    """Restore every independent model input before a new scenario run."""
    model.REVENUE_GROWTH = deepcopy(BASE_INPUTS["revenue_growth"])
    model.GROSS_MARGIN = deepcopy(BASE_INPUTS["gross_margin"])


def run_scenario(name, scenario):
    """Run one scenario after resetting all independent inputs to base."""
    reset_base_inputs()
    if scenario["driver"] == "revenue_growth":
        model.REVENUE_GROWTH = deepcopy(scenario["values"])
    elif scenario["driver"] == "gross_margin":
        model.GROSS_MARGIN = deepcopy(scenario["values"])
    else:
        raise ValueError(f"Unknown driver: {scenario['driver']}")

    forecast, valuation = model.run_model()
    final = forecast[-1]
    checks_pass = all(
        abs(row["balance_check"]) < 0.01 and row["cash"] >= model.MINIMUM_CASH
        for row in forecast
    )
    return {
        "name": name,
        "driver": scenario["driver"],
        "values": scenario["values"],
        "units": scenario["units"],
        "final_ebit": final["ebit"],
        "final_fcff": final["unlevered_fcf"],
        "value_per_share": valuation["value_per_share"],
        "checks_pass": checks_pass,
        "trace": final,
    }


def print_result(result, base):
    values = ", ".join(f"{value:.1%}" for value in result["values"])
    print(f"\n{result['name']}")
    print(f"Input path (Y1-Y5): {values} [{result['units']}]")
    print(f"Final-year operating profit (EBIT): {result['final_ebit']:.2f}")
    print(f"Final-year FCFF: {result['final_fcff']:.2f}")
    print(f"Value per diluted share: ${result['value_per_share']:.2f}")
    print(f"Change from base - EBIT: {result['final_ebit'] - base['final_ebit']:+.2f}; "
          f"FCFF: {result['final_fcff'] - base['final_fcff']:+.2f}; "
          f"value/share: {result['value_per_share'] - base['value_per_share']:+.2f}")
    print(f"Accounting checks: {'PASS' if result['checks_pass'] else 'FAIL'}")
    trace = result["trace"]
    print(f"Trace, Year 5 - revenue {trace['revenue']:.2f}; gross profit "
          f"{trace['gross_profit']:.2f}; capex {trace['capex']:.2f}; "
          f"ending cash {trace['cash']:.2f}; balance check {trace['balance_check']:.6f}")


def span(results, key):
    values = [result[key] for result in results if result["checks_pass"]]
    return max(values) - min(values)


def same_within_rounding(first, second, tolerance=0.01):
    keys = ("final_ebit", "final_fcff", "value_per_share")
    return all(abs(first[key] - second[key]) <= tolerance for key in keys)


def main():
    try:
        revenue_results = [run_scenario(name, SCENARIOS[name]) for name in (
            "Revenue growth (-2.0 pp each year)",
            "Revenue growth (base)",
            "Revenue growth (+2.0 pp each year)",
        )]
        margin_results = [run_scenario(name, SCENARIOS[name]) for name in (
            "Gross margin (-2.0 pp each year)",
            "Gross margin (base)",
            "Gross margin (+2.0 pp each year)",
        )]
        base_before = revenue_results[1]

        print("ANF Lab 11 - One-at-a-Time Sensitivity Analysis")
        print("FCFF is unlevered free cash flow; all accounting quantities recalculate.")
        for result in revenue_results:
            print_result(result, base_before)
        for result in margin_results:
            print_result(result, base_before)

        print("\nOutput spans across valid lower/base/higher runs")
        for label, results in (("Revenue growth", revenue_results), ("Gross margin", margin_results)):
            print(f"{label}: EBIT {span(results, 'final_ebit'):.2f}; "
                  f"FCFF {span(results, 'final_fcff'):.2f}; "
                  f"value/share ${span(results, 'value_per_share'):.2f}")

        reset_base_inputs()
        base_after = run_scenario("Base restored", SCENARIOS["Revenue growth (base)"])
        restored = same_within_rounding(base_before, base_after)
        print("\nRestored-base check")
        print(f"Base before: EBIT {base_before['final_ebit']:.2f}; FCFF {base_before['final_fcff']:.2f}; "
              f"value/share ${base_before['value_per_share']:.2f}")
        print(f"Base after:  EBIT {base_after['final_ebit']:.2f}; FCFF {base_after['final_fcff']:.2f}; "
              f"value/share ${base_after['value_per_share']:.2f}")
        print(f"Restored base: {'PASS' if restored else 'FAIL'} (tolerance: $0.01)")
    finally:
        reset_base_inputs()


if __name__ == "__main__":
    main()
