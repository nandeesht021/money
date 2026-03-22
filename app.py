import streamlit as st
from auth import check_auth

# 🔐 AUTH FIRST
check_auth()

# 🔓 LOGOUT BUTTON
col1, col2 = st.columns([8, 1])
with col2:
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

# 👇 YOUR EXISTING APP
st.title("💰 FinSmart Dashboard")

# rest of your code...

st.set_page_config(
    page_title="FinSmart — AI Wealth Manager",
    page_icon="💰",
    layout="wide"
)

st.title("💰 FinSmart — Your AI Wealth Manager")
st.caption("Smart investing, automated for every Indian")

# Sidebar navigation
page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "📋 Risk Quiz",
    "📊 My Portfolio",
    "📰 Market News",
    "💸 Round-up Invest",
    "🧾 Tax Saver",
    "📈 SIP Tracker"
])

if page == "🏠 Home":
    st.header("Welcome to FinSmart")
    from market_data import get_current_price, get_multiple_prices
    prices = get_multiple_prices()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Nifty 50", f"₹{prices.get('Nifty 50', 'N/A')}")
    col2.metric("Sensex", f"₹{prices.get('Sensex', 'N/A')}")
    col3.metric("Gold ETF", f"₹{prices.get('Gold ETF', 'N/A')}")
    col4.metric("Liquid Fund", f"₹{prices.get('Liquid Fund', 'N/A')}")
    st.info("Use the sidebar to navigate. Start with the Risk Quiz!")

elif page == "📋 Risk Quiz":
    st.header("📋 Risk Profiling Quiz")
    st.write("Answer 5 questions to find your investor profile")

    age = st.slider("Q1. Your age", 18, 60, 22)
    income = st.number_input("Q2. Monthly income (₹)",
                             min_value=0, value=15000, step=1000)

    goal = st.selectbox("Q3. Investment goal", [
        "Retirement (long term)",
        "Buy a house (medium term)",
        "Travel or gadget (short term)"
    ])

    reaction = st.selectbox("Q4. If your investment drops 20%, you:", [
        "Buy more — great opportunity!",
        "Hold and wait patiently",
        "Sell immediately to stop loss"
    ])

    years = st.slider("Q5. Years you can keep money invested", 1, 30, 5)

    if st.button("Calculate My Risk Score"):
        score = 0
        score += 3 if age < 25 else (2 if age < 35 else 1)
        score += 3 if income > 50000 else (2 if income > 20000 else 1)
        score += 3 if "Retirement" in goal else (2 if "house" in goal else 1)
        score += 3 if "Buy more" in reaction else (
            2 if "Hold" in reaction else 1)
        score += 3 if years > 10 else (2 if years > 5 else 1)
        final = round((score / 15) * 10)

        st.session_state["risk_score"] = final

        if final <= 3:
            profile = "Conservative"
            color = "blue"
        elif final <= 7:
            profile = "Balanced"
            color = "orange"
        else:
            profile = "Aggressive"
            color = "red"

        st.success(f"Your Risk Score:{final}/10 —{profile} Investor")
        st.balloons()
