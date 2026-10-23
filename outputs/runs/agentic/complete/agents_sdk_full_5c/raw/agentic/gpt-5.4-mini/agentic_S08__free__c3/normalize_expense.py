from typing import Any, Dict

from document_models import ExpenseRecord, normalize_amount


NORMALIZATION_PROVIDER = "google.cloud.documentai.v1.DocumentProcessorServiceClient"


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    record = ExpenseRecord(
        source_type=extracted.get("source_type", "invoice"),
        vendor=extracted.get("vendor") or extracted.get("merchant") or "",
        transaction_date=None,
        total=normalize_amount(extracted.get("total")) or 0.0,
        tax=normalize_amount(extracted.get("tax")),
        items=extracted.get("line_items") or extracted.get("items") or [],
    )
    return {
        "source_type": record.source_type,
        "vendor": record.vendor,
        "transaction_date": record.transaction_date.isoformat() if record.transaction_date else None,
        "total": record.total,
        "tax": record.tax,
        "currency": record.currency,
        "items": record.items,
        "provider": NORMALIZATION_PROVIDER,
    }
