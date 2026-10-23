from typing import Any, Dict


class DocumentRequest:
    def __init__(self, document_path: str):
        self.document_path = document_path


class DocumentResponse:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
