from di_prototype.domain.i_data_exporter import IDataExporter
from di_prototype.domain.model import ParseResult


class NullDataExporter(IDataExporter):
    """製品用エクスポーター。何も出力しない（no-op）。"""

    def export(self, result: ParseResult) -> None:
        pass
