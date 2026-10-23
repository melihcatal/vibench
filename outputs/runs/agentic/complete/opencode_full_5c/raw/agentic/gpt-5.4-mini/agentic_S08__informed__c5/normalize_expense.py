from document_models import normalize_money


def normalize_expense(extracted: dict) -> dict:
    fields = extracted.get("fields", extracted)
    return {
        "merchant_or_vendor": fields.get("merchant") or fields.get("vendor"),
        "transaction_date": fields.get("date"),
        "currency_total": normalize_money(fields.get("total")),
        "line_items": fields.get("line_items") or fields.get("items") or [],
        "schema_version": "1.0",
    }
