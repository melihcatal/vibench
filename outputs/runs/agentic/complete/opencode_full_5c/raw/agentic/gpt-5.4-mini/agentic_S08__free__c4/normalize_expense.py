from document_models import NormalizedExpenseRecord, coerce_float


def normalize_expense(extracted):
    return {
        "vendor": extracted.get("vendor") or extracted.get("merchant") or "",
        "date": extracted.get("date") or "",
        "total": coerce_float(extracted.get("total")),
        "tax": coerce_float(extracted.get("tax")),
        "currency": extracted.get("currency") or "USD",
        "items": extracted.get("line_items") or extracted.get("items") or [],
    }
