from typing import Dict
from .document_models import NormalizedExpense

def invoice_summary(extracted: Dict) -> str:
    """
    Generate a concise summary from the normalized expense record.
    Expecting a NormalizedExpense schema (or equivalent dict).
    """
    # Assume the caller has already normalized the data into the expected shape
    total = extracted.get("total", 0)
    vendor = extracted.get("vendor", "Unknown")
    date = extracted.get("date", "--")
    summary = f"Invoice from {vendor} dated {date}, total ${total:.2f}."
    return summary
