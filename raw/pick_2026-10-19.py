#!/usr/bin/env python3
"""Print the digest selection from the fetched JSON (for the agent to summarize)."""
import json
import sys

path = sys.argv[1]
data = json.load(open(path, encoding="utf-8"))

def show(label, items):
    print(f"\n===== {label} ({len(items)}) =====")
    for i, it in enumerate(items, 1):
        print(f"{i}. TITLE: {it.get('title','')}")
        print(f"   URL: {it.get('url','')}")
        desc = (it.get('description') or '').strip().replace('\n', ' ')
        if desc:
            print(f"   DESC: {desc[:220]}")
        print(f"   SCORE: {it.get('score')} TAGS: {it.get('tags')}")

hn = sorted(data.get("hn", []), key=lambda x: x.get("score", 0), reverse=True)[:8]
reddit = data.get("reddit", [])[:8]
devto = sorted(data.get("devto", []), key=lambda x: x.get("score", 0), reverse=True)[:5]
lobsters = sorted(data.get("lobsters", []), key=lambda x: x.get("score", 0), reverse=True)[:8]

show("HN", hn)
show("REDDIT", reddit)
show("DEVTO", devto)
show("LOBSTERS", lobsters)
print("\nFAILURES:", data.get("failures"))
print("COUNTS:", {k: len(v) for k, v in data.items() if isinstance(v, list)})
