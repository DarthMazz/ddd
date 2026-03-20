---
title: Repository Copilot Instructions (Local Multi-Agent)
version: 0.1
---
# 目的
このリポジトリはDDDを実践するためのサンプルコードとドキュメントを保持します。Copilotはこのリポジトリのコードとドキュメントを生成・修正するためのエージェントとして機能します。

# 基本
- 変更は最小差分
- 不確実な前提は仮説と確認事項を明示
- 重要操作はHITL（承認待ち）

# ローカルで必ず確認すること
- install/build/lint/test/typecheck/format の実行方法を提示（不明なら質問）
- 実行結果に基づき次の手を決める（推測で進めない）

# マルチエージェント運用
- .github/agents/00_orchestrator.md の指示に従う
- workflow.md の順序とゲート（Reviewer/Security）を守る

# ディレクトリ構成
- トップに存在するDDDの範囲毎にディレクトリを分ける。
- トップに存在するディレクトリの中に、DDDの範囲毎のコードとドキュメントを保持する。
- ドキュメントはREADME.mdにまとめる。