import json
d = json.load(open('raw/tech_news_2026-10-24.json'))
r = json.load(open('raw/reddit_2026-10-24.json'))
for i in d['devto'][:8]:
    print('DEVTO', i['score'], '|', i['title'])
    print('   ', i['url'])
    print('   desc:', (i.get('description') or '')[:200])
print()
for i in r[:12]:
    print('REDDIT', '|', i['title'])
