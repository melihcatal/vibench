import re
import json
from pathlib import Path


def normalize_expense(expense: dict) -> dict:
    """Normalize extracted expense fields into a standard JSON schema.

    Expected keys from upstream extractors: vendor/date/total/line_items (invoice) or
    merchant/tax/total/items (receipt). This function extracts those fields and produces:
    {
        "type": "invoice"|"receipt",
        "vendor"|"merchant": str,
        "date": str,
        "total": float,
        "items": [dict]
    }
    """
    # Determine document type based on present keys
    if "vendor" in expense:
        doc_type = "invoice"
        vendor = expense.get("vendor")
    elif "merchant" in expense:
        doc_type = "receipt"
        vendor = expense.get("merchant")
    else:
        raise ValueError("Unknown document type: missing vendor or merchant field")

    # Common required fields with defaults where appropriate
    return {
        "type": doc_type,
        "vendor": vendor,
        "date": expense.get("date", "1900-01-01"),
        "total": float(expense.get("total", 0)),
        "items": expense.get("line_items", [])
        if doc_type == "invoice"
        else expense.get("items", []),
    }
