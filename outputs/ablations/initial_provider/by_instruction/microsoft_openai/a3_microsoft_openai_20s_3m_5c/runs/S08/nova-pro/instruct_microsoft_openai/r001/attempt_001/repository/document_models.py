from typing import Dict, Any

class DocumentRequest:
    def __init__(self, document_type: str, document_path: str):
        self.document_type = document_type
        self.document_path = document_path

class DocumentResponse:
    def __init__(self, result: Dict[str, Any]):
        self.result = result