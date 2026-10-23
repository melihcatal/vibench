# [LATER-STEP] invoice_summary.py

# Summarizes extracted invoice fields for reporting
import json
from normalize_expense import NormalizedExpense


def summarize_invoice(extracted: dict) -> str:
    """Create a human‑readable summary string from raw invoice extraction output."""
    # Assume `extracted` follows the shape from extract_invoice_fields
    vendor = extracted.get("vendor", "Unknown vendor")
    date = extracted.get("date", "Unknown date")
    total = extracted.get("total", "0.00")
    items = extracted.get("line_items", [])
    if items:
        items_summary = ", ".join(items)
    else:
        items_summary = "No line items"
    return f"Vendor: {vendor}\nDate: {date}\nTotal: ${total}\nItems:\n  {items_summary}"
