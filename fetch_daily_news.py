#!/usr/bin/env python3
"""Daily news summary for Discord delivery at 18:00 JST (09:00 UTC).
Fetches from 9 sources with 20-second rate limiting after each.
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
    except Exception:
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

def is_meta_post(title):
    t = title.lower()
    return any(kw in t for kw in ['thread', 'discussion', 'directory', 'questions', 'survey', 'reminder', 'announcement'])

japan, tech, anime_game, intl, science = [], [], [], [], []

# Source 1: Hacker News
hn = fetch_json('https://hacker-news.firebaseio.com/v0/topstories.json')
if hn:
    for sid in hn[:10]:
        item = fetch_json(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json')
        if item and item.get('title'):
            tech.append({'title': item['title'], 'source': 'Hacker News'})
time.sleep(20)

# Source 2: Reddit r/worldnews
data = fetch_json('https://api.rss2json.com/v1/api.json?rss_url=https://www.reddit.com/r/worldnews/.rss')
if data and 'items' in data:
    for it in data.get('items', [])[:10]:
        t = strip_html(it.get('title', ''))
        if is_meta_post(t): continue
        intl.append({'title': t, 'source': 'Reddit r/worldnews'})
time.sleep(20)

# Source 3: Reddit r/japan
data = fetch_json('https://api.rss2json.com/v1/api.json?rss_url=https://www.reddit.com/r/japan/.rss')
if data and 'items' in data:
    for it in data.get('items', [])[:10]:
        t = strip_html(it.get('title', ''))
        if is_meta_post(t): continue
        japan.append({'title': t, 'source': 'Reddit r/japan'})
time.sleep(20)

# Source 4: Reddit r/technology
data = fetch_json('https://api.rss2json.com/v1/api.json?rss_url=https://www.reddit.com/r/technology/.rss')
if data and 'items' in data:
    for it in data.get('items', [])[:10]:
        t = strip_html(it.get('title', ''))
        if is_meta_post(t): continue
        tech.append({'title': t, 'source': 'Reddit r/technology'})
time.sleep(20)

# Source 5: Reddit r/anime
data = fetch_json('https://api.rss2json.com/v1/api.json?rss_url=https://www.reddit.com/r/anime/.rss')
if data and 'items' in data:
    for it in data.get('items', [])[:10]:
        t = strip_html(it.get('title', ''))
        if is_meta_post(t): continue
        anime_game.append({'title': t, 'source': 'Reddit r/anime'})
time.sleep(20)

# Source 6: Reddit r/gaming
data = fetch_json('https://api.rss2json.com/v1/api.json?rss_url=https://www.reddit.com/r/gaming/.rss')
if data and 'items' in data:
    for it in data.get('items', [])[:10]:
        t = strip_html(it.get('title', ''))
        if is_meta_post(t): continue
        anime_game.append({'title': t, 'source': 'Reddit r/gaming'})
time.sleep(20)

# Source 7: Reddit r/Games
data = fetch_json('https://api.rss2json.com/v1/api.json?rss_url=https://www.reddit.com/r/Games/.rss')
if data and 'items' in data:
    for it in data.get('items', [])[:10]:
        t = strip_html(it.get('title', ''))
        if is_meta_post(t): continue
        anime_game.append({'title': t, 'source': 'Reddit r/Games'})
time.sleep(20)

# Source 8: Dev.to
devto = fetch_json('https://dev.to/api/articles?top=7&per_page=10')
if devto:
    for it in devto[:10]:
        tech.append({'title': it.get('title', ''), 'source': 'Dev.to'})
time.sleep(20)

# Source 9: Lobste.rs
lobsters = fetch_json('https://lobste.rs/hottest.json')
if lobsters:
    for it in lobsters[:10]:
        tech.append({'title': it.get('title', ''), 'source': 'Lobste.rs'})

# Science/Research: ArXiv
arxiv = fetch_rss('http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending')
if arxiv:
    for entry in re.findall(r'<entry>(.*?)</entry>', arxiv, re.DOTALL)[:5]:
        t = re.search(r'<title[^>]*>(.*?)</title>', entry, re.DOTALL)
        if t and t.group(1):
            science.append({'title': strip_html(t.group(1)), 'source': 'ArXiv CS.AI'})

# Output
jst_date = datetime.now().strftime('%Y年%m月%d日')
out = [f"📰 **デイリーサマリー** | {jst_date}", ""]

for section, items, emoji in [
    ('日本', japan, '🇯🇵'),
    ('テック & AI', tech, '💻'),
    ('アニメ & ゲーム', anime_game, '🎮'),
    ('国際 & 経済', intl, '🌍'),
    ('科学 & 研究', science, '🔬'),
]:
    out.append(f"{emoji} **{section}**")
    seen = set()
    for it in items[:5]:
        t = it['title']
        if t and t not in seen:
            seen.add(t)
            out.append(f"- {t} ({it['source']})")
    out.append("")

print("\n" + "\n".join(out))