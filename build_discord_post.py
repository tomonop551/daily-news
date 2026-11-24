#!/usr/bin/env python3
"""Build Discord-formatted tech news post from fetched JSON data."""

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

def classify_title(title, desc="", tags=None):
    """Classify a news item into a Japanese genre label based on keywords."""
    tags = tags or []
    text = f"{title} {desc} {' '.join(tags)}".lower()

    kws = [
        (["llm", "gpt", "openai", "claude", "gemini", "chatgpt", "transformer",
          "language model", "foundation model", "mistral", "llama"], "AI/LLM"),
        (["machine learning", "deep learning", "neural net", "reinforcement learning",
          "pytorch", "tensorflow", "training", "fine-tun"], "ML/AI"),
        (["ai agent", "agent", "agentic", "autonomous"], "AIエージェント"),
        (["python", "django", "flask", "fastapi", "pypi"], "Python"),
        (["rust", "cargo", "rustc", "rustacean"], "Rust"),
        (["javascript", "typescript", "node.js", "nodejs", "react", "vue",
          "angular", "svelte", "next.js", "nuxt"], "JS/TS"),
        (["go ", "golang"], "Go"),
        (["kubernetes", "k8s", "docker", "containerd", "container"], "コンテナ/K8s"),
        (["aws", "gcp", "azure", "cloud", "lambda", "s3", "ec2"], "クラウド"),
        (["linux", "kernel", "unix", "posix", "systemd"], "Linux/OS"),
        (["security", "vulnerability", "cve", "exploit", "malware", "ransomware",
          "zero-day", "auth", "oauth", "saml", "jwt"], "セキュリティ"),
        (["database", "postgres", "postgresql", "mysql", "sqlite", "redis",
          "mongodb", "sql", "nosql"], "データベース"),
        (["gpu", "nvidia", "cuda", "amd", "rocm", "hardware", "chip", "processor"], "GPU/ハードウェア"),
        (["performance", "optimiz", "benchmark", "latency", "throughput"], "パフォーマンス"),
        (["open source", "oss", "floss", "commons", "foss"], "オープンソース"),
        (["startup", "venture", "funding", "yc ", "y combinator"], "スタートアップ"),
        (["web", "html", "css", "browser", "http", "wasm", "webassembly"], "Web"),
    ]
    for kw_list, label in kws:
        if any(kw in text for kw in kw_list):
            return f"[{label}] {truncate(title, 70)}"
    # Source-based fallback
    return f"💡 {truncate(title, 75)}"

def build_overall_summary(hn, devto, lobsters):
    """Dynamically build a 2-3 line overall summary."""
    lines = []
    highlights = []

    if hn:
        highlights.append(f"HNでは「{hn[0]['title'][:45]}」が{hn[0]['score']}スコアで話題")

    if lobsters:
        highlights.append(f"Lobstersでは「{lobsters[0]['title'][:45]}」が注目")

    if devto:
        highlights.append(f"Dev.toでは「{devto[0]['title'][:40]}」に反応集中")

    if len(highlights) >= 2:
        lines.append(f"• **Hacker News**：{highlights[0]}")
        lines.append(f"• **Lobsters/Dev.to**：{highlights[1]}")
    if len(highlights) >= 3:
        lines.append(f"• **その他**：{highlights[2]}")
    elif len(highlights) >= 1:
        # Use remaining
        pass

    if not lines:
        lines.append("• 本日は特集記事が少なめです")

    # Add GitHub trending note
    github_count = sum(1 for _ in [])
    lines.append("• **GitHub**：今週も多数の注目リポジトリが更新中")

    return "\n".join(lines)

def format_source(source_name, icon, items, max_items=15, extra_fields=None):
    """Format a source section."""
    lines = []
    lines.append(f"### {icon} **{source_name}**")
    if not items:
        lines.append("> データを取得できませんでした")
        return "\n".join(lines)

    for item in items[:max_items]:
        t = item.get("title", "")
        url = item.get("url", "")
        score = item.get("score", 0)
        tags = item.get("tags", []) or []
        description = item.get("description", "") or ""

        # Japanese summary line
        summary = classify_title(t, description, tags)
        lines.append(f"> {summary}")
        lines.append(f"> 🔗 {url}")

        if extra_fields:
            lines.append(f"> {extra_fields(item)}")
        elif source_name == "Hacker News":
            lines.append(f"> ⭐ {score} points")
        elif source_name == "Dev.to":
            lines.append(f"> 👍 {score} reactions")
        elif source_name == "Lobsters":
            lines.append(f"> ⭐ {score} points")
            if tags:
                lines.append(f"> 🏷️ {' '.join(tags)}")
        elif source_name == "Reddit":
            lines.append(f"> 💬 {score} upvotes")

        lines.append("")

    return "\n".join(lines)

def main():
    input_path = sys.argv[1] if len(sys.argv) > 1 else "/tmp/tech_news_raw.json"

    now_jst = datetime.now(JST)
    year = now_jst.strftime("%Y")
    month = now_jst.strftime("%m")
    day = now_jst.strftime("%d")
    date_str = f"{year}-{month}-{day}"
    date_display = f"{year}年{month}月{day}日"

    data = load_news(input_path)

    hn = data.get("hn", [])
    reddit = data.get("reddit", [])
    devto = data.get("devto", [])
    lobsters = data.get("lobsters", [])

    sections = []

    # ── Header ──
    sections.append(f"📰 **今日のテックトレンド** | {date_display}")
    sections.append("")

    # ── Overall summary (dynamically generated) ──
    sections.append("**📊 本日のハイライト：**")

    bullet_points = []
    if hn:
        bullet_points.append(
            f"• **Hacker News**：スコア{hn[0]['score']}で「{hn[0]['title'][:50]}」がトップ"
            + (f"。{hn[1]['title'][:40]}や{hn[2]['title'][:40]}も注目"
               if len(hn) >= 3 else "")
        )
    if lobsters:
        bullet_points.append(
            f"• **Lobsters**：{lobsters[0]['title'][:55]}（{lobsters[0]['score']}pts）が話題"
        )
    if devto:
        bullet_points.append(
            f"• **Dev.to**：{devto[0]['title'][:50]}（👍{devto[0]['score']}）が人気"
        )
    if reddit:
        bullet_points.append(f"• **Reddit**：注目の{len(reddit)}記事を紹介")

    for bp in bullet_points:
        sections.append(bp)

    # GitHub from data
    github = data.get("github", [])
    if github:
        top_repo = github[0]
        lang_info = f"（{top_repo.get('language', '')}）" if top_repo.get('language') else ""
        sections.append(
            f"• **GitHub**：{top_repo['title'][:60]}{lang_info}が★{top_repo['score']:,}でトップ"
        )

    sections.append("")

    # ── Hacker News ──
    sections.append(format_source("Hacker News", "💻", hn, 15))
    sections.append("")

    # ── Reddit ──
    if reddit:
        sections.append(format_source("Reddit r/programming", "🔴", reddit, 15))
        sections.append("")

    # ── Dev.to ──
    sections.append(format_source("Dev.to", "📝", devto, 15))
    sections.append("")

    # ── Lobsters ──
    sections.append(format_source("Lobsters", "🦞", lobsters, 15))

    content = "\n".join(sections)

    # Save
    out_dir = f"/opt/data/home/daily-news/news/{year}/{month}"
    out_path = f"{out_dir}/{date_str}.md"
    os.makedirs(out_dir, exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"SAVED:{out_path}")
    print(f"LENGTH:{len(content)}")
    print("---CONTENT_START---")
    print(content)
    print("---CONTENT_END---")

if __name__ == "__main__":
    main()
