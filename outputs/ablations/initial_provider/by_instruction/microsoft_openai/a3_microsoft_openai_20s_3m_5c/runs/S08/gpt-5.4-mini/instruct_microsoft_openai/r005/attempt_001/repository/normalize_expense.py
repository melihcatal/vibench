from document_models import normalize_confidence


def normalize_expense(data):
    return {
        "vendor": data.get("vendor") or data.get("merchant"),
        "date": data.get("date"),
        "total": data.get("total"),
        "tax": data.get("tax"),
        "items": data.get("line_items") or data.get("items") or [],
        "confidence": normalize_confidence(data.get("confidence", 0.0)),
    }
