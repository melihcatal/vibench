from typing import Any


class OCRResponse:
    def __init__(self, text: str, layout: Any, tables: Any, key_values: Any):
        self.text = text
        self.layout = layout
        self.tables = tables
        self.key_values = key_values
