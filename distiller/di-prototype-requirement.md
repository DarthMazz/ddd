# 要件定義書 — HTML 解析 DI プロトタイプ

## 1. 概要

Python の DI フレームワーク `injector` を利用し、HTML 解析処理における開発用・製品用の振る舞いを  
依存性注入によって切り替えるプロトタイプを実装する。

開発用は評価ログおよび検証用データを出力するが、製品用ではそれらを一切出力しない。  
ロジックの本体は同一インターフェースを通じて利用し、環境差異を DI の注入モジュールで吸収する。

---

## 2. 用語定義

| 用語 | 定義 |
|---|---|
| DI（依存性注入） | 依存オブジェクトを外部から注入することで結合度を下げる設計パターン |
| 開発モード | 評価ログ・検証用データを出力する動作環境 |
| 製品モード | ログ・検証用データを出力しない本番動作環境 |
| HTML 解析モジュール | HTML を受け取り、主要要素を抽出する処理単位 |
| ロガーインターフェース | ログ出力の抽象インターフェース。開発用と製品用で実装を差し替える |
| データエクスポーターインターフェース | 検証用データ出力の抽象インターフェース。同上 |

---

## 3. 機能要件

### 3.1 HTML 解析

- 入力として HTML ファイルのパスを受け取り、ファイルを読み込む。
- HTML をパースし、以下の要素を抽出する。
  - ページタイトル（`<title>` タグ）
  - 見出し一覧（`<h1>` 〜 `<h3>` タグ）
  - 本文テキスト（`<p>` タグ）
  - リンク一覧（`<a>` タグの `href` 属性）
- 抽出結果を構造化データ（`ParseResult`）として返す。

### 3.2 ロガーインターフェース（`ILogger`）

| 実装クラス | モード | 動作 |
|---|---|---|
| `DevLogger` | 開発用 | 解析開始・終了・各抽出ステップのログを標準出力へ書き出す |
| `NullLogger` | 製品用 | すべてのログ呼び出しを何もせずに受け流す（no-op） |

- インターフェースは `info(msg: str)`, `debug(msg: str)`, `warn(msg: str)`, `error(msg: str)` を定める。

### 3.3 データエクスポーターインターフェース（`IDataExporter`）

| 実装クラス | モード | 動作 |
|---|---|---|
| `DevDataExporter` | 開発用 | `ParseResult` を JSON ファイルとして `./output/` ディレクトリへ保存する |
| `NullDataExporter` | 製品用 | 何も出力しない（no-op） |

- インターフェースは `export(result: ParseResult) -> None` を定める。

### 3.4 DI による切り替え

- `injector` の `Module` を継承した以下の 2 つの注入設定クラスを実装する。

| クラス名 | 用途 | 注入するクラス |
|---|---|---|
| `DevModule` | 開発用 | `DevLogger`, `DevDataExporter` |
| `ProdModule` | 製品用 | `NullLogger`, `NullDataExporter` |

- `HtmlParser` は `ILogger` と `IDataExporter` をコンストラクタインジェクションで受け取る。
- `Injector` に渡すモジュールを切り替えることで、動作モードを一元変更できる。

### 3.5 エントリポイント

- `main.py` に以下の CLI 引数を設ける。
  - `--mode dev|prod`：起動時の DI モジュールを選択する（デフォルト: `prod`）
  - `--file <path>`：解析対象の HTML ファイルパスを指定する（必須）

---

## 4. 非機能要件

| 項目 | 内容 |
|---|---|
| 依存ライブラリ | `injector`, `beautifulsoup4`, `lxml`（HTML パース用） |
| パッケージ管理 | `uv`（`pyproject.toml` で依存を管理、`uv sync` で付帯環境を構築） |
| 製品モードの副作用ゼロ | 製品モードでは I/O 処理（ファイル書き込み・標準出力）が発生しないこと |
| テスト容易性 | `ILogger` / `IDataExporter` をモックに差し替えてユニットテストが書けること |
| 拡張性 | 新たな出力先（例: クラウドログ）は新しい実装クラスを追加するだけで対応できること |
| Python バージョン | 3.14 以上 |

---

## 5. ディレクトリ構成（案）

```
distiller/                        ← uv プロジェクトルート
├── pyproject.toml                # 依存管理・ビルド設定（uv）
├── .python-version               # Python バージョン固定（3.14）
└── di_prototype/
    ├── domain/
    │   ├── model.py          # ParseResult（データクラス）
    │   ├── i_logger.py       # ILogger インターフェース（ABC）
    │   └── i_data_exporter.py  # IDataExporter インターフェース（ABC）
    ├── infrastructure/
    │   ├── dev_logger.py     # DevLogger 実装
    │   ├── null_logger.py    # NullLogger 実装
    │   ├── dev_data_exporter.py   # DevDataExporter 実装
    │   └── null_data_exporter.py  # NullDataExporter 実装
    ├── application/
    │   └── html_parser.py    # HtmlParser（DI 受け取り先）
    ├── di/
    │   ├── dev_module.py     # DevModule（injector.Module）
    │   └── prod_module.py    # ProdModule（injector.Module）
    ├── main.py               # CLI エントリポイント
    ├── sample.html           # 動作確認用サンプル HTML
    └── README.md
```

---

## 6. 処理フロー

```
main.py 起動
  │
  ├─ --mode dev  → Injector(DevModule)  → HtmlParser(DevLogger, DevDataExporter)
  └─ --mode prod → Injector(ProdModule) → HtmlParser(NullLogger, NullDataExporter)
                                               │
                                               ▼
                                        HTML ファイルパスを受け取る・ファイルを読み込む
                                               │
                                               ▼
                                        ILogger.info("解析開始")  ← 開発のみ出力
                                               │
                                               ▼
                                        HTML パース
                                        （タイトル・見出し・本文・リンク抽出）
                                               │
                                               ▼
                                        ILogger.debug(各ステップ)  ← 開発のみ出力
                                               │
                                               ▼
                                        ParseResult を生成
                                               │
                                               ▼
                                        IDataExporter.export(result)  ← 開発のみ保存
                                               │
                                               ▼
                                        ILogger.info("解析完了")  ← 開発のみ出力
                                               │
                                               ▼
                                        ParseResult を返却
```

---

## 7. 決定事項（旧・未決事項）

| # | 項目 | 決定内容 |
|---|---|---|
| 1 | HTML の入力源 | ファイルパス指定（ファイル読み込み） |
| 2 | `DevDataExporter` の出力先ディレクトリ | `./output/` 固定パス |
| 3 | 検証用データのファイル形式 | JSON |
| 4 | テストフレームワーク | `pytest` を前提とする |
