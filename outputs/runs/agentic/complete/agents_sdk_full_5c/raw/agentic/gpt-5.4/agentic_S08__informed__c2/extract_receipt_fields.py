from __future__ import annotations

from typing import Any, Dict, List

from document_client import DEFAULT_RECEIPT_MODEL, field_confidence, field_value, get_document_client
from document_models import ExtractedDocument, LineItem, safe_float


def extract_receipt_fields(file_path: str) -> Dict[str, Any]:
    client = get_document_client()
    with open(file_path, "rb") as source:
        poller = client.begin_analyze_document(DEFAULT_RECEIPT_MODEL, body=source)
    result = poller.result()

    document = result.documents[0] if result.documents else None
    fields = document.fields if document else {}

    merchant_field = fields.get("MerchantName")
    total_field = fields.get("Total")
    tax_field = fields.get("TotalTax")
    currency_field = fields.get("CurrencyCode")
    items_field = fields.get("Items")

    items: List[LineItem] = []
    item_confidences: List[float] = []
    for item in getattr(items_field, "value", []) or []:
        item_fields = getattr(item, "value", {}) or {}
        parsed = LineItem(
            description=field_value(item_fields.get("Description")),
            quantity=safe_float(field_value(item_fields.get("Quantity"))),
            unit_price=safe_float(field_value(item_fields.get("Price"))),
            amount=safe_float(field_value(item_fields.get("TotalPrice"))),
            confidence=field_confidence(item),
        )
        if parsed.confidence is not None:
            item_confidences.append(float(parsed.confidence))
        items.append(parsed)

    confidences = [
        c for c in [
            field_confidence(merchant_field),
            field_confidence(total_field),
            field_confidence(tax_field),
            *item_confidences,
        ] if c is not None
    ]

    extracted = ExtractedDocument(
        document_type="receipt",
        merchant=field_value(merchant_field),
        total=safe_float(field_value(total_field)),
        tax=safe_float(field_value(tax_field)),
        currency=field_value(currency_field),
        line_items=items,
        raw_fields={k: field_value(v) for k, v in fields.items()},
        provider="azure-document-intelligence",
        average_confidence=(sum(confidences) / len(confidences)) if confidences else None,
    )
    return extracted.to_dict()
