from __future__ import annotations

from typing import Any, Dict

from document_models import NormalizedExpense


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    doc = extracted.get("document")
    normalized = NormalizedExpense(
        source_type=getattr(doc, "document_type", "unknown"),
        counterparty=getattr(doc, "vendor", None) or getattr(doc, "merchant", None),
        transaction_date=getattr(doc, "date", None),
        total_amount=getattr(doc, "total", None),
        tax_amount=getattr(doc, "tax", None),
        currency=getattr(doc, "currency", None),
        line_items=[item.__dict__ for item in getattr(doc, "items", [])],
        memo=getattr(doc, "notes", None),
    )
    return {"normalized": normalized, "schema": "standard.expense.v1"}
