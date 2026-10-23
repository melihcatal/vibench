from document_models import normalize_currency, normalize_items


def normalize_expense(extracted):
    return {
        "vendor": extracted.get("vendor") or extracted.get("merchant"),
        "date": extracted.get("date"),
        "total": normalize_currency(extracted.get("total")),
        "tax": normalize_currency(extracted.get("tax")),
        "items": normalize_items(
            extracted.get("line_items") or extracted.get("items") or []
        ),
    }
