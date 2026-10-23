from typing import Any, Dict

class DocumentRequest:
    def __init__(self, document_path: str):
        self.document_path = document_path

class DocumentResponse:
    def __init__(self, result: Dict[str, Any]):
        self.result = result

class NormalizedExpense:
    def __init__(self, vendor: str, date: str, total: float, items: Dict[str, Any]):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.items = items