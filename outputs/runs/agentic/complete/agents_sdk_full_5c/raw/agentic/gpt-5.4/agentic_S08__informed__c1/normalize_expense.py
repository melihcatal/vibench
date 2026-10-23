from __future__ import annotations

from typing import Any, Dict, List

from azure.ai.documentintelligence import DocumentIntelligenceClient

from document_models import NormalizedExpense, coerce_float, iso_date_or_none, new_record_id



def normalize_expense(extracted: Dict[str, Any]) -> Dict[str, Any]:
    source_type = extracted.get("document_type", "expense")
    supplier_name = extracted.get("vendor") or extracted.get("merchant") or ""
    source_items: List[Dict[str, Any]] = extracted.get("line_items") or extracted.get("items") or []
    normalized_items = [
        {
            "description": item.get("description"),
            "quantity": coerce_float(item.get("quantity")),
            "unit_price": coerce_float(item.get("unit_price")),
            "amount": coerce_float(item.get("amount")),
            "confidence": item.get("confidence"),
        }
        for item in source_items
    ]

    payload = NormalizedExpense(
        record_id=new_record_id(),
        source_type=source_type,
        supplier_name=supplier_name,
        transaction_date=iso_date_or_none(extracted.get("invoice_date")),
        total_amount=coerce_float(extracted.get("total")),
        tax_amount=coerce_float(extracted.get("tax")),
        currency=extracted.get("currency"),
        memo=extracted.get("vendor_notes") or extracted.get("notes"),
        items=normalized_items,
        metadata={
            "provider": "azure-ai-documentintelligence",
            "client_class": DocumentIntelligenceClient.__name__,
            "raw_fields": extracted.get("raw_fields", {}),
            "confidence": extracted.get("confidence", {}),
        },
    )
    return payload.to_dict()
