from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import create_document_intelligence_client, load_document_bytes
from document_models import ExtractedDocument, FieldValue, LineItem


AZURE_RECEIPT_MODEL_ID = "prebuilt-receipt"


def _get_field(document: Any, key: str) -> Optional[Any]:
    if not getattr(document, "fields", None):
        return None
    return document.fields.get(key)


def _field_value(field: Any) -> FieldValue:
    if field is None:
        return FieldValue(value=None, confidence=0.0)
    value = getattr(field, "value_string", None)
    if value is None:
        value = getattr(field, "value_date", None)
    if value is None:
        value = getattr(field, "value_number", None)
    if value is None:
        value = getattr(field, "value_currency", None)
        if value is not None:
            value = getattr(value, "amount", None)
    if value is None:
        value = getattr(field, "content", None)
    return FieldValue(
        value=value, confidence=float(getattr(field, "confidence", 0.0) or 0.0)
    )


def _extract_items(items_field: Any) -> List[LineItem]:
    items: List[LineItem] = []
    if items_field is None:
        return items
    for entry in getattr(items_field, "value_array", []) or []:
        values = getattr(entry, "value_object", {}) or {}
        description_field = values.get("Description")
        quantity_field = values.get("Quantity")
        unit_price_field = values.get("Price")
        total_price_field = values.get("TotalPrice")
        unit_price = getattr(
            getattr(unit_price_field, "value_currency", None), "amount", None
        )
        total_price = getattr(
            getattr(total_price_field, "value_currency", None), "amount", None
        )
        quantity = getattr(quantity_field, "value_number", None)
        description = getattr(description_field, "value_string", None) or getattr(
            description_field, "content", ""
        )
        confidences = [
            float(getattr(f, "confidence", 0.0) or 0.0)
            for f in [
                description_field,
                quantity_field,
                unit_price_field,
                total_price_field,
            ]
            if f is not None
        ]
        items.append(
            LineItem(
                description=description or "",
                quantity=quantity,
                unit_price=unit_price,
                amount=total_price,
                confidence=sum(confidences) / len(confidences) if confidences else 0.0,
            )
        )
    return items


def extract_receipt_fields(file_path: str) -> Dict[str, Any]:
    client = create_document_intelligence_client()
    poller = client.begin_analyze_document(
        AZURE_RECEIPT_MODEL_ID, body=load_document_bytes(file_path)
    )
    result = poller.result()
    receipt = result.documents[0] if result.documents else None
    extracted = ExtractedDocument(document_type="receipt", source_uri=file_path)
    extracted.fields = {
        "merchant": _field_value(_get_field(receipt, "MerchantName")),
        "date": _field_value(_get_field(receipt, "TransactionDate")),
        "tax": _field_value(_get_field(receipt, "TotalTax")),
        "total": _field_value(_get_field(receipt, "Total")),
        "currency": _field_value(_get_field(receipt, "Total")),
    }
    extracted.items = _extract_items(_get_field(receipt, "Items"))
    response = extracted.to_dict()
    response["provider"] = "azure-document-intelligence"
    response["model_id"] = AZURE_RECEIPT_MODEL_ID
    return response
