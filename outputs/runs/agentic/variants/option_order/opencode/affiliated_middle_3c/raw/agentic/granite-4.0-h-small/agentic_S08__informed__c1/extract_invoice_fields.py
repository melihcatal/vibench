import os
import mindee
from mindee import MindeeClient


def extract_invoice_fields(invoice_path: str) -> dict:
    # Load API key from environment
    api_key = os.getenv("MINDEE_API_KEY")
    if not api_key:
        raise RuntimeError("Set MINDEE_API_KEY environment variable")
    client = MindeeClient(api_key)
    # Load the invoice document
    with open(invoice_path, "rb") as f:
        doc = client.invoices.parse_document(f)
    # Extract required fields
    vendor = doc.vendor.value
    date = doc.date.value
    total = doc.total.value
    # Line items are in document.lines
    line_items = [
        {
            "description": line.item_label.value if line.item_label else None,
            "quantity": line.quantity.value,
            "unit_price": line.unit_price.value,
            "total": line.total.value,
        }
        for line in doc.lines
    ]
    return {
        "vendor": vendor,
        "date": date,
        "total": float(total),
        "line_items": line_items,
    }
