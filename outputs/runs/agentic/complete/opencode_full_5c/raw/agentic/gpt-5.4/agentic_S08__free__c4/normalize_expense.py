from __future__ import annotations

from typing import Any, Dict

from document_models import (
    NormalizedExpenseRecord,
    coerce_float,
    field_value,
    normalize_confidence_map,
)


def normalize_expense(extraction_result: Dict[str, Any]) -> Dict[str, Any]:
    fields = extraction_result.get("fields", {})
    document_type = extraction_result.get("document_type", "unknown")
    vendor = field_value(fields, "vendor")
    merchant = field_value(fields, "merchant")
    tax = coerce_float(field_value(fields, "tax"))
    total = coerce_float(field_value(fields, "total"))
    subtotal = total - tax if total is not None and tax is not None else None
    record = NormalizedExpenseRecord(
        record_type="expense",
        vendor=vendor,
        merchant=merchant,
        document_date=field_value(fields, "date"),
        currency="USD",
        subtotal=subtotal,
        tax=tax,
        total=total,
        items=extraction_result.get("line_items", []),
        source_document_type=document_type,
        provider=extraction_result.get("provider", "google_document_ai"),
        confidence_summary=normalize_confidence_map(fields),
    )
    return record.to_dict()
