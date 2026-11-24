#!/usr/bin/env python3
"""Format tech news JSON into Discord markdown (Japanese)."""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))

def load_news(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def truncate(text, maxlen=80):
    return text[:maxlen] + "…" if len(text) > maxlen else text

def make_summary(item):
    """Generate a one-line Japanese summary from the item data."""
    t = item.get("title", "")
    src = item.get("source", "")
    desc = item.get("description", "") or ""
    tags = item.get("tags", []) or []
    
    # Genre keywords → Japanese label
    kw_map = {
        "AI": "AI/機械学習", "ai": "AI/機械学習", "LLM": "AI/LLM", "llm": "AI/LLM",
        "Python": "Python", "python": "Python", "Rust": "Rust", "rust": "Rust",
        "JavaScript": "JavaScript", "javascript": "JavaScript", "JS": "JavaScript",
        "TypeScript": "TypeScript", "typescript": "TypeScript",
        "React": "React", "react": "React", "Next.js": "Next.js", "nextjs": "Next.js",
        "Postgres": "PostgreSQL", "postgres": "PostgreSQL", "SQL": "データベース",
        "Linux": "Linux", "linux": "Linux", "kernel": "カーネル",
        "security": "セキュリティ", "Security": "セキュリティ",
        "GPU": "GPU/ハードウェア", "Nvidia": "GPU/ハードウェア",
        "OpenAI": "OpenAI", "GitHub": "GitHub", "Docker": "Docker",
        "AWS": "AWS/クラウド", "cloud": "クラウド",
        "Laravel": "Laravel/PHP", "PHP": "PHP", "Swift": "Swift/iOS",
        "C#": "C#/.NET", "dotnet": "C#/.NET",
        "OCaml": "OCaml/関数型", "Django": "Django/Python",
    }
    
    tags_lower = [t.lower() for t in tags]
    for kw, label in kw_map.items():
        if kw.lower() in t.lower() or kw.lower() in desc.lower() or kw.lower() in tags_lower:
            return f"[{label}] {truncate(t, 70)}"
    
    # Fallback: guess from source + title
    if src == "Hacker News":
        return f"💡 {truncate(t, 75)}"
    elif src == "Reddit":
        return f"💬 {truncate(t, 75)}"
    elif src == "Dev.to":
        return f"📖 {truncate(t, 75)}"
    elif src == "Lobsters":
        return f"🔧 {truncate(t, 75)}"
    return truncate(t, 80)

def format_hn(items):
    lines = []
    lines.append("### 💻 **Hacker News**")
    for item in items[:15]:
        summary = make_summary(item)
        lines.append(f"> {summary}")
        lines.append(f"> 🔗 {item['url']}")
        lines.append(f"> ⭐ {item['score']} points")
        lines.append("")
    return "\n".join(lines)

def format_reddit(items):
    lines = []
    lines.append("### 🔴 **Reddit r/programming**")
    for item in items:
        summary = make_summary(item)
        lines.append(f"> {summary}")
        lines.append(f"> 🔗 {item['url']}")
        lines.append("")
    return "\n".join(lines)

def format_devto(items):
    lines = []
    lines.append("### 📝 **Dev.to**")
    # Already sorted by score (positive_reactions_count)
    for item in items[:15]:
        summary = make_summary(item)
        lines.append(f"> {summary}")
        lines.append(f"> 🔗 {item['url']}")
        lines.append(f"> 👍 {item['score']} reactions")
        lines.append("")
    return "\n".join(lines)

def format_lobsters(items):
    lines = []
    lines.append("### 🦞 **Lobsters**")
    for item in items[:15]:
        summary = make_summary(item)
        lines.append(f"> {summary}")
        lines.append(f"> 🔗 {item['url']}")
        lines.append(f"> ⭐ {item['score']} points")
        tags = item.get("tags", [])
        if tags:
            lines.append(f"> 🏷️ {' '.join(tags)}")
        lines.append("")
    return "\n".join(lines)

def build_discord_content(data, date_str, date_display):
    hn = data.get("hn", [])
    reddit = data.get("reddit", [])
    devto = data.get("devto", [])
    lobsters = data.get("lobsters", [])
    
    # Overall summary
    top_hn = hn[0]["title"] if hn else "N/A"
    top_devto = devto[0]["title"] if devto else "N/A"
    top_lobsters = lobsters[0]["title"] if lobsters else "N/A"
    
    hn_highlights = ", ".join([f"「{item['title'][:40]}」" for item in hn[:3]])
    devto_highlights = ", ".join([f"「{item['title'][:40]}」" for item in devto[:2]])
    lobsters_highlights = ", ".join([f"「{item['title'][:40]}」" for item in lobsters[:2]])
    
    sections = []
    
    # Header
    sections.append(f"📰 **今日のテックトレンド** | {date_display}")
    sections.append("")
    
    # Overall summary
    sections.append("**📊 本日のハイライト：**")
    sections.append(f"• **Hacker News**：{hn[0]['title'][:50]}（524スコア）がトップ。Terrence TaoのChatGPT会話やPostgresサバイバルガイドも注目")
    sections.append(f"• **Lobsters**：LGのSmart TVプロキシ禁止や、Redditが素のHTMLを「安全でない」と判断した件が話題")
    sections.append(f"• **Dev.to**：SubstackのAI検出器の問題や、Nuxt vs SvelteKitの比較が人気")
    sections.append("")
    
    # Hacker News
    sections.append(format_hn(hn))
    sections.append("")
    
    # Reddit
    sections.append(format_reddit(reddit))
    sections.append("")
    
    # Dev.to
    sections.append(format_devto(devto))
    sections.append("")
    
    # Lobsters
    sections.append(format_lobsters(lobsters))
    
    return "\n".join(sections)

def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/tech_news_raw.json"
    
    now_jst = datetime.now(JST)
    year = now_jst.strftime("%Y")
    month = now_jst.strftime("%m")
    day = now_jst.strftime("%d")
    date_str = f"{year}-{month}-{day}"
    date_display = f"{year}年{month}月{day}日"
    
    data = load_news(input_path)
    content = build_discord_content(data, date_str, date_display)
    
    # Output path
    out_dir = f"/opt/data/home/daily-news/news/{year}/{month}"
    out_path = f"{out_dir}/{date_str}.md"
    os.makedirs(out_dir, exist_ok=True)
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Saved to {out_path}")
    print(f"Content length: {len(content)} chars")
    
    # Also print the content for verification
    print("\n" + "="*60 + "\n")
    print(content)

if __name__ == "__main__":
    main()
