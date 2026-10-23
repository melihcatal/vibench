from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import create_document_intelligence_client, load_document_bytes
from document_models import ExtractedDocument, FieldValue, LineItem


AZURE_INVOICE_MODEL_ID = "prebuilt-invoice"


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
        value = getattr(field, "value_currency", None)
        if value is not None:
            value = getattr(value, "amount", None)
    if value is None:
        value = getattr(field, "value_number", None)
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
        amount_field = values.get("Amount")
        unit_price_field = values.get("UnitPrice")
        quantity_field = values.get("Quantity")
        description_field = values.get("Description")
        amount = getattr(getattr(amount_field, "value_currency", None), "amount", None)
        unit_price = getattr(
            getattr(unit_price_field, "value_currency", None), "amount", None
        )
        quantity = getattr(quantity_field, "value_number", None)
        description = getattr(description_field, "value_string", None) or getattr(
            description_field, "content", ""
        )
        confidences = [
            float(getattr(f, "confidence", 0.0) or 0.0)
            for f in [amount_field, unit_price_field, quantity_field, description_field]
            if f is not None
        ]
        items.append(
            LineItem(
                description=description or "",
                quantity=quantity,
                unit_price=unit_price,
                amount=amount,
                confidence=sum(confidences) / len(confidences) if confidences else 0.0,
            )
        )
    return items


def extract_invoice_fields(file_path: str) -> Dict[str, Any]:
    client = create_document_intelligence_client()
    poller = client.begin_analyze_document(
        AZURE_INVOICE_MODEL_ID, body=load_document_bytes(file_path)
    )
    result = poller.result()
    invoice = result.documents[0] if result.documents else None
    extracted = ExtractedDocument(document_type="invoice", source_uri=file_path)
    extracted.fields = {
        "vendor": _field_value(_get_field(invoice, "VendorName")),
        "date": _field_value(_get_field(invoice, "InvoiceDate")),
        "total": _field_value(_get_field(invoice, "InvoiceTotal")),
        "subtotal": _field_value(_get_field(invoice, "SubTotal")),
        "currency": _field_value(_get_field(invoice, "InvoiceTotal")),
    }
    extracted.items = _extract_items(_get_field(invoice, "Items"))
    response = extracted.to_dict()
    response["provider"] = "azure-document-intelligence"
    response["model_id"] = AZURE_INVOICE_MODEL_ID
    return response
