import datetime
import json
import os

ORDERS_FILE = "paper_orders.json"

# NOTE: For real Zerodha API, uncomment and use:
# from kiteconnect import KiteConnect
# kite = KiteConnect(api_key="your_api_key")


def simulate_sip_order(fund_name, amount, fund_symbol="NIFTYBEES"):
    """Simulates placing a SIP order — paper trade only"""

    orders = []
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r") as f:
            orders = json.load(f)

    order = {
        "order_id": f"PAPER{len(orders)+1:04d}",
        "date": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
        "fund": fund_name,
        "symbol": fund_symbol,
        "amount": amount,
        "status": "COMPLETE (Paper)",
        "type": "SIP"
    }

    orders.append(order)
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)

    print(f"✅ Order placed:{order['order_id']} |{fund_name} | ₹{amount}")
    return order


def get_order_history():
    if not os.path.exists(ORDERS_FILE):
        return []
    with open(ORDERS_FILE, "r") as f:
        return json.load(f)


def get_portfolio_value(allocation, amount):
    """Returns what each fund is worth based on allocation"""
    return {
        "Nifty 50 Index Fund": round(amount * allocation["equity_pct"] / 100),
        "Liquid Debt Fund": round(amount * allocation["debt_pct"] / 100),
        "Gold ETF": round(amount * allocation["gold_pct"] / 100)
    }


if __name__ == "__main__":
    print("=== Paper Trade Simulator ===\n")
    simulate_sip_order("Nifty 50 Index Fund", 5000)
    simulate_sip_order("Gold ETF", 1000)
    simulate_sip_order("Liquid Debt Fund", 2000)

    print("\n=== Order History ===")
    for order in get_order_history():
        print(
            f"{order['date']} |{order['order_id']} |{order['fund']} | ₹{order['amount']} |{order['status']}")
