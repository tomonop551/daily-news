#!/usr/bin/env python3
"""Validate the digest MD: section counts, every item has a wrapped URL + summary."""
import re, sys

path = sys.argv[1]
text = open(path, encoding="utf-8").read()
lines = text.splitlines()

sections = {}
cur = None
bad = []
for ln in lines:
    if ln.startswith("## "):
        cur = ln[3:].strip()
        sections[cur] = []
    elif cur and re.match(r"^\d+\. ", ln):
        sections[cur].append(ln)

for name, items in sections.items():
    print(f"{name}: {len(items)} items")
    for it in items:
        m = re.match(r"^\d+\. \*\*(.+?)\*\*。(.+?)=<(https?://[^>]+)>$", it)
        if not m:
            bad.append((name, it[:90]))

print("\nBAD LINES:", len(bad))
for b in bad:
    print(" -", b)

# any bare URLs outside <>?
bare = [l for l in lines if re.search(r"(?<!<)https?://", l)]
print("BARE URL LINES:", len(bare))
for l in bare:
    print(" !", l[:100])

print("\nTotal chars:", len(text))
print("Date header OK:", "2026年10月19日" in text)
