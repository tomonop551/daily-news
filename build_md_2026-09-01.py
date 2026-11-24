#!/usr/bin/env python3
import json, os

DATA = "data/tech_news_2026-09-01.json"
DATE_STR = "2026-09-01"
DAY_JP = "2026年9月1日"

d = json.load(open(DATA, encoding="utf-8"))

# Hand-written Japanese summaries keyed by (source, title). Fallback templates below.
SUMMARY = {
    ("Hacker News", "OpenShot 4.0 – Open-source video editor"): "オープンソースの動画編集ソフト「OpenShot」がメジャー版4.0に。録画・編集・カラー補正がこれまで以上に強化された。今日HNでトップのスコアを獲得。",
    ("Hacker News", "Playa Phone"): "話題のモバイル端末「Playa Phone」についての紹介記事。斬新なハードウェア設計が注目を集める。",
    ("Hacker News", "I turned my security cameras into an automatic bird identification system"): "セキュリティカメラをBirdNETなどと組み合わせ、鳥を自動識別するシステムを自作した個人開発の記録。",
    ("Hacker News", "Apple caught off guard by AI demand for Mac Mini and Mac Studio"): "AI用途の需要急増でMac MiniとMac Studioが想定外の売れ行きとなり、Appleが対応に追われる状況を報じる。",
    ("Hacker News", "Dwarf Fortress is getting the mother of all magic updates"): "名作ローグライク「Dwarf Fortress」に、世界の宇宙構造にまで及ぶ大規模な魔法アップデートが来ると紹介。",
    ("Hacker News", "I think the military commissary's freezers were hacked"): "軍の売店（commissary）の冷凍庫が何者かにハッキングされた可能性を調査した個人による検証記事。",
    ("Hacker News", "ChatGPT Work Tool and Skill Reference"): "ChatGPT関連のWork Toolとスキル仕様を整理したリファレンス資料。エージェント開発者が注目。",
    ("Hacker News", "Internet centralization and the original sin of NAT"): "NAT（ネットワークアドレス変換）を「原罪」と位置づけ、インターネットの中央集権化の根源を論じる考察記事。",
    ("Hacker News", "A walkable ASCII cyberpunk city in one HTML file [video]"): "1つのHTMLファイルだけで歩き回れるASCIIアートのサイバーパンク都市を実現した作品の動画。",
    ("Hacker News", "ravynOS: Pre-alpha open-source OS based on Darwin, FreeBSD, Apple open-source"): "DarwinとFreeBSD、Appleのオープンソースを基盤にしたプレアルファ段階のオープンソースOS「ravynOS」。",
    ("Hacker News", "Tmp.0ut, Vol. 5"): "マルウェア解析・リバースエンジニアリングをテーマにしたZine「Tmp.0ut」の第5巻。",
    ("Hacker News", "Smartphone LED detects hidden cameras with AI"): "スマホのLEDとAIを使って隠しカメラを検出する技術について報じた記事。",
    ("Hacker News", "C++26: Standard Library Hardening Experiments"): "C++26に向けた標準ライブラリのハードニング（堅牢化）手法の実験をまとめた記事。",
    ("Hacker News", "Show HN: Laser Graffiti"): "レーザーで落書き（グラフィティ）を描くプロジェクトを紹介するShow HN。",
    ("Hacker News", "Terence Tao explains 6 essential mathematical concepts [video]"): "数学者テレンス・タオが重要な数学概念6つを解説する講義動画。",
    ("Hacker News", "Launch HN: Hebbian Robotics (YC S26) – Build scalable robotics data pipelines"): "YC S26出身のHebbian Roboticsが、スケーラブルなロボティクス向けデータパイプラインを発表したLaunch HN。",
}

