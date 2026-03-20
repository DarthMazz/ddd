import dataclasses
import json
import os
from datetime import datetime
from pathlib import Path

from di_prototype.domain.i_data_exporter import IDataExporter
from di_prototype.domain.model import ParseResult

OUTPUT_DIR = Path("output")


class DevDataExporter(IDataExporter):
    """開発用エクスポーター。ParseResult を JSON ファイルとして ./output/ へ保存する。"""

    def export(self, result: ParseResult) -> None:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = OUTPUT_DIR / f"parse_result_{timestamp}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dataclasses.asdict(result), f, ensure_ascii=False, indent=2)
        print(f"[DevDataExporter] 検証用データを保存しました: {filename}")
