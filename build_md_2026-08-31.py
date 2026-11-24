#!/usr/bin/env python3
import json

DATA = "raw/tech_news_2026-08-31.json"
DATE_STR = "2026-08-31"
DAY_JP = "2026年8月31日"

d = json.load(open(DATA, encoding="utf-8"))

# Hand-written Japanese summaries keyed by (source, title). Fallback templates below.
SUMMARY = {
    ("Hacker News", "Creepy Crawlies"): "生物・生態系をテーマにしたエッセイ的な記事。今日のHNで最もスコアを集めた話題。",
    ("Hacker News", "Omarchy: Any User Process Can Escalate to Root"): "LinuxベースのOS「Omarchy」で、通常のユーザープロセスがroot権限へ昇格できる設計上の問題が指摘されたセキュリティ記事。",
    ("Hacker News", "European Commission Revives Push for Encryption Backdoors in ProtectEU Strategy"): "欧州委員会がProtectEU戦略で暗号化のバックドア導入を再び推進。プライバシーと法執行のせめぎ合いが焦点。",
    ("Hacker News", "Casey Muratori – The Root of the Root of All Evil – BSC 2026 [video]"): "Casey Muratori氏による「諸悪の根源」をテーマにした技術講演の動画。プログラミングの本質に迫る内容。",
    ("Hacker News", "Hacking IKEA Furniture"): "IKEA家具をハック／改造して電子機器や機構を組み込むDIYプロジェクトの紹介記事。",
    ("Hacker News", "Haiku R1/beta6 has been released"): "BeOS後継OS「Haiku」の新ベータ版R1/beta6がリリース。改善点と新機能がまとめられている。",
    ("Hacker News", "Europe's summer drought is so extreme that desertification is a growing threat"): "欧州の夏の干ばつが深刻化し、砂漠化の脅威が拡大している実情を報告する記事。",
    ("Hacker News", "Arbitrary code execution in QubesOS via copy-to-VM error reporting backchannel"): "QubesOSに、VMへのコピー時のエラー報告機能を悪用した任意コード実行の脆弱性。",
    ("Hacker News", "Longest Straight Line Paths on Water or Land on the Earth (2018)"): "地球上で水上・陸上を走る最長の直線経路を求めた地理計算の古典記事。",
    ("Hacker News", "METR and Redwood Offer Holy %^ Postmortem of the HuggingFace Hack"): "HuggingFaceの不正アクセス（ハック）をMETRとRedwood機関が事後分析した総括記事。",
    ("Hacker News", "What my dad taught me about AI coding in the 90s"): "1990年代に父親から学んだAIプログラミングの基礎について回想するエッセイ。",
    ("Hacker News", "Coordination Headwind: How Organizations Are Like Slime Molds"): "組織が粘菌のように協調する仕組みを考察し、連携の難しさ（Coordination Headwind）を論じる記事。",
}

# Dev.to summaries use description
DEVTO_SUMMARY = {
    "IND-TECH WEEKLY #1: Jio Files for India's Biggest-Ever IPO, Navi Bags ": "インドのテック週刊まとめ。Jioの史上最大規模IPO申請などインド市場の最新動向を紹介。",
    "I Built an Agent That Marked Its Own Finding as Already Known": "自らの発見を「既知」と判定してしまうAIエージェントを自作した開発者が、その設計過程を解説。",
    "Git Said It Succeeded. The State Said Otherwise.": "Gitの動作が「成功」を報告しつつ実際の状態と食い違うケースを検証し、正しい確認方法を解説。",
    "Two Projects, One Problem — What PlannerCritic and AdversarialDebate E...": "別々に作った2つのAIシステムが同じ問題にどう取り組むかを比較した記事。",
    "My Commit Said \"Stop Trusting the Receipt.\" That Is the Commit Where t...": "「受領証を信じるな」というメッセージをコミットに残した経緯から、検証の重要性を語る。",
    "I'm Looking for the Right Problem, Not the Right Job Title — Could It ...": "職種名ではなく「正しい問題」を探すエンジニアが、自身のキャリアについて綴る記事。",
    "Delta encoding multiplayer game state": "ブラウザ戦略ゲームで、マルチプレイのゲーム状態をデルタ符号化で圧縮送信する手法を解説。",
    "CPU, GPU, TPU, NPU, DPU, QPU: six chips, one question": "CPU/GPU/TPU/NPU/DPU/QPUの6種類のチップの違いを整理し、用途ごとの役割を解説。",
    "Tell Me About You": "コミュニティ記事。読者同士が自己紹介し合うことを促す対話型の投稿。",
    "Bugs Are Innocent Until Reproduced: Building Verdict, an Evidence-Firs...": "再現できるまでバグは「無罪」という思想に基づき、証拠重視のバグ報告ツール「Verdict」を開発した話。",
    "I gave an AI agent a production rollback button — then spent the hacka...": "AIエージェントに本番ロールバックボタンを付けた開発者が、MCP定義の1行ミスの怖さを語る。",
    "Nuxt useState vs ref(): Why Server State Leaks Across Users": "NuxtのuseStateとref()の違いを解説。モジュールスコープのrefがユーザー間で状態を漏らす落とし穴。",
}

