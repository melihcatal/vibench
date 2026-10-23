from __future__ import annotations

from typing import Any, Dict

from document_models import NormalizedExpenseRecord, StructuredDocumentExtractionResponse, normalize_line_item


def normalize_expense(extracted: StructuredDocumentExtractionResponse, document_type: str) -> Dict[str, Any]:
    record = NormalizedExpenseRecord(
        document_type=document_type,
        vendor=extracted.vendor,
        merchant=extracted.merchant,
        date=extracted.date,
        total=extracted.total,
        tax=extracted.tax,
        line_items=[normalize_line_item(item) for item in extracted.line_items] + [normalize_line_item(item) for item in extracted.items],
        source_confidence=extracted.confidence,
        metadata={"has_notes": bool(extracted.notes)},
    )
    return record.to_dict()
