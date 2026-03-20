# HTML 解析 DI プロトタイプ

Python の `injector` を使い、開発用・製品用の振る舞いを依存性注入で切り替えるプロトタイプです。

## ディレクトリ構成

```
di_prototype/
├── domain/
│   ├── model.py             # ParseResult（データクラス）
│   ├── i_logger.py          # ILogger インターフェース（ABC）
│   └── i_data_exporter.py   # IDataExporter インターフェース（ABC）
├── infrastructure/
│   ├── dev_logger.py        # DevLogger（開発用: 標準出力へ書き出す）
│   ├── null_logger.py       # NullLogger（製品用: no-op）
│   ├── dev_data_exporter.py # DevDataExporter（開発用: JSON ファイル保存）
│   └── null_data_exporter.py# NullDataExporter（製品用: no-op）
├── application/
│   └── html_parser.py       # HtmlParser（DI 受け取り先）
├── di/
│   ├── dev_module.py        # DevModule（injector.Module）
│   └── prod_module.py       # ProdModule（injector.Module）
├── main.py                  # CLI エントリポイント
├── sample.html              # 動作確認用サンプル HTML
└── requirements.txt
```

## セットアップ

> **前提**: [uv](https://docs.astral.sh/uv/) がインストール済みであること。

```bash
# リポジトリルートから distiller/ へ移動
cd distiller/

# Python 3.14 をインストール（未インストールの場合）
uv python install 3.14

# 仮想環境の作成 + 依存ライブラリのインストール
uv sync
```

`uv sync` を実行すると `.python-version`（3.14）を読み取り、自動的に仮想環境（`.venv/`）が作成されます。  
依存ライブラリは `pyproject.toml` から解決されます。

## 実行方法

`distiller/` ディレクトリから `uv run` で実行します。

### 開発モード（ログ + 検証用 JSON 出力あり）

```bash
uv run python -m di_prototype.main --mode dev --file di_prototype/sample.html
```

- 標準出力にステップごとのログが表示されます。
- `output/parse_result_<timestamp>.json` に解析結果が保存されます。

### 製品モード（ログ・ファイル出力なし）

```bash
uv run python -m di_prototype.main --mode prod --file di_prototype/sample.html
```

- 標準出力には最終結果の JSON のみ出力されます。
- ファイルへの書き込みは一切行われません。

### スクリプトエントリポイントでの実行

`pyproject.toml` に `di-prototype` スクリプトを定義しています。

```bash
uv run di-prototype --mode dev --file di_prototype/sample.html
```

## DI 切り替えの仕組み

```
--mode dev  → Injector(DevModule)  → HtmlParser(DevLogger,  DevDataExporter)
--mode prod → Injector(ProdModule) → HtmlParser(NullLogger, NullDataExporter)
```

`HtmlParser` は `ILogger` と `IDataExporter` のインターフェースだけに依存しており、  
モジュール切り替えのみで動作を変更できます。`HtmlParser` 本体のコードは変更不要です。

## モジュール依存関係

```
HtmlParser
  ├── ILogger        ← DevLogger / NullLogger
  └── IDataExporter  ← DevDataExporter / NullDataExporter
```
