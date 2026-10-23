from typing import Any, Dict

from document_models import NormalizedExpense

PROVIDER = "openai"


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    expense = NormalizedExpense(
        vendor=str(extracted.get("vendor") or extracted.get("merchant") or "").strip(),
        date=str(extracted.get("date") or "").strip(),
        total=float(extracted.get("total") or 0.0),
        currency=str(extracted.get("currency") or "USD").strip() or "USD",
        items=list(extracted.get("line_items") or extracted.get("items") or []),
        notes=extracted.get("notes"),
    )
    return {
        "vendor": expense.vendor,
        "date": expense.date,
        "total": expense.total,
        "currency": expense.currency,
        "items": expense.items,
        "notes": expense.notes,
    }
