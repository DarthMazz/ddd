from di_prototype.domain.i_logger import ILogger


class NullLogger(ILogger):
    """製品用ロガー。すべての呼び出しを何もせずに受け流す（no-op）。"""

    def info(self, msg: str) -> None:
        pass

    def debug(self, msg: str) -> None:
        pass

    def warn(self, msg: str) -> None:
        pass

    def error(self, msg: str) -> None:
        pass
