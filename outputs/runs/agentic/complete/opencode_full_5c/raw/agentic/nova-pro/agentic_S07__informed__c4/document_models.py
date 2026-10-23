from typing import Dict, List


class DocumentResponse:
    def __init__(
        self, text: str, layout: List[Dict], tables: List[Dict], key_values: Dict
    ):
        self.text = text
        self.layout = layout
        self.tables = tables
        self.key_values = key_values