DEVTO_SUMMARY = {
    "How long does it take for you to write a dev.to article?": "Dev.toの記事執筆にどれくらい時間がかかるかを開発者が語る対話型の投稿。開発者同士の共感を集めた。",
    "Remember CLAIM-24? Here's what happened.": "6月に公開したテスト・検証シリーズ「CLAIM-24」の続報。実際の検証結果と実装を振り返る。",
    "Fixing Delicate Cache Mismatches in a Brownfield SPA: A Pragmatic Solution": "DEVの本番環境で起きていた微妙なCSSキャッシュ不整合を、大規模書き換えなしに解決した実践的なノウハウ。",
    "Free AWS Certification for Students: The Complete Step-by-Step Guide": "学生向けのAWS認定資格バウチャー（$100相当）を無料で取得するための手順と注意点を完全ガイドにまとめた記事。",
    "I Tried to Beat Peter Norvig and Accidentally Became Ryan Gosling": "Peter Norvigに挑むべく書いたコードが思いがけない結果を生んだ過程を、ユーモアを交えて綴った記事。",
    "I'm 12. I built a social network for developers. Adults are NOT allowed.": "12歳の開発者が「大人禁止」の開発者向けSNSを自作したエピソードを語る投稿。",
    "My LLM Critic Flip-Flops on Every Run. That's Fine — Because a Frozenset Decides What's Fatal.": "LLMベースの批評エージェントが判定を揺らす問題と、frozensetによる致命的判定の設計について解説。",
    "Best Enterprise MCP Gateway for Your AI Agents in 2026": "AIエージェント向けのエンタープライズMCPゲートウェイの選定基準とおすすめを2026年版として紹介。",
    "Sessions vs JWTs: you are choosing how often you pay for state": "SessionsとJWTの選択が「状態に支払う頻度」の違いであると捉え、認証方式を比較する記事。",
}

def trunc(t, n=70):
    return t[:n] + "…" if len(t) > n else t

def esc(t):
    return t.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&").replace("&#x27;", "'").replace("&quot;", '"')

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
        "Announcement: We've Updated The Rules": "r/programmingの運営がルール更新と管理方針について告知。",
        "Please, I beg you, we need to stop using Stored Procedures": "アプリケーション層でのストアドプロシージャ（SP）利用をやめるべきだと強く訴える議論の多い投稿。",
        "a CVE dispute": "curlの著名開発者らを巻き込んだCVE（脆弱性ID）の扱いを巡る紛争についての投稿。",
        "The Hugging Face incident from a security engineering perspective": "Hugging Faceの不正アクセス事件をセキュリティエンジニアの視点から分析した投稿。",
        "p99 0 ms* autocomplete for 240 million domain names": "2億4000万件のドメイン名に対してp99をほぼ0msでオートコンプリートする技術の解説。",
        "A Self-Baked Async FFI Framework for Rust C# Interop": "RustとC#の相互運用のための自作Async FFIフレームワークを紹介する投稿。",
        "Node.js sandboxes powered by QuickJS and WebAssembly": "QuickJSとWebAssemblyを利用してNode.jsのサンドボックスを実現する手法を解説。",
        "Using stable and evolutionary problems to guide program decomposition": "安定かつ進化的な問題を用いてプログラムの分割を導く設計論を議論した投稿。",
        "On End-to-End Tests During Redesign": "リデザイン（UI刷新）期間中のエンドツーエンドテストの扱いについて論じた投稿。",
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
        "There's no such thing as Just a Tool": "「ただの道具」など実は存在しない、とツールの本質を哲学的に論じた記事。Lobstersで高スコア。",
        "Omarchy: Any User Process Can Escalate to Root": "LinuxベースOS「Omarchy」で通常のユーザープロセスがrootへ昇格できる設計上の問題を指摘するセキュリティ分析。",
        "But where does taste come from?": "エンジニアリング・デザインにおける「美的感覚（taste）」の源泉を考察した記事。",
        "curl: a CVE dispute": "curlのCVE刷新を巡る紛争について、作者のDaniel Stenbergが自らの見解を解説。",
        "Transfer files over an ethernet patch cable": "イーサネットのパッチケーブルだけでファイルを送受信する手法・原理を解説。",
        "VibeCoded AI-Slop License v1.0": "Vibe Coding（AI生成）による「AIスロップ」向けという風刺的なライセンス文書をユーモア交じりに公開。",
        "July in Servo: more platforms, faster canvas, web fonts in SVG": "Rust製ブラウザエンジンServoの2026年7月の進捗。対応プラットフォーム拡大やCanvas高速化などを報告。",
        "A Better SQL in 11 Lines of Code": "たった11行でより良いSQL処理を実現するという言語プロジェクトを紹介する記事。",
        "On not becoming a cyborg": "テクノロジーに過度に依存しない生き方（cyborg化しない選択）について綴ったエッセイ。",
        "Could Cargo's scheduler be better?": "RustのビルドツールCargoのスケジューラ改善の可能性を探る技術考察。",
        "Cancelation Terminology": "プログラミングにおける「キャンセル」関連の用語の整理と誤解を解く記事。",
        "Rootless Docker and Its Hidden Security Trade-Offs": "Rootless（非root）で動くDockerの実装が秘めるセキュリティ上のトレードオフを解説。",
        "Bootstrappable builds: how and why": "ブートストラップ可能なビルド（自己再現可能なビルド）の意義と実現方法を解説するLWN記事。",
        "C++26: Standard Library Hardening Experiments": "C++26標準ライブラリの堅牢化実験をまとめた記事。HNでも話題。",
    }
    for k, v in m.items():
        if k in it["title"] or it["title"] in k:
            return v
    return f"「{trunc(t)}」についてLobstersで議論されている記事。"

