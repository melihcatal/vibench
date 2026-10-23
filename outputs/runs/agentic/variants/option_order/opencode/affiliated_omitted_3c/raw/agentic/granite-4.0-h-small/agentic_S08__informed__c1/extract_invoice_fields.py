# [SAME-SCENARIO] extract_invoice_fields.py
# Extract vendor, date, total, and line-item fields from an invoice using Mindee Invoice OCR

import os
import mindee
from document_client import DocumentClient

MINDEE_API_KEY = os.getenv("MINDEE_API_KEY")


class InvoiceExtractor:
    def __init__(self):
        self.client = mindee.Client(api_key=MINDEE_API_KEY)
        self.doc_client = DocumentClient()

    def extract(self, image_bytes):
        # Use Mindee's Invoice OCR
        doc = self.client.invoices.parse_from_source(image_bytes)
        # Transform Mindee response into our normalized fields
        vendor = doc.invoice.supplier.name or ""
        date = doc.invoice.date_original or ""
        total = doc.invoice.total or 0.0
        line_items = [
            {
                "description": item.product_name,
                "quantity": item.quantity,
                "unit_price": item.total / item.quantity if item.quantity else 0,
                "total": item.total,
            }
            for item in doc.invoice.items
        ]
        return {
            "vendor": vendor,
            "date": date,
            "total": total,
            "line_items": line_items,
        }


if __name__ == "__main__":
    # Example usage with a local file (placeholder)
    with open("sample_invoice.png", "rb") as f:
        result = InvoiceExtractor().extract(f.read())
        print(result)
