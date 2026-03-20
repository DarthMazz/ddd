from abc import ABC, abstractmethod

from .model import ParseResult


class IDataExporter(ABC):
    """検証用データエクスポーターインターフェース。開発用と製品用で実装を差し替える。"""

    @abstractmethod
    def export(self, result: ParseResult) -> None:
        ...
