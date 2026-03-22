def calculate_tax_saved(investments):
    """
    Advanced Indian Tax Engine:
    - STCG: 20%
    - LTCG: 12.5% (after ₹1L exemption)
    - Loss offset rules applied
    """

    stcg_gains = []
    ltcg_gains = []
    stcg_losses = []
    ltcg_losses = []

    # Step 1: Categorize
    for inv in investments:
        pnl = (inv["current_price"] - inv["buy_price"]) * inv["units"]
        is_stcg = inv["holding_days"] < 365

        if pnl >= 0:
            if is_stcg:
                stcg_gains.append(pnl)
            else:
                ltcg_gains.append(pnl)
        else:
            if is_stcg:
                stcg_losses.append(abs(pnl))
            else:
                ltcg_losses.append(abs(pnl))

    # Totals
    total_stcg_gain = sum(stcg_gains)
    total_ltcg_gain = sum(ltcg_gains)
    total_stcg_loss = sum(stcg_losses)
    total_ltcg_loss = sum(ltcg_losses)

    # =========================
    # WITHOUT HARVESTING
    # =========================
    stcg_tax_without = total_stcg_gain * 0.20

    ltcg_taxable_without = max(0, total_ltcg_gain - 100000)
    ltcg_tax_without = ltcg_taxable_without * 0.125

    tax_without = stcg_tax_without + ltcg_tax_without

    # =========================
    # WITH HARVESTING
    # =========================

    # Rule 1: STCL can offset BOTH STCG & LTCG
    remaining_stcg_loss = total_stcg_loss

    # Offset STCG first
    if remaining_stcg_loss > 0:
        offset = min(total_stcg_gain, remaining_stcg_loss)
        total_stcg_gain -= offset
        remaining_stcg_loss -= offset

    # Then offset LTCG
    if remaining_stcg_loss > 0:
        offset = min(total_ltcg_gain, remaining_stcg_loss)
        total_ltcg_gain -= offset
        remaining_stcg_loss -= offset

    # Rule 2: LTCL can offset ONLY LTCG
    if total_ltcg_loss > 0:
        offset = min(total_ltcg_gain, total_ltcg_loss)
        total_ltcg_gain -= offset

    # Apply taxes AFTER offset
    stcg_tax_with = total_stcg_gain * 0.20

    ltcg_taxable_with = max(0, total_ltcg_gain - 100000)
    ltcg_tax_with = ltcg_taxable_with * 0.125

    tax_with = stcg_tax_with + ltcg_tax_with

    # =========================
    # TAX SAVED
    # =========================
    tax_saved = round(tax_without - tax_with, 2)

    # =========================
    # SMART SUGGESTION
    # =========================
    suggestions = []

    for inv in investments:
        pnl = (inv["current_price"] - inv["buy_price"]) * inv["units"]

        if pnl < 0:
            suggestions.append(
                f"Sell {inv['name']} to harvest loss of ₹{abs(round(pnl,2))}"
            )

    if not suggestions:
        suggestions.append("No tax harvesting opportunity (no losses)")

    return {
        "STCG_gain": round(sum(stcg_gains), 2),
        "LTCG_gain": round(sum(ltcg_gains), 2),
        "STCG_loss": round(total_stcg_loss, 2),
        "LTCG_loss": round(total_ltcg_loss, 2),
        "tax_without_harvesting": round(tax_without, 2),
        "tax_with_harvesting": round(tax_with, 2),
        "tax_saved": tax_saved,
        "suggestions": suggestions
    }
