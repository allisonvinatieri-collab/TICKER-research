"""Lab 08: ANF peer P/E valuation (all monetary inputs are USD per share).

LAB 08 RECORD — September 17, 2026
==================================
Target and comparison date
--------------------------
Target: Abercrombie & Fitch (ANF)
Comparison date: September 1, 2026

Peer policy
-----------
Consider public specialty-apparel retailers that primarily earn from owned
consumer brands sold through stores and digital channels. Qualify companies
with material differences in category mix, wholesale, rental/subscription,
geography, leverage, or earnings quality. Exclude businesses that are not
primarily comparable apparel retailers, have non-comparable or negative annual
GAAP EPS, or lack price and earnings data public by the comparison date.

Admitted qualified peers and source record
------------------------------------------
American Eagle Outfitters (AEO): operates the American Eagle and Aerie brands.
Difference: Aerie/OFFLINE changes its category mix and growth drivers.
FY2025 diluted EPS: $1.09; fiscal year ended January 31, 2026; 10-K filed
March 30, 2026. Source: SEC Form 10-K, Item 1 Business and Consolidated
Statements of Operations:
https://www.sec.gov/Archives/edgar/data/919012/000119312526132097/aeo-20260131.htm

Urban Outfitters (URBN): operates Urban Outfitters, Anthropologie, Free People,
FP Movement, and Nuuly. Difference: broader brand portfolio, wholesale
activity, and Nuuly rental/subscription business. Fiscal 2026 diluted EPS:
$5.06; fiscal year ended January 31, 2026; 10-K filed April 1, 2026. Source:
SEC Form 10-K, Item 1 Business and earnings-per-share disclosures:
https://www.sec.gov/Archives/edgar/data/912615/000119312526137916/urbn-20260131.htm

Target earnings and price record
--------------------------------
ANF FY2025 diluted EPS: $10.46; fiscal year ended January 31, 2026; reported
in the FY2025 10-K filed March 26, 2026. ANF, AEO, and URBN annual periods all
ended January 31, 2026, although fiscal-year labels differ. The September 1
closing-price inputs should be rechecked in Nasdaq Market Activity before
submission.

Validation and interpretation
-----------------------------
AEO hand check: $16.58 / $1.09 = 15.211009 P/E. The program returns an ANF
peer-implied range of $159.11 to $163.91 and a median of $161.51. Removing AEO
leaves URBN's $163.91 reference estimate, $2.40 above the two-peer median;
removing URBN leaves AEO's $159.11 reference estimate, $2.40 below it. One
remaining peer is a reference estimate, not a range; removing the sole peer
leaves no estimate.

DCF comparison and review
-------------------------
The saved FCFF DCF base value is $193.27 per share, with a $145.05-$235.83
sensitivity range. Its assumptions are FCFF growth of 8%, 7%, 6%, 5%, and 4%,
a 9.0% WACC, and 2.5% terminal growth. The peer-P/E median is $161.51, below
the DCF. Provisional call: Watch-defer; both methods exceed the September 1
ANF price of $140.68, but margin stability and broader growth need evidence.

Skeptical review: accept that two operationally different peers are a thin
comparison and that the peer prices use September 1 while the saved DCF price
reference uses September 9. Reject averaging the P/E and DCF or bridging P/E
with cash/debt: both are per-share equity values, but they use different
methods. Current margin durability remains unresolved because Week 3 evidence
showed tariff/mix pressure and uneven brand growth.

Decision-changing question: using a single common trading date, does the peer
range remain materially below the DCF after evidence on ANF margin durability?
"""

from statistics import median


# Editable inputs: September 1, 2026 comparison date.
TARGET = {
    "name": "Abercrombie & Fitch (ANF)",
    "price": 140.68,
    "diluted_eps": 10.46,
}

PEERS = [
    {"name": "American Eagle Outfitters (AEO)", "price": 16.58, "diluted_eps": 1.09},
    {"name": "Urban Outfitters (URBN)", "price": 79.29, "diluted_eps": 5.06},
]


def positive_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def key(name):
    return str(name).strip().casefold()


def unique_non_target_peers():
    target_key = key(TARGET.get("name", ""))
    seen = set()
    result = []
    for peer in PEERS:
        peer_key = key(peer.get("name", ""))
        if peer_key == target_key or peer_key in seen:
            continue
        seen.add(peer_key)
        result.append(peer)
    return result


def peer_multiple(peer):
    price = peer.get("price")
    diluted_eps = peer.get("diluted_eps")
    if not positive_number(price) or not positive_number(diluted_eps):
        return None
    return price / diluted_eps


def implied_price(multiple):
    target_eps = TARGET.get("diluted_eps")
    if not positive_number(target_eps):
        return None
    return multiple * target_eps


def print_full_estimate(valid_peers):
    if not valid_peers:
        print("Full-Peer Estimate: no usable peers")
        return None
    if not positive_number(TARGET.get("diluted_eps")):
        print("Full-Peer Estimate: not meaningful (target diluted EPS is missing or nonpositive)")
        return None

    multiples = [multiple for _, multiple in valid_peers]
    median_multiple = median(multiples)
    median_price = implied_price(median_multiple)
    if len(valid_peers) == 1:
        print(f"Reference P/E: {median_multiple:.6f}")
        print(f"Reference Implied Price: ${median_price:.2f}")
        print("Implied Price Range: no range (one valid peer)")
    else:
        minimum = min(multiples)
        maximum = max(multiples)
        print(f"Minimum Peer P/E: {minimum:.6f}")
        print(f"Median Peer P/E: {median_multiple:.6f}")
        print(f"Maximum Peer P/E: {maximum:.6f}")
        print(f"Minimum Implied Price: ${implied_price(minimum):.2f}")
        print(f"Median Implied Price: ${median_price:.2f}")
        print(f"Maximum Implied Price: ${implied_price(maximum):.2f}")
    return median_price


def print_leave_one_out(valid_peers, full_estimate):
    print("Leave-One-Out Median Implied Prices:")
    if not valid_peers:
        print("no usable peers")
        return
    if full_estimate is None:
        print("not meaningful (target diluted EPS is missing or nonpositive)")
        return
    for removed_peer, _ in valid_peers:
        remaining = [multiple for peer, multiple in valid_peers if peer is not removed_peer]
        name = removed_peer.get("name", "Unnamed Peer")
        if not remaining:
            print(f"Remove {name}: no estimate (no usable peers remain)")
            continue
        remaining_price = implied_price(median(remaining))
        change = remaining_price - full_estimate
        note = " (reference estimate; no range)" if len(remaining) == 1 else ""
        print(f"Remove {name}: ${remaining_price:.2f}{note}; change ${change:+.2f}")


def main():
    print(f"Target: {TARGET.get('name', 'Unnamed Target')}")
    print(f"Comparison-Date Target Price: ${TARGET.get('price', 0):.2f}")
    target_eps = TARGET.get("diluted_eps")
    if positive_number(target_eps):
        print(f"Target Diluted EPS: {target_eps:.6f}")
    else:
        print("Target Diluted EPS: not meaningful (missing or nonpositive)")

    print("Peer P/E Multiples:")
    valid_peers = []
    for peer in unique_non_target_peers():
        multiple = peer_multiple(peer)
        name = peer.get("name", "Unnamed Peer")
        if multiple is None:
            print(f"{name}: not meaningful (price or diluted EPS is missing or nonpositive)")
        else:
            print(f"{name}: {multiple:.6f}")
            valid_peers.append((peer, multiple))

    full_estimate = print_full_estimate(valid_peers)
    print_leave_one_out(valid_peers, full_estimate)


if __name__ == "__main__":
    main()
