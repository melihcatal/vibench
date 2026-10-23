import os
import mindee
from mindee import MindeeClient


def extract_receipt_fields(receipt_path: str) -> dict:
    api_key = os.getenv("MINDEE_API_KEY")
    if not api_key:
        raise RuntimeError("Set MINDEE_API_KEY environment variable")
    client = MindeeClient(api_key)
    with open(receipt_path, "rb") as f:
        doc = client.receipts.parse_document(f)
    merchant = doc.merchant.value
    date = doc.date.value
    total = doc.total.value
    items = [
        {
            "name": line.item_label.value,
            "price": line.amount.value,
            "quantity": line.quantity.value,
        }
        for line in doc.lines
    ]
    return {
        "merchant": merchant,
        "date": date,
        "total": float(total),
        "items": items,
    }
