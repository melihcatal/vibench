from document_models import normalize_fields, normalize_items


def normalize_expense(extracted: dict):
    data = extracted.get("invoice") or extracted.get("receipt") or extracted
    return normalize_fields(
        {
            "merchant": data.get("vendor") or data.get("merchant"),
            "date": data.get("date"),
            "total": data.get("total"),
            "tax": data.get("tax"),
            "items": normalize_items(data.get("items", [])),
            "source_provider": extracted.get("provider") or data.get("provider"),
        }
    )
