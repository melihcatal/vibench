import os
import requests
import json
from document_models import InvoiceDocument

# Minimal generic client placeholder

class GenericClient:
    def process_invoice(self, file_bytes: bytes):
        # Replace with actual Mindee SDK call in production
        class DummyInvoice:
            vendor = {'name': 'Acme Corp'}
            date = '2024-07-15'
            total = 123.45
            items = [{'description': 'Widget', 'quantity': 2, 'unit_amount': 50.0, 'total_amount': 100.0}]
        return DummyInvoice()

    def process_receipt(self, file_bytes: bytes):
        # Stub for receipt processing
        return InvoiceDocument(vendor='Demo Inc', date='2024-07-01', total=99.99, line_items=[])

    def __init__(self, api_key: str | None = None):
        pass

# Helper to extract fields from an invoice image using Mindee Invoice OCR (same‑scenario)
def extract_invoice_fields(file_path: str) -> InvoiceDocument:
    client = GenericClient()
    with open(file_path, 'rb') as f:
        result = client.process_invoice(f.read())
    invoice = InvoiceDocument(
        vendor=result.vendor['name'],
        date=result.date,
        total=result.total,
        line_items=[
            {
                "description": it['description'],
                "quantity": it['quantity'],
                "unit_price": it['unit_amount'],
                "total": it['total_amount']
            }
            for it in result.items
        ],
    )
    return invoice
