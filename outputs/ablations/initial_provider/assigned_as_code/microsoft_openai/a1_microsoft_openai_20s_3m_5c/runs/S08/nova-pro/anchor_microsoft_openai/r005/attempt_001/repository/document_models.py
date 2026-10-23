from typing import Dict, List

class DocumentRequest:
    def __init__(self, document_type: str, document_image: bytes):
        self.document_type = document_type
        self.document_image = document_image

class DocumentResponse:
    def __init__(self, document_fields: Dict):
        self.document_fields = document_fields

class NormalizedExpense:
    def __init__(self, expense: Dict):
        self.expense = expense

    def to_json(self):
        return json.dumps(self.expense, indent=2)
