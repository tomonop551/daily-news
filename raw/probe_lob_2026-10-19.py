#!/usr/bin/env python3
import json
data = json.load(open('/home/sophy/.hermes/home/daily-news/raw/tech_news_2026-10-19.json', encoding='utf-8'))
for s in sorted(data['lobsters'], key=lambda x: x['score'], reverse=True)[:8]:
    print(s['score'], '|', s['title'][:50], '| url=', repr(s.get('url')), '| keys=', list(s.keys()))
print('---- sample lobsters raw (first) ----')
print(json.dumps(data['lobsters'][0], ensure_ascii=False))
