"""エントリポイント。

使い方:
    cd distiller/
    python -m di_prototype.main --mode dev --file di_prototype/sample.html
    python -m di_prototype.main --mode prod --file di_prototype/sample.html
"""
import argparse
import dataclasses
import json

from injector import Injector

from di_prototype.application.html_parser import HtmlParser
from di_prototype.di.dev_module import DevModule
from di_prototype.di.prod_module import ProdModule


def build_injector(mode: str) -> Injector:
    module = DevModule() if mode == "dev" else ProdModule()
    return Injector([module])


def main() -> None:
    parser = argparse.ArgumentParser(
        description="HTML 解析 DI プロトタイプ",
    )
    parser.add_argument(
        "--mode",
        choices=["dev", "prod"],
        default="prod",
        help="動作モード（dev: ログ・データ出力あり / prod: 出力なし）",
    )
    parser.add_argument(
        "--file",
        required=True,
        metavar="PATH",
        help="解析対象の HTML ファイルパス",
    )
    args = parser.parse_args()

    injector = build_injector(args.mode)
    html_parser = injector.get(HtmlParser)
    result = html_parser.parse(args.file)

    print(json.dumps(dataclasses.asdict(result), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
