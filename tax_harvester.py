def calculate_tax_saved(investments):
    """
    investments: list of dicts with keys:
    - name: fund name
    - buy_price: price when you bought
    - current_price: price today
    - units: number of units
    - holding_days: how many days held
    """

    gains = []
    losses = []

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

      total_profit = sum(profits)
total_loss = sum(losses)

if total_loss > 0:
    taxable_profit = total_profit - total_loss
else:
    taxable_profit = total_profit  # no change

tax = calculate_tax(taxable_profit)

    total_gain = sum(g["pnl"] for g in gains)
    total_loss = abs(sum(l["pnl"] for l in losses))

    # Without harvesting
    tax_without = sum(g["pnl"] * g["tax_rate"] for g in gains)

    # With harvesting — offset gains with losses
    net_taxable = max(0, total_gain - total_loss)
    avg_rate = (sum(g["tax_rate"]
                for g in gains) / len(gains)) if gains else 0.20
    tax_with = net_taxable * avg_rate

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
         "units": 100, "holding_days": 200},
        {"name": "IT Sector Fund", "buy_price": 200, "current_price": 160,
         "units": 50, "holding_days": 180},
        {"name": "Gold ETF", "buy_price": 50, "current_price": 65,
         "units": 200, "holding_days": 400},
    ]

    result = calculate_tax_saved(sample)
    print("\n=== Tax-Loss Harvesting Report ===")
    print(f"Total Gains  : ₹{result['total_gain']}")
    print(f"Total Losses : ₹{result['total_loss']}")
    print(f"Tax WITHOUT harvesting : ₹{result['tax_without_harvesting']}")
    print(f"Tax WITH harvesting    : ₹{result['tax_with_harvesting']}")
    print(f"💰 You Save            : ₹{result['tax_saved']}")
