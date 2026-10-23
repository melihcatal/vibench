from document_models import NormalizedExpense, normalize_currency_amount


def normalize_expense(extracted: dict) -> dict:
    return NormalizedExpense(
        vendor=extracted.get("vendor") or extracted.get("merchant"),
        date=extracted.get("date"),
        total=normalize_currency_amount(extracted.get("total")),
        currency=extracted.get("currency", "USD"),
        items=extracted.get("line_items") or extracted.get("items") or [],
        confidence=float(extracted.get("confidence", 0.0)),
    ).__dict__