def _has_url(items):
    return [it for it in items if it.get("url")]

def fmt_hn(items, n=12):
    items = _has_url(items)
    L = ["💻 **Hacker News**（スコア順）\n"]
    for i, it in enumerate(items[:n], 1):
        L.append(f"**{i}.** [{esc(it['title'])}]({it['url']}) — ⬆️{it['score']}pt")
        L.append(f"   > {hn_sum(it)}")
        L.append("")
    return "\n".join(L)

def fmt_reddit(items, n=8):
    items = _has_url(items)
    L = ["🔴 **Reddit r/programming**\n"]
    for i, it in enumerate(items[:n], 1):
        L.append(f"**{i}.** [{esc(it['title'])}]({it['url']})")
        L.append(f"   > {reddit_sum(it)}")
        L.append("")
    return "\n".join(L)

def fmt_devto(items, n=10):
    items = _has_url(items)
    L = ["📝 **Dev.to**（リアクション数順）\n"]
    for i, it in enumerate(items[:n], 1):
        tags = "`" + "` `".join(it.get("tags", [])[:3]) + "`" if it.get("tags") else ""
        L.append(f"**{i}.** [{esc(it['title'])}]({it['url']}) — ❤️{it['score']} {tags}")
        L.append(f"   > {devto_sum(it)}")
        L.append("")
    return "\n".join(L)

def fmt_lob(items, n=10):
    items = _has_url(items)
    L = ["🦞 **Lobsters**（スコア順）\n"]
    for i, it in enumerate(items[:n], 1):
        tags = "`" + "` `".join(it.get("tags", [])[:3]) + "`" if it.get("tags") else ""
        L.append(f"**{i}.** [{esc(it['title'])}]({it['url']}) — ⬆️{it['score']}pt {tags}")
        L.append(f"   > {lob_sum(it)}")
        L.append("")
    return "\n".join(L)

hn = d["hn"]; reddit = d["reddit"]; devto = d["devto"]; lob = d["lobsters"]

parts = []
parts.append("📰 **今日のテックトレンド** | " + DAY_JP + "\n")
parts.append("📌 **全体サマリー**")
parts.append("  • Hacker News ではオープンソース動画編集ソフト **OpenShot 4.0**（489pt）がトップ。マークアップ系・セキュリティ・DIY系まで幅広い話題が並ぶ。")
parts.append("  • Lobsters ではツール論（「Just a Tool」）と Omarchy の権限昇格セキュリティネタが高スコア。Dev.to はAIエージェント・テスト・認証周りの記事が活況。")
parts.append("  • Reddit はストアドプロシージャ問題・Hugging Face 事件のセキュリティ分析・CVE 紛争など、開発者のホットトピックが集まった。")
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

out_dir = "/opt/data/home/daily-news/news/2026/09"
os.makedirs(out_dir, exist_ok=True)
out_file = f"{out_dir}/{DATE_STR}.md"
with open(out_file, "w", encoding="utf-8") as f:
    f.write(output + "\n")
print("SAVED:", out_file)
print(output)