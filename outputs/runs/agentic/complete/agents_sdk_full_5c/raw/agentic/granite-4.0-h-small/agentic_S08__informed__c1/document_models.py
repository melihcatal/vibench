import os
from typing import TypedDict

# Common document models used by extraction and later-step tasks

class InvoiceDocument(TypedDict):
    vendor: str
    date: str
    total: float
    line_items: list[dict]


class ReceiptDocument(TypedDict):
    merchant: str
    tax: float
    total: float
    items: list[dict]


class ExpenseRecord(TypedDict):
    provider: str
    document_type: str
    original_file: str
    normalized: dict
