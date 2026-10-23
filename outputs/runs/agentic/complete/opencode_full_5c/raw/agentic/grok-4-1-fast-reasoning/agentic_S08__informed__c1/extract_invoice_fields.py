import os
from datetime import date
from mindee.client import Client
from mindee.product.invoice import Invoice
from document_models import InvoiceFields, LineItem
from typing import Dict


def extract_invoice_fields(file_path: str) -> InvoiceFields:
    api_key = os.getenv("MINDEE_API_KEY")
    client = Client(api_key=api_key)
    result = client.load(file_path).predict(Invoice)
    vendor = result.document.supplier.value
    date_str = result.document.date.value
    invoice_date = date.fromisoformat(date_str)
    total = result.document.total_amount.value
    line_items = []
    confidences = {}
    for li in result.document.line_items:
        line_items.append(
            LineItem(
                description=li.description.value,
                quantity=li.quantity.value,
                unit_price=li.unit_price.value,
                amount=li.total_amount.value,
                confidence=li.total_amount.confidence,
            )
        )
    confidences = {
        "vendor": result.document.supplier.confidence,
        "date": result.document.date.confidence,
        "total": result.document.total_amount.confidence,
    }
    return InvoiceFields(
        vendor=vendor,
        date=invoice_date,
        total=total,
        line_items=line_items,
        confidence=confidences,
    )