def trunc(t, n=70):
    return t[:n] + "…" if len(t) > n else t

def esc(t):
    return t.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#x27;", "'")

def hn_sum(it):
    t = esc(it["title"])
    key = ("Hacker News", it["title"])
    s = SUMMARY.get(key)
    if not s:
        s = f"{trunc(t)}。Hacker Newsで話題になった記事。"
    return s

def reddit_sum(it):
    t = esc(it["title"])
    m = {
        "Reverse Engineering Unknown File Formats with ImHex": "「ImHex」を使い、未知のファイル形式をリバースエンジニアリングする方法を解説。",
        "How LLMs Actually Work": "大規模言語モデル（LLM）が実際にどう動作するのかを分かりやすく解説した記事。",
        "The Cost YAGNI Was Never About": "「YAGNI（余計なものは作るな）」原則の本質と、そのコストを巡る議論。",
        "Automating immersive reading": "没入型リーディングの自動化についての考察記事。",
        "Zod v4.5 adds schema compilation (3-9x faster validation)": "型検証ライブラリZod v4.5がスキーマコンパイルを追加し、バリデーションが3〜9倍高速化。",
        "Building Critical Infrastructure with htmx: Network Automation for the Pa...": "htmxを使いネットワーク自動化ツールの重要インフラを構築した事例紹介。",
        "Inside the TypeScript Checker: From Text to Types": "TypeScriptチェッカーがテキストから型へ変換される内部処理を解説。",
        "Coding a database proxy for fun": "楽しみながらデータベースプロキシを自作した開発者の記事。",
        "htmx 4.0.0 has been released!": "軽量Webライブラリhtmxのメジャーバージョン4.0.0がリリース。",
        "Announcement: We've Updated The Rules, and April Is Finally Over": "r/programmingの運営がルール更新と管理方針について告知。",
    }
    for k, v in m.items():
        if k in it["title"] or it["title"] in k:
            return v
    return f"「{trunc(t)}」に関するReddit r/programmingの投稿。"

def devto_sum(it):
    t = esc(it["title"])
    for k, v in DEVTO_SUMMARY.items():
        if k in it["title"] or it["title"] in k:
            return v
    return f"「{trunc(t)}」に関するDev.to記事。"

def lob_sum(it):
    t = esc(it["title"])
    m = {
        "Being kicked out of the tech industry": "テック業界を追われる経験を綴ったエッセイ。業界のあり方と居場所を考えさせられる内容。",
        "Creepy crawlies": "今日のHN同様、生物・生態系を巡る考察記事。Lobstersで高スコアを獲得。",
        "There's no such thing as Just a Tool": "「ただの道具」というものは存在しない、とツールの本質を哲学的に論じる記事。",
        "Debian and the sirens": "Debianの現状と、魅力的だが危険な誘惑（sirens）について考察するエッセイ。",
        "Gram Editor 3.3.0 Released": "Rustで書かれたテキストエディタ「Gram Editor」の新バージョン3.3.0がリリース。",
        "Introducing ReactOS 0.4.16": "Windows互換を目指すオープンソースOS「ReactOS」の新バージョン0.4.16が公開。",
        "California Passes AB-1856 For Open-Source Relief Over Age Verification": "カリフォルニア州が年齢認証を巡るオープンソース保護の法案AB-1856を可決。",
        "Rust Function Overloading - Call for Experimentation": "Rustの関数オーバーロード導入を巡り、実験参加を呼びかける提案記事。",
        "Bug blindness": "開発者はなぜバグが見えなくなるのか（Bug blindness）を考察するプラクティス記事。",
        "But where does taste come from?": "エンジニアリングにおける「美的感覚（taste）」の源泉について考察した記事。",
        "Omarchy: Any User Process Can Escalate to Root": "HNでも話題のOmarchyに、ユーザープロセスがrootへ昇格できるセキュリティ上の問題点を指摘。",
        "Transfer files over an ethernet patch cable": "イーサネットのパッチケーブルだけでファイルを転送する手法を解説。",
    }
    for k, v in m.items():
        if k in it["title"] or it["title"] in k:
            return v
    return f"「{trunc(t)}」についてLobstersで議論されている記事。"

