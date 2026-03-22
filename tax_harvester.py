def calculate_tax_saved(investments):
    """
    investments: list of dicts with keys:
    - name
    - buy_price
    - current_price
    - units
    - holding_days
    """

    gains = []
    losses = []

    # Step 1: Separate gains and losses
    for inv in investments:
        pnl = (inv["current_price"] - inv["buy_price"]) * inv["units"]

        tax_type = "STCG" if inv["holding_days"] < 365 else "LTCG"
        tax_rate = 0.20 if tax_type == "STCG" else 0.125

        entry = {
            "name": inv["name"],
            "pnl": round(pnl, 2),
            "type": tax_type,
            "tax_rate": tax_rate
        }

        if pnl >= 0:
            gains.append(entry)
        else:
            losses.append(entry)

    # Step 2: Calculate totals
    total_gain = sum(g["pnl"] for g in gains)
    total_loss = abs(sum(l["pnl"] for l in losses))  # convert to positive

    # Step 3: Tax WITHOUT harvesting
    tax_without = sum(g["pnl"] * g["tax_rate"] for g in gains)

    # Step 4: Tax WITH harvesting
    # Offset gains with losses
    net_taxable = max(0, total_gain - total_loss)

    # Apply weighted tax properly
    if total_gain > 0:
        weighted_tax = sum(g["pnl"] * g["tax_rate"] for g in gains) / total_gain
    else:
        weighted_tax = 0

    tax_with = net_taxable * weighted_tax

    # Step 5: Tax saved
    tax_saved = round(tax_without - tax_with, 2)

    return {
        "total_gain": round(total_gain, 2),
        "total_loss": round(total_loss, 2),
        "tax_without_harvesting": round(tax_without, 2),
        "tax_with_harvesting": round(tax_with, 2),
        "tax_saved": tax_saved
    }


if __name__ == "__main__":
    # Example portfolio
    sample = [
        {"name": "Nifty 50 Fund", "buy_price": 100, "current_price": 140,
         "units": 100, "holding_days": 200},   # profit

        {"name": "IT Sector Fund", "buy_price": 200, "current_price": 160,
         "units": 50, "holding_days": 180},    # LOSS

        {"name": "Gold ETF", "buy_price": 50, "current_price": 65,
         "units": 200, "holding_days": 400},   # profit
    ]

    result = calculate_tax_saved(sample)

    print("\n=== Tax-Loss Harvesting Report ===")
    print(f"Total Gains  : ₹{result['total_gain']}")
    print(f"Total Losses : ₹{result['total_loss']}")
    print(f"Tax WITHOUT harvesting : ₹{result['tax_without_harvesting']}")
    print(f"Tax WITH harvesting    : ₹{result['tax_with_harvesting']}")
    print(f"💰 You Save            : ₹{result['tax_saved']}")
