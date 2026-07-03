#!/usr/bin/env python3
"""Fetch tech news for morning-tech-trends cron job.
Gets news from Hacker News, Reddit, Dev.to, Lobsters.
Outputs to stdout in fixed format to minimize AI requests.
"""
import urllib.request
import json
import re
import html
import time
from datetime import datetime

UA = 'Mozilla/5.0 (Hermes Daily News Bot)'

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return None

def fetch_rss(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode('utf-8')
    except Exception:
        return None

def strip_html(text):
    if not text: return ''
    text = re.sub(r'<!\[CDATA\[', '', text)
    text = re.sub(r'\]\]>', '', text)
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

items = []

# Hacker News
hn = fetch_json('https://hacker-news.firebaseio.com/v0/topstories.json')
if hn:
    for sid in hn[:5]:
        item = fetch_json(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json')
        if item and item.get('title'):
            items.append({'title': item['title'], 'url': f'https://news.ycombinator.com/item?id={sid}', 'source': 'Hacker News', 'score': item.get('score', 0)})
time.sleep(1)

# Reddit r/programming (RSS)
data = fetch_json('https://api.rss2json.com/v1/api.json?rss_url=https://www.reddit.com/r/programming/.rss')
if data and 'items' in data:
    for it in data.get('items', [])[:5]:
        items.append({'title': strip_html(it.get('title', '')), 'url': it.get('link', ''), 'source': 'Reddit r/programming'})
time.sleep(1)

# Dev.to (RSS)
devto = fetch_json('https://dev.to/api/articles?top=1&per_page=5')
if devto:
    for it in devto[:5]:
        items.append({'title': it.get('title', ''), 'url': it.get('url', ''), 'source': 'Dev.to', 'score': it.get('positive_reactions_count', 0)})
time.sleep(1)

# Lobsters
lobsters = fetch_json('https://lobste.rs/hottest.json')
if lobsters:
    for it in lobsters[:5]:
        items.append({'title': it.get('title', ''), 'url': it.get('url', ''), 'source': 'Lobsters', 'score': it.get('score', 0)})

# Output JSON for AI to process
print(json.dumps({'date': datetime.now().strftime('%Y-%m-%d'), 'items': items}, ensure_ascii=False))