from typing import Any, Dict, List


class DocumentRequest:
    def __init__(self, document_path: str):
        self.document_path = document_path


class DocumentResponse:
    def __init__(
        self,
        content: str,
        pages: List[Dict[str, Any]],
        tables: List[Dict[str, Any]],
        key_value_pairs: List[Dict[str, Any]],
    ):
        self.content = content
        self.pages = pages
        self.tables = tables
        self.key_value_pairs = key_value_pairs
