import json

d = json.load(open('/home/sophy/.hermes/home/daily-news/raw/tech_news_2026-10-25.json'))
print("failures:", d.get("failures"))
for key, n in (("hn", 15), ("devto", 15), ("lobsters", 15), ("github", 6)):
    print("=" * 20, key)
    for i, it in enumerate(d.get(key, [])[:n]):
        print(i, "|", it.get("score"), "|", it.get("title"))
        print("    ", it.get("url"))
        if it.get("tags"):
            print("     tags:", it.get("tags"))
