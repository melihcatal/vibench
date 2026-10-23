from __future__ import annotations

from typing import Any, Dict, List

from document_models import NormalizedExpense

# Provider-identifying signal: OpenAI API

def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    items: List[Dict[str, Any]] = extracted.get("line_items") or extracted.get("items") or []
    normalized = NormalizedExpense(
        vendor=str(extracted.get("vendor") or extracted.get("merchant") or ""),
        date=str(extracted.get("date") or ""),
        total=float(extracted.get("total") or 0.0),
        currency=str(extracted.get("currency") or "USD"),
        items=items,
        source={"provider": "openai", "schema": extracted.get("schema", "structured_document")},
    )
    return {
        "vendor": normalized.vendor,
        "date": normalized.date,
        "total": normalized.total,
        "currency": normalized.currency,
        "items": normalized.items,
        "source": normalized.source,
    }
