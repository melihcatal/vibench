from typing import Dict, List

class DocumentRequest:
    def __init__(self, image_path: str):
        self.image_path = image_path

class DocumentResponse:
    def __init__(self, fields: Dict):
        self.fields = fields

class NormalizedExpense:
    def __init__(self, vendor: str, date: str, total: str, line_items: List[str]):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items