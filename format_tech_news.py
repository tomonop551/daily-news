#!/usr/bin/env python3
import json
import datetime
import sys

def format_tech_news():
    # Predefined JSON from the fetch execution
    json_text = """{"date": "2026-07-03", "items": [{"title": "Giant trees have no trouble pumping water to top branches", "url": "https://news.ycombinator.com/item?id=48780870", "source": "Hacker News", "score": 25}, {"title": "SearXNG: A free internet metasearch engine", "url": "https://news.ycombinator.com/item?id=48779454", "source": "Hacker News", "score": 98}, {"title": "Steam Controller Auto-Charge – pilot to magnetic charging puck using CV", "url": "https://news.ycombinator.com/item?id=48780865", "source": "Hacker News", "score": 22}, {"title": "Leanstral 1.5: Proof Abundance for All", "url": "https://news.ycombinator.com/item?id=48780801", "source": "Hacker News", "score": 21}, {"title": "Dispersion loss counteracts embedding condensation in small language models", "url": "https://news.ycombinator.com/item?id=48780826", "source": "Hacker News", "score": 13}, {"title": "Announcement: We've Updated The Rules, and April Is Finally Over", "url": "https://www.reddit.com/r/programming/comments/1tlh5aj/announcement_weve_updated_the_rules_and_april_is/", "source": "Reddit r/programming"}, {"title": "Linux has officially won", "url": "https://www.reddit.com/r/programming/comments/1um497y/linux_has_officially_won/", "source": "Reddit r/programming"}, {"title": "Hunting a 16-year-old SQLite bug with TLA+: is dqlite affected?", "url": "https://www.reddit.com/r/programming/comments/1umi3j4/hunting_a_16yearold_sqlite_bug_with_tla_is_dqlite/", "source": "Reddit r/programming"}, {"title": "Keynote: Linus Torvalds in Conversation with Dirk Hohndel", "url": "https://www.reddit.com/r/programming/comments/1umk39t/keynote_linus_torvalds_in_conversation_with_dirk/", "source": "Reddit r/programming"}, {"title": "Understanding Traceroute", "url": "https://www.reddit.com/r/programming/comments/1um4hyx/understanding_traceroute/", "source": "Reddit r/programming"}, {"title": "The Conspiracy Big Software Engineering Doesn't Want You to Know", "url": "https://dev.to/dailycontext/the-conspiracy-big-software-engineering-doesnt-want-you-to-know-5299", "source": "Dev.to", "score": 7}, {"title": "A Third Brain for your Second Brain", "url": "https://dev.to/dailycontext/a-third-brain-for-your-second-brain-38b4", "source": "Dev.to", "score": 6}, {"title": "Dev Opportunity Radar #6: Y Combinator Startup School, Open Source AI Grants, and a $60K APAC Hackathon", "url": "https://dev.to/devengers/dev-opportunity-radar-6-y-combinator-startup-school-open-source-ai-grants-and-a-60k-apac-4nlp", "source": "Dev.to", "score": 33}, {"title": "Protect Yourself, Mesh Yourself", "url": "https://dev.to/eschmechel/protect-yourself-mesh-yourself-3fkn", "source": "Dev.to", "score": 6}, {"title": "Choosing the Right Tooling Layer for Your Agent", "url": "https://dev.to/dailycontext/choosing-the-right-tooling-layer-for-your-agent-1eg2", "source": "Dev.to", "score": 6}, {"title": "Fourteener Lobsters", "url": "", "source": "Lobsters", "score": 206}, {"title": "Why implementing ActivityPub is hard, and why it doesn't have to be", "url": "https://hackers.pub/@fedify/2026/why-activitypub-is-hard", "source": "Lobsters", "score": 35}, {"title": "Clickhouse is winning the Observability Wars", "url": "https://matduggan.com/clickhouse-is-winning-the-observability-wars/", "source": "Lobsters", "score": 54}, {"title": "crustc: Entirety of rustc, translated to C", "url": "https://github.com/FractalFir/crustc", "source": "Lobsters", "score": 98}, {"title": "Arbitrary code execution breaking sandboxes in KDE Plasma", "url": "https://blog.kimiblock.top/2026/07/01/arbitrary-code-execution-in-kde-plasma/", "source": "Lobsters", "score": 35}]}"""
    
    # Parse the JSON
    data = json.loads(json_text)
    
    # Format as Discord markdown with emojis
    result = f"# 📱 Tech News - {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
    
    # Group items by source
    sources = {}
    for item in data['items']:
        source = item['source']
        if source not in sources:
            sources[source] = []
        sources[source].append(item)
    
    # Source emojis
    source_emojis = {
        'Hacker News': '🦄',
        'Reddit r/programming': '📝',
        'Dev.to': '💻',
        'Lobsters': '🦞'
    }
    
    # Add each source section
    for source, items in sources.items():
        emoji = source_emojis.get(source, '📊')
        result += f"## {emoji} {source}\n\n"
        for item in items:
            score_str = f" ({item.get('score', 0)})" if item.get('score') else ""
            if item.get('url'):
                result += f"• [{item['title']}]({item['url']}){score_str}\n"
            else:
                result += f"• {item['title']}{score_str}\n"
        result += "\n"
    
    # Save to file
    with open('/opt/data/home/daily-news/tech_news.md', 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✅ Tech news formatted and saved as /opt/data/home/daily-news/tech_news.md")

if __name__ == '__main__':
    format_tech_news()