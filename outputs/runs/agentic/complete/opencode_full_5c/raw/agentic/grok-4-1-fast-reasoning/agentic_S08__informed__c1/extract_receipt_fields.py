import os
from datetime import date
from mindee.client import Client
from mindee.product.receipt import Receipt
from document_models import ReceiptFields
from typing import Dict, List


def extract_receipt_fields(file_path: str) -> ReceiptFields:
    api_key = os.getenv("MINDEE_API_KEY")
    client = Client(api_key=api_key)
    result = client.load(file_path).predict(Receipt)
    merchant = result.document.supplier.value
    date_str = result.document.date.value
    receipt_date = date.fromisoformat(date_str)
    total = result.document.total_amount.value
    tax = result.document.total_tax.value if result.document.total_tax else None
    items = [li.product_name.value for li in result.document.line_items]
    confidences = {
        "merchant": result.document.supplier.confidence,
        "date": result.document.date.confidence,
        "total": result.document.total_amount.confidence,
        "tax": result.document.total_tax.confidence
        if result.document.total_tax
        else 1.0,
    }
    return ReceiptFields(
        merchant=merchant, tax=tax, total=total, items=items, confidence=confidences
    )
