from __future__ import annotations

from typing import Any, Dict, List

from document_models import NormalizedExpenseRecord, iso_date, safe_float


def _normalize_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items or []:
        normalized.append(
            {
                "description": item.get("description") or "",
                "quantity": safe_float(item.get("quantity")),
                "unit_price": safe_float(item.get("unit_price")),
                "amount": safe_float(item.get("amount")),
                "confidence": safe_float(item.get("confidence")),
            }
        )
    return normalized


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    supplier_name = extracted.get("vendor") or extracted.get("merchant") or ""
    record = NormalizedExpenseRecord(
        record_type=extracted.get("document_type", "expense"),
        supplier_name=supplier_name,
        document_date=iso_date(extracted.get("invoice_date")),
        totals={
            "subtotal": None,
            "tax": safe_float(extracted.get("tax")),
            "grand_total": safe_float(extracted.get("total")),
        },
        currency=extracted.get("currency"),
        items=_normalize_items(extracted.get("line_items", [])),
        source_document={
            "provider": extracted.get("provider"),
            "raw_fields": extracted.get("raw_fields", {}),
            "notes": extracted.get("notes"),
            "source_confidence": extracted.get("source_confidence", {}),
        },
        validation={},
    )
    return record.to_dict()
