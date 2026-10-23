import os
import requests
import json
from document_models import ReceiptDocument

# Generic client placeholder for receipt processing (same‑scenario)

class GenericClient:
    def process_receipt(self, file_bytes: bytes):
        # Stub response mimicking a receipt result
        return {
            "merchant_name": "Corner Store",
            "tax": 5.5,
            "total": 45.0,
            "items": [
                {"name": "Coffee", "price": 2.5},
                {"name": "Croissant", "price": 3.0}
            ]
        }

# Helper to extract fields from a receipt image (same‑scenario)
def extract_receipt_fields(file_path: str) -> ReceiptDocument:
    client = GenericClient()
    with open(file_path, 'rb') as f:
        result = client.process_receipt(f.read())
    receipt = ReceiptDocument(
        merchant=result['merchant_name'],
        tax=result['tax'],
        total=result['total'],
        items=[{'name': it['name'], 'price': it['price']} for it in result['items']]
    )
    return receipt
