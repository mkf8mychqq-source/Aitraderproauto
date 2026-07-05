import feedparser
from datetime import datetime, timezone

RSS_FEEDS = [
    "https://feeds.reuters.com/reuters/businessNews",
    "https://feeds.reuters.com/reuters/marketsNews",
    "https://www.investing.com/rss/news_25.rss",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
]

KEYWORDS = {
    "oil": ["oil", "crude", "wti", "brent", "opec", "iran", "hormuz", "inventory", "eia", "api"],
    "gold": ["gold", "xau", "fed", "inflation", "cpi", "dollar", "treasury", "geopolitical"],
    "crypto": ["bitcoin", "btc", "ethereum", "eth", "etf", "crypto", "binance", "coinbase"],
    "index": ["nasdaq", "spx", "s&p", "fed", "nvidia", "rates", "jobs", "payroll"],
}

POSITIVE = ["rise", "gain", "surge", "rally", "approve", "cut rates", "bull", "strong"]
NEGATIVE = ["fall", "drop", "plunge", "war", "attack", "sanction", "hike", "bear", "weak", "risk"]


def fetch_news(limit: int = 12):
    items = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                title = getattr(entry, "title", "").strip()
                link = getattr(entry, "link", "").strip()
                if title:
                    items.append({"title": title, "link": link})
        except Exception:
            continue
    seen = set()
    unique = []
    for item in items:
        key = item["title"].lower()
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique[:limit]


def classify_news(items):
    text = " ".join(i["title"].lower() for i in items)
    scores = {"oil": 0, "gold": 0, "crypto": 0, "index": 0}
    hits = []
    for market, words in KEYWORDS.items():
        for w in words:
            if w in text:
                scores[market] += 1
    for w in POSITIVE:
        if w in text:
            hits.append(f"偏多詞：{w}")
    for w in NEGATIVE:
        if w in text:
            hits.append(f"風險詞：{w}")
    return scores, hits[:5]


def build_news_summary():
    items = fetch_news()
    scores, hits = classify_news(items)
    lines = ["📰 新聞 / 市場情緒掃描"]
    if not items:
        lines.append("目前沒有抓到新聞 RSS，稍後再試。")
        return "\n".join(lines)
    for item in items[:6]:
        lines.append(f"- {item['title']}")
    lines.append(f"關聯分數：石油 {scores['oil']}｜黃金 {scores['gold']}｜加密 {scores['crypto']}｜指數 {scores['index']}")
    if hits:
        lines.append("關鍵情緒：" + "、".join(hits))
    return "\n".join(lines)
