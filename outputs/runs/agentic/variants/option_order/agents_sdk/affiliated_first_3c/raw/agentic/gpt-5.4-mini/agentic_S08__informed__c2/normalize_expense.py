from __future__ import annotations

from typing import Any, Dict

from document_models import NormalizedExpense


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    expense = NormalizedExpense(
        vendor=extracted.get("vendor") or extracted.get("merchant") or "",
        date=extracted.get("date"),
        total=_float_or_none(extracted.get("total")),
        currency=extracted.get("currency"),
        tax=_float_or_none(extracted.get("tax")),
        items=extracted.get("items") or extracted.get("line_items") or [],
        invoice_number=extracted.get("invoice_number"),
        confidence=_float_or_none(extracted.get("confidence")),
    )
    return expense.to_json()


def _float_or_none(value: Any):
    try:
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None
