from injector import Module, provider, singleton

from di_prototype.domain.i_data_exporter import IDataExporter
from di_prototype.domain.i_logger import ILogger
from di_prototype.infrastructure.null_data_exporter import NullDataExporter
from di_prototype.infrastructure.null_logger import NullLogger


class ProdModule(Module):
    """製品用 DI モジュール。ログ・データ出力を一切行わない（no-op）実装を注入する。"""

    @provider
    @singleton
    def provide_logger(self) -> ILogger:
        return NullLogger()

    @provider
    @singleton
    def provide_exporter(self) -> IDataExporter:
        return NullDataExporter()
