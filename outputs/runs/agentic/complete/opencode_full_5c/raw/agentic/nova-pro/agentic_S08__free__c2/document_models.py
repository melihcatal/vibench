from typing import Dict


class DocumentRequest:
    def __init__(self, document_path: str):
        self.document_path = document_path


class DocumentResponse:
    def __init__(self, data: Dict):
        self.data = data
