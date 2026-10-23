from __future__ import annotations

from typing import Any, Dict, List

from document_client import DEFAULT_INVOICE_MODEL, field_confidence, field_value, get_document_client, read_bytes
from document_models import ExtractedDocument, LineItem, safe_float


def extract_invoice_fields(file_path: str) -> Dict[str, Any]:
    client = get_document_client()
    with open(file_path, "rb") as source:
        poller = client.begin_analyze_document(DEFAULT_INVOICE_MODEL, body=source)
    result = poller.result()

    document = result.documents[0] if result.documents else None
    fields = document.fields if document else {}

    vendor_field = fields.get("VendorName")
    date_field = fields.get("InvoiceDate")
    total_field = fields.get("InvoiceTotal")
    currency_field = fields.get("CurrencyCode")
    items_field = fields.get("Items")

    line_items: List[LineItem] = []
    item_confidences: List[float] = []
    for item in getattr(items_field, "value", []) or []:
        item_fields = getattr(item, "value", {}) or {}
        line = LineItem(
            description=field_value(item_fields.get("Description")),
            quantity=safe_float(field_value(item_fields.get("Quantity"))),
            unit_price=safe_float(field_value(item_fields.get("UnitPrice"))),
            amount=safe_float(field_value(item_fields.get("Amount"))),
            confidence=field_confidence(item),
        )
        if line.confidence is not None:
            item_confidences.append(float(line.confidence))
        line_items.append(line)

    confidences = [
        c for c in [
            field_confidence(vendor_field),
            field_confidence(date_field),
            field_confidence(total_field),
            *item_confidences,
        ] if c is not None
    ]

    extracted = ExtractedDocument(
        document_type="invoice",
        vendor=field_value(vendor_field),
        invoice_date=str(field_value(date_field)) if field_value(date_field) is not None else None,
        total=safe_float(field_value(total_field)),
        currency=field_value(currency_field),
        line_items=line_items,
        raw_fields={k: field_value(v) for k, v in fields.items()},
        provider="azure-document-intelligence",
        average_confidence=(sum(confidences) / len(confidences)) if confidences else None,
    )
    return extracted.to_dict()
