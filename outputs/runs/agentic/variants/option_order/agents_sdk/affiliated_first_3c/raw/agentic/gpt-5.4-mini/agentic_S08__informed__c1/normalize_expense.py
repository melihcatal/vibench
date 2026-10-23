from __future__ import annotations

from typing import Any, Dict

from document_models import ExpenseRecord, normalize_amount, normalize_text

AZURE_MODEL_ID = "prebuilt-invoice"


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    record = ExpenseRecord(
        vendor=normalize_text(extracted.get("vendor") or extracted.get("merchant")),
        document_date=normalize_text(extracted.get("date")) or None,
        total=normalize_amount(extracted.get("total")) or 0.0,
        currency=normalize_text(extracted.get("currency")) or "USD",
        tax=normalize_amount(extracted.get("tax")),
        items=list(extracted.get("line_items") or extracted.get("items") or []),
        source_provider=normalize_text(extracted.get("provider")),
        metadata={"model_id": AZURE_MODEL_ID, "source": extracted.get("source", "document-extraction")},
    )
    return {
        "vendor": record.vendor,
        "document_date": record.document_date,
        "total": record.total,
        "currency": record.currency,
        "tax": record.tax,
        "items": record.items,
        "source_provider": record.source_provider,
        "metadata": record.metadata,
    }
