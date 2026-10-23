import os
from typing import TypedDict
import requests
from document_models import InvoiceDocument, ReceiptDocument, ExpenseRecord

# Define unified expense schema

class NormalizedExpense(TypedDict):
    vendor: str
    date: str
    total: float
    line_items: list[dict]


def normalize_expense(raw: dict) -> NormalizedExpense:
    # Extremely simplified mapping from any source to standard keys
    vendor = raw.get('vendor') or raw.get('merchant') or ''
    date = raw.get('date') or ''
    total = float(raw.get('total', 0))
    line_items = [
        {
            'description': item.get('description', ''),
            'quantity': int(item.get('quantity', 0)),
            'unit_price': float(item.get('unit_price', 0)),
            'total': float(item.get('total', 0))
        }
        for item in raw.get('line_items', [])
    ]
    return {
        'vendor': vendor,
        'date': date,
        'total': total,
        'line_items': line_items
    }
