import logging
import sys

from di_prototype.domain.i_logger import ILogger

_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class DevLogger(ILogger):
    """開発用ロガー。解析の各ステップを標準出力へ書き出す。"""

    def __init__(self) -> None:
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.DEBUG,
            format=_FORMAT,
            datefmt=_DATE_FORMAT,
        )
        self._logger = logging.getLogger("dev")

    def info(self, msg: str) -> None:
        self._logger.info(msg)

    def debug(self, msg: str) -> None:
        self._logger.debug(msg)

    def warn(self, msg: str) -> None:
        self._logger.warning(msg)

    def error(self, msg: str) -> None:
        self._logger.error(msg)
