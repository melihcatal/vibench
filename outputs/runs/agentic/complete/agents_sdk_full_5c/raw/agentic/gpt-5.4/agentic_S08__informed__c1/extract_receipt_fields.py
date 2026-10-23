from __future__ import annotations

from typing import Any, Dict, List

from document_client import AzureDocumentExtractionClient, currency_value, field_confidence, parse_kv_fields
from document_models import ExtractedDocument, LineItem, iso_date_or_none


MODEL_ID = "prebuilt-invoice"



def extract_receipt_fields(document_bytes: bytes) -> Dict[str, Any]:
    client = AzureDocumentExtractionClient(model_id=MODEL_ID)
    result = client.analyze_document_bytes(document_bytes, model_id=MODEL_ID)
    fields = parse_kv_fields(result)

    items: List[LineItem] = []
    items_field = fields.get("Items")
    for item in getattr(items_field, "value_array", []) or []:
        obj = getattr(item, "value_object", {}) or {}
        items.append(
            LineItem(
                description=getattr(obj.get("Description"), "content", "") if obj.get("Description") else "",
                quantity=getattr(obj.get("Quantity"), "value_number", None) if obj.get("Quantity") else None,
                amount=currency_value(obj.get("Amount")) if obj.get("Amount") else None,
                confidence=min(
                    [c for c in [field_confidence(obj.get("Description")), field_confidence(obj.get("Amount"))] if c is not None],
                    default=None,
                ),
            )
        )

    extracted = ExtractedDocument(
        document_type="receipt",
        merchant=getattr(fields.get("VendorName"), "content", None),
        invoice_date=iso_date_or_none(getattr(fields.get("InvoiceDate"), "value_date", None) or getattr(fields.get("TransactionDate"), "value_date", None)),
        tax=currency_value(fields.get("TotalTax")),
        total=currency_value(fields.get("InvoiceTotal")),
        currency=getattr(getattr(fields.get("InvoiceTotal"), "value_currency", None), "currency_code", None),
        items=items,
        notes=getattr(fields.get("MerchantAddress"), "content", None),
        raw_fields={key: getattr(value, "content", None) for key, value in fields.items()},
        confidence={
            "merchant": field_confidence(fields.get("VendorName")) or 0.0,
            "tax": field_confidence(fields.get("TotalTax")) or 0.0,
            "total": field_confidence(fields.get("InvoiceTotal")) or 0.0,
            "items": field_confidence(items_field) or 0.0,
        },
    )
    return extracted.to_dict()
