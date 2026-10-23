from __future__ import annotations

from typing import Any, Dict

from document_models import NormalizedExpenseRecord


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    record = NormalizedExpenseRecord(
        source=extracted.get("source", "document_ai"),
        vendor=extracted.get("vendor") or extracted.get("merchant"),
        transaction_date=extracted.get("date"),
        total=extracted.get("total"),
        tax=extracted.get("tax"),
        currency=extracted.get("currency"),
        items=extracted.get("line_items") or extracted.get("items") or [],
        metadata={k: v for k, v in extracted.items() if k not in {"vendor", "merchant", "date", "total", "tax", "currency", "line_items", "items"}},
    )
    return record.to_dict()
