from __future__ import annotations

from document_models import build_expense_record, normalize_date, parse_float


def normalize_expense(extracted_payload: dict, document_type: str) -> dict:
    if document_type == "invoice":
        supplier_name = (extracted_payload.get("vendor") or {}).get("value")
        document_date = normalize_date(
            (extracted_payload.get("invoice_date") or {}).get("value")
        )
        total_amount = parse_float((extracted_payload.get("total") or {}).get("value"))
        tax_amount = None
        line_items = extracted_payload.get("line_items", [])
    else:
        supplier_name = (extracted_payload.get("merchant") or {}).get("value")
        document_date = normalize_date(
            (extracted_payload.get("date") or {}).get("value")
        )
        total_amount = parse_float((extracted_payload.get("total") or {}).get("value"))
        tax_amount = parse_float((extracted_payload.get("tax") or {}).get("value"))
        line_items = extracted_payload.get("items", [])

    currency = (extracted_payload.get("currency") or {}).get("value")
    normalized_items = [
        {
            "description": item.get("description"),
            "quantity": parse_float(item.get("quantity")),
            "unit_price": parse_float(item.get("unit_price")),
            "amount": parse_float(item.get("amount")),
            "tax": parse_float(item.get("tax")),
            "confidence": item.get("confidence"),
        }
        for item in line_items
    ]

    return build_expense_record(
        document_type=document_type,
        supplier_name=supplier_name,
        document_date=document_date,
        total_amount=total_amount,
        tax_amount=tax_amount,
        currency=currency,
        line_items=normalized_items,
        source_payload=extracted_payload,
    )
