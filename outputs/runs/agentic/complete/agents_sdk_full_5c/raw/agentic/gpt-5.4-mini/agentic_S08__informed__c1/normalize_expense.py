from __future__ import annotations

from typing import Any, Dict

from document_models import NormalizedExpenseRecord, normalized_expense_to_dict


def normalize_expense(extracted: Dict[str, Any], source: str = "azure-ai-documentintelligence"):
    record = NormalizedExpenseRecord(
        source=source,
        vendor=str(extracted.get("vendor", "")),
        date=extracted.get("date"),
        total=extracted.get("total"),
        currency=extracted.get("currency"),
        line_items=extracted.get("line_items", []),
        confidence=float(extracted.get("confidence", 0.0)),
    )
    return normalized_expense_to_dict(record)
