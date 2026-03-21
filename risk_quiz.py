from portfolio_allocator import allocate_portfolio


def get_risk_score():
    print("=== FinSmart Risk Profiling Quiz ===\n")
    score = 0

    # Question 1
    age = int(input("Q1. What is your age? "))
    if age < 25:
        score += 3
    elif age < 35:
        score += 2
    else:
        score += 1

    # Question 2
    income = int(
        input("Q2. Monthly income in rupees (just the number, e.g. 25000): "))
    if income > 50000:
        score += 3
    elif income > 20000:
        score += 2
    else:
        score += 1

    # Question 3
    print("Q3. What is your investment goal?")
    print("1 = Retirement (long term)")
    print("2 = Buy a house (medium term)")
    print("3 = Travel or gadget (short term)")
    goal = int(input("Enter 1, 2 or 3: "))
    if goal == 1:
        score += 3
    elif goal == 2:
        score += 2
    else:
        score += 1

    # Question 4
    print("Q4. If your investment drops 20%, what do you do?")
    print("1 = Buy more (opportunity!)")
    print("2 = Hold and wait")
    print("3 = Sell immediately")
    reaction = int(input("Enter 1, 2 or 3: "))
    if reaction == 1:
        score += 3
    elif reaction == 2:
        score += 2
    else:
        score += 1

    # Question 5
    years = int(input("Q5. For how many years can you keep money invested? "))
    if years > 10:
        score += 3
    elif years > 5:
        score += 2
    else:
        score += 1

    # Final score out of 15 → convert to 1-10
    final_score = round((score / 15) * 10)

    print(f"\n✅ Your Risk Score:{final_score}/10")

    if final_score <= 3:
        print("📊 Profile: Conservative Investor — Safety first")
    elif final_score <= 7:
        print("📊 Profile: Balanced Investor — Mix of safety and growth")
    else:
        print("📊 Profile: Aggressive Investor — Maximum growth")

    return final_score


if __name__ == "__main__":
    get_risk_score()
amount = int(input("\nHow much do you want to invest monthly (₹)? "))
allocate_portfolio(final_score, amount)
