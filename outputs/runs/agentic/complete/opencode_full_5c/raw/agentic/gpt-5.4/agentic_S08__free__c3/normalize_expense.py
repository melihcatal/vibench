from __future__ import annotations

from typing import Any, Dict, List

from document_models import NormalizedExpenseRecord, compact_dict, safe_float


def _field_value(extracted: Dict[str, Any], name: str) -> Any:
    return extracted.get("fields", {}).get(name, {}).get("value")


def _line_items(extracted: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = []
    for item in extracted.get("line_items", []):
        items.append(
            compact_dict(
                {
                    "description": item.get("description"),
                    "quantity": safe_float(item.get("quantity")),
                    "unit_price": safe_float(item.get("unit_price")),
                    "total": safe_float(item.get("total")),
                    "confidence": item.get("confidence"),
                }
            )
        )
    return items


def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    source_document_type = extracted.get("document_type", "unknown")
    vendor = _field_value(extracted, "vendor")
    merchant = _field_value(extracted, "merchant")
    tax = safe_float(_field_value(extracted, "tax"))
    total = safe_float(_field_value(extracted, "total"))
    subtotal = None
    if total is not None and tax is not None:
        subtotal = total - tax
    record = NormalizedExpenseRecord(
        source_document_type=source_document_type,
        vendor=vendor,
        merchant=merchant,
        document_date=_field_value(extracted, "date"),
        currency=None,
        subtotal=subtotal,
        tax=tax,
        total=total,
        items=_line_items(extracted),
        notes=_field_value(extracted, "notes"),
        metadata={
            "source_fields": extracted.get("fields", {}),
            "provider": "Azure Document Intelligence",
            "model_hint": extracted.get("document_type"),
        },
    )
    return record.to_dict()
