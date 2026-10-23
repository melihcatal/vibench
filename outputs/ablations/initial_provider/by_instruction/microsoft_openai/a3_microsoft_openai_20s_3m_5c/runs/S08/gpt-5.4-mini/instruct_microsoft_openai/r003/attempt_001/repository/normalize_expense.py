from document_models import normalize_items, normalize_money


def normalize_expense(extracted):
    return {
        "merchant": extracted.get("vendor") or extracted.get("merchant"),
        "date": extracted.get("date"),
        "total": normalize_money(extracted.get("total")),
        "tax": normalize_money(extracted.get("tax")),
        "currency": extracted.get("currency"),
        "items": normalize_items(extracted.get("line_items") or extracted.get("items")),
    }
