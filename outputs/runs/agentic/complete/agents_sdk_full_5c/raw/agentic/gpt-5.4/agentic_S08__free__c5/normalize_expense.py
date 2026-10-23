from __future__ import annotations

from typing import Any, Dict

from document_models import NormalizedExpenseRecord, coerce_float, normalize_date



def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    document_type = extracted.get("document_type")
    supplier_name = None
    if extracted.get("vendor"):
        supplier_name = extracted["vendor"].get("value")
    if not supplier_name and extracted.get("merchant"):
        supplier_name = extracted["merchant"].get("value")

    items = []
    for item in extracted.get("line_items", []):
        items.append(
            {
                "description": item.get("description"),
                "quantity": coerce_float(item.get("quantity")),
                "unit_price": coerce_float(item.get("unit_price")),
                "amount": coerce_float(item.get("total")),
                "confidence": float(item.get("confidence", 0.0) or 0.0),
            }
        )

    normalized = NormalizedExpenseRecord(
        record_type="expense",
        source_document_type=document_type,
        supplier_name=supplier_name,
        transaction_date=normalize_date((extracted.get("date") or {}).get("value")),
        total_amount=coerce_float((extracted.get("total") or {}).get("value")),
        tax_amount=coerce_float((extracted.get("tax") or {}).get("value")),
        currency=(extracted.get("currency") or {}).get("value"),
        items=items,
        notes=(extracted.get("notes") or {}).get("value"),
        validation_errors=[],
    )
    return normalized.to_dict()
