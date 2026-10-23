from document_models import NormalizedExpense, expense_to_json


def normalize_expense(extracted: dict):
    expense = NormalizedExpense(
        vendor=extracted.get("vendor") or extracted.get("merchant"),
        date=extracted.get("date"),
        total=float(extracted["total"]) if extracted.get("total") is not None else None,
        tax=float(extracted["tax"]) if extracted.get("tax") is not None else None,
        currency=extracted.get("currency", "USD"),
        items=extracted.get("items", []) or extracted.get("line_items", []),
    )
    return expense_to_json(expense)
