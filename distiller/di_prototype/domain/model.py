from dataclasses import dataclass, field
from typing import List


@dataclass
class ParseResult:
    """HTML 解析結果を保持するデータクラス。"""

    source_file: str
    title: str
    headings: List[str] = field(default_factory=list)
    paragraphs: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)
