from document_models import normalize_confidence, standardize_items


def normalize_expense(data):
    normalized = dict(data)
    if "confidence" in normalized:
        normalized["confidence"] = normalize_confidence(normalized["confidence"])
    if "items" in normalized:
        normalized["items"] = standardize_items(normalized["items"])
    if "line_items" in normalized:
        normalized["line_items"] = standardize_items(normalized["line_items"])
    return normalized
