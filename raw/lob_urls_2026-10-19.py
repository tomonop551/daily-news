#!/usr/bin/env python3
"""Find comments_url / short_id for the lobsters stories we selected."""
import json, urllib.request

URL = "https://lobste.rs/hottest.json"
req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (compatible; HermesBot/1.0)"})
with urllib.request.urlopen(req, timeout=20) as r:
    data = json.loads(r.read().decode("utf-8"))

want = [
    "It's enough - vibecoding tag crossed from useless to harmful",
    "The NIST Elliptic Curves Seeds Bounty Has Been Claimed",
    "The Decoherence Trap: When AI slop drowns out the signal in an endless sea of noise",
    "The Brain Sandwich",
    "It took me nine years to hack my Xbox 360",
    "ARP! Tell your network to explain itself",
    "Men in tech #YesAllMen",
    "Intuitive concurrent programming in any language",
]
by_title = {s.get("title"): s for s in data}
for t in want:
    s = by_title.get(t)
    if not s:
        print("MISSING:", t)
        continue
    print(json.dumps({k: s.get(k) for k in ("title", "url", "comments_url", "short_id_url", "score")}, ensure_ascii=False))
