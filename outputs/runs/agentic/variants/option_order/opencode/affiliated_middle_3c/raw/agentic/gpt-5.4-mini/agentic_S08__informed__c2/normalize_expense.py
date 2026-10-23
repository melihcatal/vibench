from document_models import normalize_document_result


def normalize_expense(extracted):
    data = normalize_document_result(extracted)
    return {
        "party": data.get("vendor"),
        "date": data.get("date"),
        "amount": data.get("total"),
        "tax": data.get("tax"),
        "currency": data.get("currency"),
        "notes": data.get("notes"),
        "items": data.get("items"),
        "confidence": data.get("confidence"),
    }
