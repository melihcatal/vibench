import json
from normalize_expense import normalize_expense


def summarize_invoice(raw_output):
    """
    Summarize extracted invoice fields into a concise JSON report.
    Uses the normalized expense format from normalize_expense.py.
    """
    normalized = normalize_expense(raw_output)
    # Build a simple summary dict
    summary = {
        "vendor": normalized["vendor_or_merchant"],
        "date": normalized["date"],
        "total": normalized["total"],
        "subtotal": normalized["subtotal"],
        "tax": normalized["tax"],
        "line_items_count": len(normalized["line_items"]),
        "confidence": raw_output.get("confidence"),
    }
    return json.dumps(summary, indent=2)
