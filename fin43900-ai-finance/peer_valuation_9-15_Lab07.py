"""Peer P/E valuation using only Python's standard library.

Reflection for a partner
------------------------
P/E measures the price investors pay for one dollar of diluted earnings:
price divided by diluted EPS. It helps compare companies because the multiple
normalizes prices by earnings, so a $200 stock is not automatically more
expensive than a $50 stock.

Peer policy before looking at the result: use AutoNation because it is a
public auto retailer; use Group 1 as a qualified peer because it is also a
public auto retailer but has differences in brand mix, geographic footprint,
financing and insurance income, acquisition pace, leverage, and earnings
quality. Exclude Asbury from the peer set because it is the target.

This script calculates each peer's P/E, takes the minimum, median, and maximum,
and multiplies those unrounded multiples by Asbury's diluted EPS. The resulting
peer-implied band is a comparison tool, not proof that Asbury is fairly valued:
the peers or Asbury may be mispriced, and their future growth, risk, margins,
and capital structures may differ.
"""

from statistics import median


# Editable inputs
TARGET = {
    "name": "Asbury Automotive (ABG)",
    "price": 243.03,
    "diluted_eps": 21.50,
}

PEERS = [
    {"name": "AutoNation (AN)", "price": 169.84, "diluted_eps": 16.92},
    {"name": "Group 1 Automotive (GPI)", "price": 421.48, "diluted_eps": 36.81},
]


def normalized_name(name):
    """Return a comparison key for peer names."""
    return str(name).strip().casefold()


def positive_number(value):
    """Return True only for present, positive numeric inputs."""
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value > 0


def deduplicated_peers():
    """Keep the first peer with each name and omit the target."""
    target_key = normalized_name(TARGET.get("name", ""))
    seen = set()
    unique = []

    for peer in PEERS:
        peer_key = normalized_name(peer.get("name", ""))
        if peer_key == target_key or peer_key in seen:
            continue
        seen.add(peer_key)
        unique.append(peer)
    return unique


def peer_pe(peer):
    """Return a peer P/E, or None when its inputs are not meaningful."""
    price = peer.get("price")
    diluted_eps = peer.get("diluted_eps")
    if not positive_number(price) or not positive_number(diluted_eps):
        return None
    return price / diluted_eps


def implied_price(multiple):
    """Return the target price implied by a P/E multiple, or None."""
    target_eps = TARGET.get("diluted_eps")
    if not positive_number(target_eps):
        return None
    return multiple * target_eps


def print_full_peer_estimate(valid_pes):
    """Print the full-peer implied valuation."""
    if not valid_pes:
        print("Full-Peer Estimate: no usable peers")
        return None

    if not positive_number(TARGET.get("diluted_eps")):
        print("Full-Peer Estimate: not meaningful (target diluted EPS is missing or nonpositive)")
        return None

    multiples = [pe for _, pe in valid_pes]
    median_multiple = median(multiples)
    median_price = implied_price(median_multiple)

    if len(valid_pes) == 1:
        print(f"Reference P/E: {median_multiple:.6f}")
        print(f"Reference Implied Price: ${median_price:.2f}")
        print("Implied Price Range: no range (one valid peer)")
    else:
        minimum_multiple = min(multiples)
        maximum_multiple = max(multiples)
        print(f"Minimum Peer P/E: {minimum_multiple:.6f}")
        print(f"Median Peer P/E: {median_multiple:.6f}")
        print(f"Maximum Peer P/E: {maximum_multiple:.6f}")
        print(f"Minimum Implied Price: ${implied_price(minimum_multiple):.2f}")
        print(f"Median Implied Price: ${median_price:.2f}")
        print(f"Maximum Implied Price: ${implied_price(maximum_multiple):.2f}")
    return median_price


def print_leave_one_out(valid_pes, full_peer_estimate):
    """Print median implied price after removing each valid peer."""
    print("Leave-One-Out Median Implied Prices:")
    if not valid_pes:
        print("no usable peers")
        return
    if full_peer_estimate is None:
        print("not meaningful (target diluted EPS is missing or nonpositive)")
        return

    for removed_peer, _ in valid_pes:
        remaining_pes = [pe for peer, pe in valid_pes if peer is not removed_peer]
        peer_name = removed_peer.get("name", "Unnamed Peer")
        if not remaining_pes:
            print(f"Remove {peer_name}: no estimate (no usable peers remain)")
            continue

        remaining_price = implied_price(median(remaining_pes))
        dollar_change = remaining_price - full_peer_estimate
        estimate_type = " (reference estimate; no range)" if len(remaining_pes) == 1 else ""
        print(
            f"Remove {peer_name}: ${remaining_price:.2f}{estimate_type}; "
            f"change from full-peer estimate ${dollar_change:+.2f}"
        )


def main():
    print(f"Target: {TARGET.get('name', 'Unnamed Target')}")
    target_eps = TARGET.get("diluted_eps")
    if positive_number(target_eps):
        print(f"Target Diluted EPS: {target_eps:.6f}")
    else:
        print("Target Diluted EPS: not meaningful (missing or nonpositive)")

    print("Peer P/E Multiples:")
    valid_pes = []
    for peer in deduplicated_peers():
        multiple = peer_pe(peer)
        peer_name = peer.get("name", "Unnamed Peer")
        if multiple is None:
            print(f"{peer_name}: not meaningful (price or diluted EPS is missing or nonpositive)")
        else:
            print(f"{peer_name}: {multiple:.6f}")
            valid_pes.append((peer, multiple))

    full_peer_estimate = print_full_peer_estimate(valid_pes)
    print_leave_one_out(valid_pes, full_peer_estimate)


if __name__ == "__main__":
    main()
