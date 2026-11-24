#!/usr/bin/env python3
"""Fetch tech news from Hacker News, Reddit, Dev.to, Lobsters, and GitHub Trending."""

import json
import os
import sys
import time
import re
import urllib.request
import urllib.error

# ── Configuration ────────────────────────────────────────────────────────────
HN_TOP = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"
REDDIT_HOT = "https://www.reddit.com/r/programming/hot.json?limit=25"
DEVTO_TOP = "https://dev.to/api/articles?top=1&per_page=30"
LOBSTERS_HOT = "https://lobste.rs/hottest.json"
GITHUB_TRENDING = "https://api.github.com/search/repositories?q=stars:>200+pushed:>2026-07-04&sort=stars&order=desc&per_page=15"

USER_AGENT = "Mozilla/5.0 (compatible; HermesBot/1.0; +https://github.com/hermes/daily-news)"
TIMEOUT = 15
MAX_HN = 25  # Top N from HN
FAILURES = []  # URLs that failed to fetch (reported in JSON so the agent can backfill via kitesurf)

# ── HTTP helpers ─────────────────────────────────────────────────────────────

def fetch_json(url, headers=None):
    """Fetch a URL and parse JSON response."""
    req = urllib.request.Request(url, headers=headers or {"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"  [WARN] Failed to fetch {url}: {e}", file=sys.stderr)
        FAILURES.append(f"{url} ({e})")
        return None


# ── Source fetchers ──────────────────────────────────────────────────────────

def fetch_hn():
    """Fetch top stories from Hacker News."""
    print("  Fetching HN top stories...", file=sys.stderr)
    ids = fetch_json(HN_TOP)
    if not ids:
        return []
    items = []
    for story_id in ids[:MAX_HN]:
        data = fetch_json(HN_ITEM.format(story_id))
        if data and data.get("type") == "story" and data.get("title"):
            items.append({
                "source": "Hacker News",
                "title": data["title"],
                "url": data.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                "score": data.get("score", 0),
                "hn_id": story_id,
            })
        time.sleep(0.1)  # Rate limiting
    items.sort(key=lambda x: x["score"], reverse=True)
    return items


def fetch_reddit():
    """Fetch hot posts from r/programming via rss2json proxy."""
    print("  Fetching Reddit r/programming...", file=sys.stderr)
    data = fetch_json("https://api.rss2json.com/v1/api.json?rss_url=https://www.reddit.com/r/programming/.rss")
    if not data or "items" not in data:
        return []
    items = []
    for ritem in data.get("items", []):
        title = ritem.get("title", "")
        items.append({
            "source": "Reddit",
            "title": title,
            "url": ritem.get("link", ""),
            "score": 0,
            "comments": 0,
        })
    return items


def fetch_devto():
    """Fetch top articles from Dev.to."""
    print("  Fetching Dev.to articles...", file=sys.stderr)
    data = fetch_json(DEVTO_TOP)
    if not data:
        return []
    items = []
    for article in data:
        items.append({
            "source": "Dev.to",
            "title": article.get("title", ""),
            "url": article.get("url", ""),
            "score": article.get("positive_reactions_count", 0),
            "description": article.get("description", ""),
            "tags": article.get("tag_list", []),
        })
    items.sort(key=lambda x: x["score"], reverse=True)
    return items


def fetch_lobsters():
    """Fetch hottest stories from Lobsters."""
    print("  Fetching Lobsters stories...", file=sys.stderr)
    data = fetch_json(LOBSTERS_HOT)
    if not data:
        return []
    items = []
    for story in data:
        items.append({
            "source": "Lobsters",
            "title": story.get("title", ""),
            "url": story.get("url", story.get("comments_url", "")),
            "score": story.get("score", 0),
            "tags": story.get("tags", []),
        })
    items.sort(key=lambda x: x["score"], reverse=True)
    return items


def fetch_github():
    """Fetch trending GitHub repos."""
    print("  Fetching GitHub trending...", file=sys.stderr)
    data = fetch_json(GITHUB_TRENDING, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github.v3+json",
    })
    if not data or "items" not in data:
        return []
    items = []
    for repo in data["items"]:
        items.append({
            "source": "GitHub",
            "title": f"{repo.get('full_name', '')}: {repo.get('description', '') or '(no description)'}",
            "url": repo.get("html_url", ""),
            "score": repo.get("stargazers_count", 0),
            "description": repo.get("description", ""),
            "language": repo.get("language", ""),
        })
    items.sort(key=lambda x: x["score"], reverse=True)
    return items


# ── Main ─────────────────────────────────────────────────────────────────────

INVISIBLE_RE = re.compile(r'[\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad\u2060\u180e\u202a\u202b\u202c\u202d\u202e\u2066\u2067\u2068\u2069]')

def sanitize(obj):
    """Recursively strip invisible unicode from all string values."""
    if isinstance(obj, str):
        return INVISIBLE_RE.sub('', obj)
    elif isinstance(obj, list):
        return [sanitize(v) for v in obj]
    elif isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    return obj


def main():
    print("Fetching tech news...", file=sys.stderr)
    
    hn = fetch_hn()
    print(f"  Got {len(hn)} HN stories", file=sys.stderr)
    
    reddit = fetch_reddit()
    print(f"  Got {len(reddit)} Reddit posts", file=sys.stderr)
    
    devto = fetch_devto()
    print(f"  Got {len(devto)} Dev.to articles", file=sys.stderr)
    
    lobsters = fetch_lobsters()
    print(f"  Got {len(lobsters)} Lobsters stories", file=sys.stderr)
    
    github = fetch_github()
    print(f"  Got {len(github)} GitHub repos", file=sys.stderr)

    # Combine all items for the "all" feed (top by score)
    all_items = hn + reddit + devto + lobsters + github
    all_items.sort(key=lambda x: x["score"], reverse=True)
    all_items = all_items[:100]  # Keep top 100

    result = {
        "hn": hn,
        "reddit": reddit,
        "devto": devto,
        "lobsters": lobsters,
        "github": github,
        "all": all_items,
    }
    if FAILURES:
        result["failures"] = FAILURES
    result = sanitize(result)

    out_path = sys.argv[1] if len(sys.argv) > 1 else None
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved to {out_path}", file=sys.stderr)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
