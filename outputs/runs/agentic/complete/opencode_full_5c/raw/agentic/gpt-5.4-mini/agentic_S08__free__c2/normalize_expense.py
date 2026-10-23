from typing import Any, Dict, List

from document_models import NormalizedExpenseRecord


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    fields = extracted.get("fields", {})
    record = NormalizedExpenseRecord(
        vendor=str(
            fields.get("vendor", {}).get(
                "value", fields.get("merchant", {}).get("value", "")
            )
        ),
        transaction_date=str(fields.get("date", {}).get("value", "")),
        currency=str(fields.get("currency", {}).get("value", "USD")),
        total_amount=float(
            fields.get("total", {}).get(
                "value", fields.get("amount", {}).get("value", 0.0) or 0.0
            )
        ),
        tax_amount=float(fields.get("tax", {}).get("value", 0.0) or 0.0),
        line_items=list(
            fields.get("line_items", {}).get("value", [])
            or fields.get("items", {}).get("value", [])
        ),
        source_document_id=str(extracted.get("document_id", "")) or None,
    )
    return record.__dict__
