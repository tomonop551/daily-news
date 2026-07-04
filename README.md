# daily-news

毎朝のテックニュースを保存するリポジトリです。

## ディレクトリ構造

```text
daily-news/
├── README.md
└── news/
    └── YYYY/
        └── MM/
            └── YYYY-MM-DD.md
```

## 運用ルール

1. **ファイル命名規則**: `YYYY-MM-DD.md` フォーマット（例: `2026-06-10.md`）
2. **保存場所**: `news/YYYY/MM/` 配下
3. **更新タイミング**: 毎朝 6:00 JST に自動生成・push（cron job）
