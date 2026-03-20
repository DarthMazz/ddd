from injector import Module, provider, singleton

from di_prototype.domain.i_data_exporter import IDataExporter
from di_prototype.domain.i_logger import ILogger
from di_prototype.infrastructure.dev_data_exporter import DevDataExporter
from di_prototype.infrastructure.dev_logger import DevLogger


class DevModule(Module):
    """開発用 DI モジュール。評価ログと検証用データ出力を有効にする。"""

    @provider
    @singleton
    def provide_logger(self) -> ILogger:
        return DevLogger()

    @provider
    @singleton
    def provide_exporter(self) -> IDataExporter:
        return DevDataExporter()
