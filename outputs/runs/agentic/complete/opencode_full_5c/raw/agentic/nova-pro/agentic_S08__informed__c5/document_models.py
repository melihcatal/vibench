from typing import Dict, List


class Document:
    def __init__(self, vendor: str, date: str, total: float, line_items: List[Dict]):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items
