from abc import ABC, abstractmethod


class ILogger(ABC):
    """ロガーインターフェース。開発用と製品用で実装を差し替える。"""

    @abstractmethod
    def info(self, msg: str) -> None:
        ...

    @abstractmethod
    def debug(self, msg: str) -> None:
        ...

    @abstractmethod
    def warn(self, msg: str) -> None:
        ...

    @abstractmethod
    def error(self, msg: str) -> None:
        ...
