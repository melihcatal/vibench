from __future__ import annotations

from typing import Any, Dict

from document_models import NormalizedExpense, coerce_float, ensure_text, normalize_line_items


def normalize_expense(extracted: Dict[str, Any], source: str = "") -> Dict[str, Any]:
    vendor = ensure_text(extracted.get("vendor") or extracted.get("merchant"))
    document_date = ensure_text(extracted.get("date") or extracted.get("document_date"))
    total = coerce_float(extracted.get("total"))
    tax = extracted.get("tax")
    items = normalize_line_items(extracted.get("items"))
    normalized = NormalizedExpense(
        vendor=vendor,
        document_date=document_date,
        total=total,
        currency=ensure_text(extracted.get("currency") or "USD") or "USD",
        items=items,
        tax=coerce_float(tax) if tax is not None else None,
        notes=ensure_text(extracted.get("notes") or extracted.get("memo")) or None,
        source=source,
    )
    return normalized.to_dict()
