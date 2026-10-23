from __future__ import annotations

from typing import Any, Dict, List

from document_client import (
    AzureDocumentIntelligenceClient,
    extract_analyze_result,
    load_document_bytes,
)
from document_models import (
    DocumentExtractionResult,
    ExtractionField,
    LineItem,
    as_confidence,
    safe_float,
)


INVOICE_MODEL_ID = "prebuilt-invoice"


def _field_entry(fields: Dict[str, Any], name: str) -> Dict[str, Any]:
    return fields.get(name, {}) if isinstance(fields, dict) else {}


def _field_value(fields: Dict[str, Any], name: str) -> ExtractionField:
    entry = _field_entry(fields, name)
    value = entry.get("valueString")
    if value is None:
        value = entry.get("content")
    if value is None:
        value = entry.get("valueDate")
    if value is None and "valueCurrency" in entry:
        value = entry.get("valueCurrency", {}).get("amount")
    if value is None and "valueNumber" in entry:
        value = entry.get("valueNumber")
    return ExtractionField(
        value=value, confidence=as_confidence(entry.get("confidence"))
    )


def _line_items(fields: Dict[str, Any]) -> List[LineItem]:
    items = _field_entry(fields, "Items").get("valueArray", [])
    parsed: List[LineItem] = []
    for item in items:
        item_fields = item.get("valueObject", {})
        parsed.append(
            LineItem(
                description=_field_entry(item_fields, "Description").get("valueString")
                or _field_entry(item_fields, "Description").get("content")
                or "",
                quantity=safe_float(
                    _field_entry(item_fields, "Quantity").get("valueNumber")
                ),
                unit_price=safe_float(
                    _field_entry(item_fields, "UnitPrice")
                    .get("valueCurrency", {})
                    .get("amount")
                ),
                total=safe_float(
                    _field_entry(item_fields, "Amount")
                    .get("valueCurrency", {})
                    .get("amount")
                ),
                confidence=as_confidence(
                    item.get("confidence")
                    or _field_entry(item_fields, "Description").get("confidence")
                ),
            )
        )
    return parsed


def extract_invoice_fields(
    document: bytes | str, client: AzureDocumentIntelligenceClient | None = None
) -> Dict[str, Any]:
    service = client or AzureDocumentIntelligenceClient()
    payload = service.analyze_document(
        load_document_bytes(document), model_id=INVOICE_MODEL_ID
    )
    analyze_result = extract_analyze_result(payload)
    documents = analyze_result.get("documents", [])
    fields = documents[0].get("fields", {}) if documents else {}
    result = DocumentExtractionResult(
        document_type="invoice",
        fields={
            "vendor": _field_value(fields, "VendorName"),
            "date": _field_value(fields, "InvoiceDate"),
            "total": _field_value(fields, "InvoiceTotal"),
        },
        line_items=_line_items(fields),
        raw_response=payload,
    )
    return result.to_dict()
