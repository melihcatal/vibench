import os
from typing import Dict, Any

# Provider – using Azure Form Recognizer for invoice summarization
AZURE_FORM_RECOGNIZER_ENDPOINT = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
AZURE_FORM_RECOGNIZER_KEY = os.getenv("AZURE_FORM_RECOGNIZER_KEY")


def summarize_invoice(extracted: Dict[str, Any]) -> Dict[str, Any]:
    """Create a concise human‑readable summary for an invoice.","""
    # Example: re‑format the normalized fields into a short string
    lines = [
        f"Vendor: {extracted['merchant_or_vendor']}",
        f"Date: {extracted['date']}",
        f"Total: ${extracted['total_amount']:.2f}",
    ]
    items_lines = [
        f" - {item['description_or_name']} x{item['quantity']} @ ${item['unit_price']:.2f}"
        for item in extracted["items"]
    ]
    lines.extend(items_lines)
    summary = "\n".join(lines)
    return {"summary": summary}
