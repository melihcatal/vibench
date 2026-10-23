from typing import Dict, List


class InvoiceDocument:
    def __init__(self, vendor: str, date: str, total: float, line_items: List[Dict]):
        self.vendor = vendor
        self.date = date
        self.total = total
        self.line_items = line_items


class ReceiptDocument:
    def __init__(self, merchant: str, tax: float, total: float, items: List[Dict]):
        self.merchant = merchant
        self.tax = tax
        self.total = total
        self.items = items
