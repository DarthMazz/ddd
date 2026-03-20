from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from injector import inject

from di_prototype.domain.i_data_exporter import IDataExporter
from di_prototype.domain.i_logger import ILogger
from di_prototype.domain.model import ParseResult


class HtmlParser:
    """HTML ファイルを解析し ParseResult を返す。
    ILogger と IDataExporter は DI で注入される。
    """

    @inject
    def __init__(self, logger: ILogger, exporter: IDataExporter) -> None:
        self._logger = logger
        self._exporter = exporter

    def parse(self, file_path: str) -> ParseResult:
        self._logger.info(f"解析開始: {file_path}")

        html_text = Path(file_path).read_text(encoding="utf-8")
        self._logger.debug("HTML ファイルを読み込みました")

        soup = BeautifulSoup(html_text, "lxml")

        self._logger.debug("タイトルを抽出中")
        title = soup.title.get_text(strip=True) if soup.title else ""

        self._logger.debug("見出しを抽出中 (h1〜h3)")
        headings: List[str] = [
            tag.get_text(strip=True) for tag in soup.find_all(["h1", "h2", "h3"])
        ]

        self._logger.debug("本文段落を抽出中")
        paragraphs: List[str] = [
            p.get_text(strip=True) for p in soup.find_all("p") if p.get_text(strip=True)
        ]

        self._logger.debug("リンクを抽出中")
        links: List[str] = [
            a["href"] for a in soup.find_all("a", href=True)
        ]

        result = ParseResult(
            source_file=file_path,
            title=title,
            headings=headings,
            paragraphs=paragraphs,
            links=links,
        )

        self._exporter.export(result)
        self._logger.info(
            f"解析完了: title={result.title!r}, "
            f"headings={len(result.headings)}, "
            f"paragraphs={len(result.paragraphs)}, "
            f"links={len(result.links)}"
        )

        return result
