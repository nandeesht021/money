import requests
from bs4 import BeautifulSoup


def get_market_headlines():
    headlines = []

    # Economic Times RSS
    try:
        url = "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, "xml")
        items = soup.find_all("item")[:8]
        for item in items:
            headlines.append({
                "title": item.title.text.strip(),
                "source": "Economic Times"
            })
    except Exception as e:
        print(f"ET RSS error:{e}")

    # Moneycontrol RSS
    try:
        url = "https://www.moneycontrol.com/rss/marketreports.xml"
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.content, "xml")
        items = soup.find_all("item")[:5]
        for item in items:
            headlines.append({
                "title": item.title.text.strip(),
                "source": "Moneycontrol"
            })
    except Exception as e:
        print(f"MC RSS error:{e}")

    return headlines


if __name__ == "__main__":
    news = get_market_headlines()
    print(f"\nFetched{len(news)} headlines:\n")
    for i, n in enumerate(news, 1):
        print(f"{i}. [{n['source']}]{n['title']}")
