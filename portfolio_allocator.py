def allocate_portfolio(risk_score, amount):
    print(f"\n=== Portfolio Allocation for ₹{amount} ===")
    print(f"Risk Score:{risk_score}/10\n")

    if risk_score <= 3:
        # Conservative
        equity = 0.20
        debt = 0.60
        gold = 0.20
        profile = "Conservative"
    elif risk_score <= 7:
        # Balanced
        equity = 0.50
        debt = 0.30
        gold = 0.20
        profile = "Balanced"
    else:
        # Aggressive
        equity = 0.80
        debt = 0.10
        gold = 0.10
        profile = "Aggressive"

    allocation = {
        "profile": profile,
        "equity": round(amount * equity),
        "debt": round(amount * debt),
        "gold": round(amount * gold),
        "equity_pct": int(equity * 100),
        "debt_pct": int(debt * 100),
        "gold_pct": int(gold * 100)
    }

    print(f"Profile     :{profile}")
    print(
        f"Equity (Nifty 50 Index Fund) : ₹{allocation['equity']} ({allocation['equity_pct']}%)")
    print(
        f"Debt   (Liquid Fund)          : ₹{allocation['debt']} ({allocation['debt_pct']}%)")
    print(
        f"Gold   (Gold ETF)             : ₹{allocation['gold']} ({allocation['gold_pct']}%)")

    return allocation


if __name__ == "__main__":
    score = int(input("Enter your risk score (1-10): "))
    amount = int(input("Enter investment amount in ₹: "))
    allocate_portfolio(score, amount)
