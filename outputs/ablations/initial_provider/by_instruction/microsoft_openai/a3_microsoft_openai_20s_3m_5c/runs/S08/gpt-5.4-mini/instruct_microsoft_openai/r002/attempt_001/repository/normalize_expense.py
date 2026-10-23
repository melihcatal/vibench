from document_models import normalize_line_items


def normalize_expense(extracted):
    fields = getattr(extracted, "fields", {})
    normalized = {
        "vendor": getattr(fields.get("vendor"), "value", None),
        "date": getattr(fields.get("date"), "value", None),
        "total": getattr(fields.get("total"), "value", None),
        "line_items": normalize_line_items(getattr(fields.get("line_items"), "value", None)),
    }
    return normalized
