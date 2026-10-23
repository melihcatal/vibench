from typing import Any, Dict, List


class DocumentModel:
    def __init__(
        self,
        content: str,
        layout: List[Dict[str, Any]],
        tables: List[Dict[str, Any]],
        key_value_pairs: List[Dict[str, Any]],
    ):
        self.content = content
        self.layout = layout
        self.tables = tables
        self.key_value_pairs = key_value_pairs
