import datetime
import json
import os

INVESTMENTS_FILE = "investments_log.json"


def calculate_roundup(amount_spent):
    next_10 = ((amount_spent // 10) + 1) * 10
    roundup = next_10 - amount_spent
    return roundup


def log_investment(amount_spent, roundup_amount, fund="Nifty 50 Index Fund"):
    log = []
    if os.path.exists(INVESTMENTS_FILE):
        with open(INVESTMENTS_FILE, "r") as f:
            log = json.load(f)

    entry = {
        "date": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
        "spent": amount_spent,
        "invested": roundup_amount,
        "fund": fund
    }
    log.append(entry)

    with open(INVESTMENTS_FILE, "w") as f:
        json.dump(log, f, indent=2)

    return entry


def get_total_invested():
    if not os.path.exists(INVESTMENTS_FILE):
        return 0
    with open(INVESTMENTS_FILE, "r") as f:
        log = json.load(f)
    return sum(entry["invested"] for entry in log)


def get_investment_log():
    if not os.path.exists(INVESTMENTS_FILE):
        return []
    with open(INVESTMENTS_FILE, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    print("=== UPI Round-up Simulator ===\n")
    while True:
        try:
            amount = float(
                input("Enter amount you just spent (₹), or 0 to quit: "))
            if amount == 0:
                break
            roundup = calculate_roundup(amount)
            entry = log_investment(amount, roundup)
            print(
                f"✅ Spent ₹{amount} → Investing ₹{roundup} into{entry['fund']}")
            print(f"💰 Total invested so far: ₹{get_total_invested()}\n")
        except ValueError:
            print("Please enter a valid number")
