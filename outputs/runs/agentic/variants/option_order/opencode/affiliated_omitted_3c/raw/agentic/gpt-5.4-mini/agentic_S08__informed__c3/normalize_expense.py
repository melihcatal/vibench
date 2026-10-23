from document_models import normalize_field_map


def normalize_expense(extracted: dict):
    payload = normalize_field_map(extracted)
    return {
        "document_type": payload.get("document_type", "expense"),
        "merchant": payload.get("merchant") or payload.get("vendor"),
        "date": payload.get("date"),
        "total": payload.get("total"),
        "tax": payload.get("tax"),
        "items": payload.get("items") or payload.get("line_items") or [],
    }
