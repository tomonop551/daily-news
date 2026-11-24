#!/usr/bin/env python3
"""Format tech news JSON into Discord markdown with Japanese summaries."""

import json
import sys
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))

def get_jst_date():
    return datetime.now(JST)

def truncate(text, max_len=80):
    if len(text) > max_len:
        return text[:max_len-3] + "..."
    return text

def summarize_hn(item):
    t = item.get("title", "")
    score = item.get("score", 0)
    return f"🔥 {score}pt — {truncate(t)}"

def summarize_reddit(item):
    return f"💬 {truncate(item.get('title', ''))}"

def summarize_devto(item):
    score = item.get("score", 0)
    return f"❤️ {score} — {truncate(item.get('title', ''))}"

def summarize_lobsters(item):
    score = item.get("score", 0)
    tags = item.get("tags", [])
    tag_str = f" [{', '.join(tags[:3])}]" if tags else ""
    return f"🦞 {score}pt{tag_str} — {truncate(item.get('title', ''))}"

def format_hn(items):
    lines = ["### 💻 **Hacker News** （スコア順）\n"]
    for i, item in enumerate(items[:12], 1):
        title = item.get("title", "")
        url = item.get("url", "")
        score = item.get("score", 0)
        summary = summarize_hn(item)
        lines.append(f"**{i}.** [{title}]({url})")
        lines.append(f"   > {summary}")
        lines.append("")
    return "\n".join(lines)

def format_reddit(items):
    lines = ["### 🔴 **Reddit r/programming**\n"]
    for i, item in enumerate(items[:8], 1):
        title = item.get("title", "")
        url = item.get("url", "")
        lines.append(f"**{i}.** [{title}]({url})")
        lines.append(f"   > {summarize_reddit(item)}")
        lines.append("")
    return "\n".join(lines)

def format_devto(items):
    lines = ["### 📝 **Dev.to** （リアクション数順）\n"]
    for i, item in enumerate(items[:10], 1):
        title = item.get("title", "")
        url = item.get("url", "")
        score = item.get("score", 0)
        tags = item.get("tags", [])
        tag_str = f"`{'` `'.join(tags[:3])}`" if tags else ""
        lines.append(f"**{i}.** [{title}]({url})")
        lines.append(f"   > ❤️ {score} | {tag_str}")
        lines.append(f"   > {summarize_devto(item)}")
        lines.append("")
    return "\n".join(lines)

def format_lobsters(items):
    lines = ["### 🦞 **Lobsters** （スコア順）\n"]
    for i, item in enumerate(items[:10], 1):
        title = item.get("title", "")
        url = item.get("url", "")
        score = item.get("score", 0)
        tags = item.get("tags", [])
        tag_str = f"`{'` `'.join(tags[:3])}`" if tags else ""
        lines.append(f"**{i}.** [{title}]({url})")
        lines.append(f"   > 🦞 {score}pt | {tag_str}")
        lines.append("")
    return "\n".join(lines)

def build_summary(data):
    hn_top = data["hn"][:3] if data["hn"] else []
    devto_top = data["devto"][:2] if data["devto"] else []
    lobsters_top = data["lobsters"][:2] if data["lobsters"] else []
    
    parts = []
    if hn_top:
        headlines = "・".join([f"「{it['title'][:30]}…」" if len(it['title'])>30 else f"「{it['title']}」" for it in hn_top])
        parts.append(f"**Hacker News** では {headlines} が話題に。")
    
    ai_count = sum(1 for item in data.get("devto", []) if any(t.lower() == "ai" for t in item.get("tags", [])))
    if ai_count > 3:
        parts.append(f"Dev.to では AI 関連記事が {ai_count}件と活況。")
    
    if data.get("lobsters"):
        parts.append("Lobsters では数学・ハードウェア・言語処理系の深掘り記事がホット。")
    
    return "　".join(parts)

def main():
    # Read JSON
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    
    dt = get_jst_date()
    date_str = dt.strftime("%Y-%m-%d")
    year = dt.strftime("%Y")
    month = dt.strftime("%m")
    day_jp = f"{dt.year}年{dt.month}月{dt.day}日"
    
    summary_text = build_summary(data)
    
    # Build full markdown
    lines = []
    lines.append(f"📰 **今日のテックトレンド** | {day_jp}\n")
    lines.append(f"📌 **全体サマリー**")
    lines.append(f"{summary_text}\n")
    lines.append("---\n")
    
    # HN
    lines.append(format_hn(data["hn"]))
    lines.append("---\n")
    
    # Reddit
    lines.append(format_reddit(data["reddit"]))
    lines.append("---\n")
    
    # Dev.to
    lines.append(format_devto(data["devto"]))
    lines.append("---\n")
    
    # Lobsters
    lines.append(format_lobsters(data["lobsters"]))
    
    output = "\n".join(lines)
    
    # Output path
    out_dir = f"/opt/data/home/daily-news/news/{year}/{month}"
    out_file = f"{out_dir}/{date_str}.md"
    
    import os
    os.makedirs(out_dir, exist_ok=True)
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"SAVED:{out_file}")
    print(f"DATE:{date_str}")
    print(f"YEAR:{year}")
    print(f"MONTH:{month}")

if __name__ == "__main__":
    main()