elif page == "📊 My Portfolio":
    st.header("📊 My Portfolio")
    from portfolio_allocator import allocate_portfolio
    import plotly.express as px

    risk_score = st.session_state.get("risk_score", 5)
    st.info(
        f"Using risk score:{risk_score}/10. Take the quiz first to update this.")

    amount = st.number_input("Monthly SIP amount (₹)",
                             min_value=100, value=5000, step=500)

    allocation = allocate_portfolio(risk_score, amount)

    col1, col2, col3 = st.columns(3)
    col1.metric("Equity (Nifty 50)",
                f"₹{allocation['equity']}", f"{allocation['equity_pct']}%")
    col2.metric("Debt (Liquid Fund)",
                f"₹{allocation['debt']}", f"{allocation['debt_pct']}%")
    col3.metric(
        "Gold ETF", f"₹{allocation['gold']}", f"{allocation['gold_pct']}%")

    fig = px.pie(
        names=["Equity", "Debt", "Gold"],
        values=[allocation["equity_pct"],
                allocation["debt_pct"], allocation["gold_pct"]],
        title=f"Portfolio Split —{allocation['profile']} Profile",
        color_discrete_sequence=["#636EFA", "#EF553B", "#FFD700"]
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "💸 Round-up Invest":
    st.header("💸 UPI Round-up Simulator")
    from roundup_simulator import calculate_roundup, log_investment, get_total_invested, get_investment_log
    import pandas as pd

    st.write("Every time you spend, FinSmart rounds up and invests the spare change.")

    amount = st.number_input("Amount you just spent (₹)",
                             min_value=1.0, value=43.0, step=1.0)
    roundup = calculate_roundup(amount)

    st.info(
        f"You spent ₹{amount} → Rounding up to ₹{int(amount//10*10+10)} → Investing ₹{roundup}")

    if st.button("Invest Round-up Now"):
        entry = log_investment(amount, roundup)
        st.success(f"✅ ₹{roundup} invested into Nifty 50 Index Fund!")

    st.metric("Total Invested via Round-ups", f"₹{get_total_invested()}")

    log = get_investment_log()
    if log:
        df = pd.DataFrame(log)
        st.dataframe(df, use_container_width=True)

elif page == "📰 Market News":
    st.header("📰 Market News + Sentiment")
    from news_scraper import get_market_headlines
    from sentiment_engine import get_sentiment, get_overall_market_mood
    import pandas as pd

    if st.button("Refresh News"):
        st.rerun()

    with st.spinner("Fetching latest headlines..."):
        news = get_market_headlines()

    mood, action = get_overall_market_mood(news)
    st.subheader(mood)
    st.warning(f"Recommended Action:{action}")

    rows = []
    for n in news:
        rows.append({
            "Sentiment": get_sentiment(n["title"]),
            "Headline": n["title"],
            "Source": n["source"]
        })

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

elif page == "🧾 Tax Saver":
    st.header("🧾 Tax-Loss Harvesting Calculator")
    from tax_harvester import calculate_tax_saved

    st.write(
        "Add your investments below to see how much tax you can save before March 31")

    n = st.number_input("How many investments do you have?",
                        min_value=1, max_value=10, value=3)

    investments = []
    for i in range(int(n)):
        st.subheader(f"Investment{i+1}")
        col1, col2, col3, col4, col5 = st.columns(5)
        name = col1.text_input(
            f"Fund name", value=f"Fund{i+1}", key=f"name{i}")
        buy = col2.number_input("Buy price", value=100.0, key=f"buy{i}")
        current = col3.number_input(
            "Current price", value=120.0, key=f"cur{i}")
        units = col4.number_input("Units", value=100, key=f"units{i}")
        days = col5.number_input("Days held", value=200, key=f"days{i}")
        investments.append({
            "name": name, "buy_price": buy,
            "current_price": current, "units": units, "holding_days": days
        })

    if st.button("Calculate Tax Savings"):
        result = calculate_tax_saved(investments)
        col1, col2, col3 = st.columns(3)
        col1.metric("Tax without harvesting",
                    f"₹{result['tax_without_harvesting']}")
        col2.metric("Tax with harvesting", f"₹{result['tax_with_harvesting']}")
        col3.metric(
            "💰 You Save", f"₹{result['tax_saved']}", delta=f"₹{result['tax_saved']} saved")

elif page == "📈 SIP Tracker":
    st.header("📈 SIP Order Tracker")
    from zerodha_connect import simulate_sip_order, get_order_history
    import pandas as pd

    col1, col2 = st.columns(2)
    fund = col1.selectbox(
        "Fund", ["Nifty 50 Index Fund", "Gold ETF", "Liquid Debt Fund"])
    amount = col2.number_input(
        "SIP Amount (₹)", min_value=100, value=1000, step=100)

    if st.button("Place Paper SIP Order"):
        order = simulate_sip_order(fund, amount)
        st.success(f"✅ Order{order['order_id']} placed —{fund} for ₹{amount}")

    st.subheader("Order History")
    orders = get_order_history()
    if orders:
        df = pd.DataFrame(orders)
        st.dataframe(df, use_container_width=True)
        st.metric("Total SIP invested", f"₹{sum(o['amount'] for o in orders)}")
    else:
        st.info("No orders yet. Place your first SIP above!")
