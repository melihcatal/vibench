from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import analyze_invoice_document, read_binary
from document_models import ExtractedDocument, as_document_dict, field_value, line_item


def _field_content(field: Any) -> Any:
    if field is None:
        return None
    value = getattr(field, "value", None)
    if value is not None:
        return value
    return getattr(field, "content", None)


def _field_confidence(field: Any, default: float = 0.0) -> float:
    if field is None:
        return default
    return float(getattr(field, "confidence", default) or default)


def _extract_items(document: Any) -> List[Any]:
    fields = getattr(document, "fields", {}) or {}
    items_field = fields.get("Items")
    values = getattr(items_field, "value_array", None) or []
    parsed = []
    for entry in values:
        entry_fields = getattr(entry, "value_object", {}) or {}
        parsed.append(
            line_item(
                description=_field_content(entry_fields.get("Description")),
                quantity=_field_content(entry_fields.get("Quantity")),
                unit_price=_field_content(entry_fields.get("UnitPrice")),
                amount=_field_content(entry_fields.get("Amount")),
                confidence=max(
                    _field_confidence(entry_fields.get("Description")),
                    _field_confidence(entry_fields.get("Amount")),
                ),
            )
        )
    return parsed


def extract_invoice_fields(file_path: str) -> Dict[str, Any]:
    result = analyze_invoice_document(read_binary(file_path))
    document = result.documents[0]
    fields = document.fields
    extracted = ExtractedDocument(
        document_type="invoice",
        source_provider="azure_document_intelligence",
        source_model="prebuilt-invoice",
        vendor=field_value(
            _field_content(fields.get("VendorName")),
            _field_confidence(fields.get("VendorName")),
        ),
        date=field_value(
            _field_content(fields.get("InvoiceDate")),
            _field_confidence(fields.get("InvoiceDate")),
        ),
        total=field_value(
            _field_content(fields.get("InvoiceTotal")),
            _field_confidence(fields.get("InvoiceTotal")),
        ),
        items=_extract_items(document),
        raw={"content": getattr(result, "content", None)},
    )
    return as_document_dict(extracted)
