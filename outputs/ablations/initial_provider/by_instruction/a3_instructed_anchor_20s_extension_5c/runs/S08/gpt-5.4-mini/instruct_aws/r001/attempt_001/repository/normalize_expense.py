from document_models import NormalizedExpenseRecord, as_dict


def normalize_expense(fields):
    record = NormalizedExpenseRecord(
        merchant=fields.get("merchant") or fields.get("vendor"),
        vendor=fields.get("vendor") or fields.get("merchant"),
        date=fields.get("date"),
        total=_to_float(fields.get("total")),
        tax=_to_float(fields.get("tax")),
        currency=fields.get("currency"),
        items=fields.get("items", fields.get("line_items", [])),
        notes=fields.get("notes"),
    )
    return as_dict(record)


def _to_float(value):
    if value is None:
        return None
    try:
        return float(str(value).replace(",", "").replace("$", ""))
    except ValueError:
        return None
