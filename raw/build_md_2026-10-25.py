#!/usr/bin/env python3
"""Merge the curl-recovered Reddit feed and build the 2026-10-25 morning report."""

import json
import os

RAW = "/home/sophy/.hermes/home/daily-news/raw/tech_news_2026-10-25.json"
REDDIT = "/tmp/reddit_2026-10-25.json"
OUT = "/home/sophy/.hermes/home/daily-news/news/2026/10/2026-10-25.md"

data = json.load(open(RAW, encoding="utf-8"))
reddit = json.load(open(REDDIT, encoding="utf-8"))
assert len(reddit) >= 8, len(reddit)
data["reddit"] = reddit
all_items = data["hn"] + reddit + data["devto"] + data["lobsters"] + data["github"]
all_items.sort(key=lambda x: x["score"], reverse=True)
data["all"] = all_items[:100]
data.pop("failures", None)
data["failures_note"] = "rss2json 403 -> recovered via curl browser-UA .rss feed (25 items)"
with open(RAW, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

hn = data["hn"][:8]
rd = reddit[:8]
dev = data["devto"][:5]
lob = data["lobsters"][:8]

HN_S = [
    "自分の徒歩30分圏内のWikipedia記事だけを集めた「ローカル版Wikipedia」が公開され、位置情報から近隣の項目を最大25件表示する",
    "配信・録画ソフトOBS Studioのメジャー版33.0.0がリリース",
    "rqlite作者が、RaftとSQLiteを組み合わせた分散SQLiteの12年を振り返る",
    "物理学者が反物質粒子を1個、1カ月間にわたってトラップすることに成功",
    "「私は量子力学を理解していない」と題したサウサンプトン大学の解説ページが再び話題に",
    "Node.jsの脆弱性Node2ShellがHTTP2Shellへ発展し、多数のHTTPライブラリとアプリに影響が及ぶ(CVE-2026-111497)",
    "Rokuが開発者向けリポジトリをGitHubからGitLabへ移行",
    "無料の動的DNS・静的DNSサービスFreeDNSのサイトがHNで再注目",
]
RD_S = [
    "Brotliデコーダのリモートコード実行脆弱性Broccoli2Shell(CVE-2026-111497)がNode.jsやPythonなど広範囲に影響",
    "認証局eMudhraがCA鍵侵害に関するプレスリリースを公開、証明書事業からの撤退を説明",
    "純粋関数型プログラミングがC言語の性能にどこまで迫れるのかを実測した記事",
    "技術ドキュメントの欠陥や誤りをどう見つけ出すかを扱った記事",
    "freeしたメモリが実際どこへ行くのか、アロケータの挙動を掘り下げた解説",
    "自作コンテナランタイムを作る過程で気づいたDockerの奇妙な仕様をまとめた記事",
    "Clojure/Conj 2026でのStuart Hallowayによる「ものづくりの方法とその理由」講演",
    "macOS版gccのバイナリを解析して中身を調べた技術記事",
]
DEV_S = [
    "OSSプロジェクトを効果的に広めるための実践的な方法をまとめた記事",
    "AIによってソフトウェアセキュリティの対応速度が週単位から時間単位に変わったと論じる記事",
    "メールやClassroomの確認が面倒で、AIアシスタントを自作した話",
    "自作サービスCrowdwideの開発22日目、UIの仕上げが想像以上に大変だった記録",
    "ポートフォリオを、ディスプレイにテーマを挿すと開く遊び場に作り替えた作品紹介",
]
LOB_S = [
    "JavaScriptボタンでリンクを再実装せず、本物のリンクを使うよう訴えるWeb作法の記事",
    "自作コンテナランタイムを作って分かったDockerの奇妙な実装の数々を解説",
    "php2shell脆弱性で大規模な悪用が起きていない理由をPoCを追って検証した記事",
    "C言語の未定義動作は「最悪セグフォするだけ」ではないと具体例で示す反論記事",
    "xkcdのネタ「常に4を返す乱数」をZigコンパイラの組み込み関数として実装してみた話",
    "インド政府サイトが失効済みのeMudhra証明書を配信し続けているとの指摘",
    "ソフトウェアが遅いのは遅い言語のせいではなく設計のせいだと論じる記事",
    "純粋関数型言語の性能がC言語にどこまで近づけるかをベンチマークで検証",
]

for name, items, sums in (("hn", hn, HN_S), ("reddit", rd, RD_S), ("devto", dev, DEV_S), ("lobsters", lob, LOB_S)):
    assert len(items) == len(sums), (name, len(items), len(sums))

SM = {}
for items, sums in ((hn, HN_S), (rd, RD_S), (dev, DEV_S), (lob, LOB_S)):
    SM.update(dict(zip([it["title"] for it in items], sums)))

SUMMARY = (
    "今日はセキュリティと「性能をどう測るか」の話題が中心。BrotliデコーダのRCE"
    "「Broccoli2Shell／Node2Shell」(CVE-2026-111497)がNode.js・Python・多数のHTTPライブラリに"
    "波及し、HNとRedditの両方で上位を占めました。eMudhraのCA鍵侵害の余波も続き、"
    "インド政府サイトが失効済み証明書を配信しているとの指摘も。性能面では「純粋FPはCにどこまで迫れるか」"
    "「遅いのは言語ではなく設計のせい」といった計測・設計論が並び、リンクを壊すなというWeb作法ネタも人気です。"
)


def section(title, items):
    lines = [f"## {title}"]
    for i, it in enumerate(items, 1):
        s = SM[it["title"]]
        lines.append(f"{i}. **{it['title']}**。{s}=<{it['url']}>")
    return "\n".join(lines)


md = [
    "📰 **今日のテックトレンド** | 2026年10月25日",
    "",
    f"🌤️ **全体サマリー**: {SUMMARY}",
    "",
    section("💻 Hacker News", hn),
    "",
    section("🔴 Reddit r/programming", rd),
    "",
    section("📝 Dev.to", dev),
    "",
    section("🦞 Lobsters", lob),
    "",
    "（提供: Hacker News / Reddit / Dev.to / Lobsters）",
    "",
]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(md))
print("wrote", OUT)
print(open(OUT, encoding="utf-8").read())
