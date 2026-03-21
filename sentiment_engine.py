def get_sentiment(headline):
    headline_lower = headline.lower()

    bullish_words = [
        "rally", "surge", "gain", "rise", "high", "record", "jump",
        "bull", "growth", "profit", "positive", "up", "strong",
        "boost", "recover", "buy", "outperform", "soar"
    ]

    bearish_words = [
        "fall", "crash", "drop", "loss", "low", "decline", "down",
        "bear", "weak", "sell", "fear", "risk", "cut", "plunge",
        "concern", "recession", "inflation", "hike", "negative"
    ]

    bull_count = sum(1 for w in bullish_words if w in headline_lower)
    bear_count = sum(1 for w in bearish_words if w in headline_lower)

    if bull_count > bear_count:
        return "🟢 Bullish"
    elif bear_count > bull_count:
        return "🔴 Bearish"
    else:
        return "🟡 Neutral"


def get_overall_market_mood(headlines):
    sentiments = [get_sentiment(h["title"]) for h in headlines]
    bullish = sentiments.count("🟢 Bullish")
    bearish = sentiments.count("🔴 Bearish")
    neutral = sentiments.count("🟡 Neutral")

    if bullish > bearish:
        mood = "🟢 Overall Market: BULLISH — Stay invested"
        action = "No rebalancing needed"
    elif bearish > bullish:
        mood = "🔴 Overall Market: BEARISH — Reduce risk"
        action = "Shift 10% from equity to gold/debt"
    else:
        mood = "🟡 Overall Market: NEUTRAL — Hold positions"
        action = "No change needed"

    return mood, action


if __name__ == "__main__":
    from news_scraper import get_market_headlines
    news = get_market_headlines()
    print("\n=== Sentiment Analysis ===\n")
    for n in news:
        sentiment = get_sentiment(n["title"])
        print(f"{sentiment} |{n['title'][:70]}")
    mood, action = get_overall_market_mood(news)
    print(f"\n{mood}")
    print(f"Recommended Action:{action}")
