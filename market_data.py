import yfinance as yf
import pandas as pd


def get_nifty_data():
    print("Fetching Nifty 50 data...")
    nifty = yf.download("^NSEI", period="1y", interval="1d")
    return nifty


def get_current_price(symbol="^NSEI"):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    price = round(data["Close"].iloc[-1], 2)
    return price


def get_multiple_prices():
    symbols = {
        "Nifty 50": "^NSEI",
        "Sensex": "^BSESN",
        "Gold ETF": "GOLDBEES.NS",
        "Liquid Fund": "LIQUIDBEES.NS"
    }
    prices = {}
    for name, symbol in symbols.items():
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="2d")
            price = round(data["Close"].iloc[-1], 2)
            prices[name] = price
        except:
            prices[name] = "N/A"
    return prices


if __name__ == "__main__":
    print("=== Live Market Prices ===")
    prices = get_multiple_prices()
    for name, price in prices.items():
        print(f"{name}: ₹{price}")

    print("\nFetching 1 year Nifty history...")
    df = get_nifty_data()
    print(df.tail())