def fmt_hn(items, n=12):
    L = ["### 💻 **Hacker News**（スコア順）\n"]
    for i, it in enumerate(items[:n], 1):
        L.append(f"**{i}.** [{esc(it['title'])}]({it['url']}) — ⬆️{it['score']}pt")
        L.append(f"   > {hn_sum(it)}")
        L.append("")
    return "\n".join(L)

def fmt_reddit(items, n=8):
    L = ["### 🔴 **Reddit r/programming**\n"]
    for i, it in enumerate(items[:n], 1):
        L.append(f"**{i}.** [{esc(it['title'])}]({it['url']})")
        L.append(f"   > {reddit_sum(it)}")
        L.append("")
    return "\n".join(L)

def fmt_devto(items, n=10):
    L = ["### 📝 **Dev.to**（リアクション数順）\n"]
    for i, it in enumerate(items[:n], 1):
        tags = "`" + "` `".join(it.get("tags", [])[:3]) + "`" if it.get("tags") else ""
        L.append(f"**{i}.** [{esc(it['title'])}]({it['url']}) — ❤️{it['score']} {tags}")
        L.append(f"   > {devto_sum(it)}")
        L.append("")
    return "\n".join(L)

def fmt_lob(items, n=10):
    L = ["### 🦞 **Lobsters**（スコア順）\n"]
    for i, it in enumerate(items[:n], 1):
        tags = "`" + "` `".join(it.get("tags", [])[:3]) + "`" if it.get("tags") else ""
        L.append(f"**{i}.** [{esc(it['title'])}]({it['url']}) — ⬆️{it['score']}pt {tags}")
        L.append(f"   > {lob_sum(it)}")
        L.append("")
    return "\n".join(L)

hn = d["hn"]; reddit = d["reddit"]; devto = d["devto"]; lob = d["lobsters"]

summary_lines = [
    f"• **Hacker News**：「{esc(hn[0]['title'])[:40]}」が{hn[0]['score']}ポイントでトップ、セキュリティ（Omarchy・QubesOS）ネタが複数ランクイン。",
    f"• **Lobsters/Dev.to**：Lobstersではキャリア論やRust、ReactOSリリースが注目。Dev.toはAIエージェント・検証に関する記事が活況。",
]
if github := d.get("github"):
    pass

parts = []
parts.append("📰 **今日のテックトレンド** | " + DAY_JP + "\n")
parts.append("📌 **全体サマリー**")
parts.append("  • Hacker News ではカジュアルな話題からセキュリティまで幅広く、最大スコアは「Creepy Crawlies」（654pt）。")
parts.append("  • Lobsters では「Being kicked out of the tech industry」がトップ、Dev.to ではAIエージェントとテスト・検証の記事が人気。")
parts.append("")
parts.append("---")
parts.append("")
parts.append(fmt_hn(hn))
parts.append("---")
parts.append("")
parts.append(fmt_reddit(reddit))
parts.append("---")
parts.append("")
parts.append(fmt_devto(devto))
parts.append("---")
parts.append("")
parts.append(fmt_lob(lob))

output = "\n".join(parts)

out_dir = f"/opt/data/home/daily-news/news/2026/08"
import os
os.makedirs(out_dir, exist_ok=True)
out_file = f"{out_dir}/{DATE_STR}.md"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(output + "\n")
print("SAVED:", out_file)
print(output)