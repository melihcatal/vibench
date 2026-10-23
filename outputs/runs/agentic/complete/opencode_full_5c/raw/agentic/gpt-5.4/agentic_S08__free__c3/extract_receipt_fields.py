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


RECEIPT_MODEL_ID = "prebuilt-receipt"


def _field_entry(fields: Dict[str, Any], name: str) -> Dict[str, Any]:
    return fields.get(name, {}) if isinstance(fields, dict) else {}


def _currency_or_number(entry: Dict[str, Any]) -> Any:
    if "valueCurrency" in entry:
        return entry.get("valueCurrency", {}).get("amount")
    return entry.get("valueNumber") or entry.get("valueString") or entry.get("content")


def _field_value(fields: Dict[str, Any], name: str) -> ExtractionField:
    entry = _field_entry(fields, name)
    return ExtractionField(
        value=_currency_or_number(entry),
        confidence=as_confidence(entry.get("confidence")),
    )


def _items(fields: Dict[str, Any]) -> List[LineItem]:
    source_items = _field_entry(fields, "Items").get("valueArray", [])
    items: List[LineItem] = []
    for item in source_items:
        value_object = item.get("valueObject", {})
        items.append(
            LineItem(
                description=_field_entry(value_object, "Description").get("valueString")
                or _field_entry(value_object, "Description").get("content")
                or "",
                quantity=safe_float(
                    _field_entry(value_object, "Quantity").get("valueNumber")
                ),
                unit_price=safe_float(
                    _field_entry(value_object, "Price")
                    .get("valueCurrency", {})
                    .get("amount")
                ),
                total=safe_float(
                    _field_entry(value_object, "TotalPrice")
                    .get("valueCurrency", {})
                    .get("amount")
                ),
                confidence=as_confidence(
                    item.get("confidence")
                    or _field_entry(value_object, "Description").get("confidence")
                ),
            )
        )
    return items


def extract_receipt_fields(
    document: bytes | str, client: AzureDocumentIntelligenceClient | None = None
) -> Dict[str, Any]:
    service = client or AzureDocumentIntelligenceClient()
    payload = service.analyze_document(
        load_document_bytes(document), model_id=RECEIPT_MODEL_ID
    )
    analyze_result = extract_analyze_result(payload)
    documents = analyze_result.get("documents", [])
    fields = documents[0].get("fields", {}) if documents else {}
    result = DocumentExtractionResult(
        document_type="receipt",
        fields={
            "merchant": _field_value(fields, "MerchantName"),
            "tax": _field_value(fields, "TotalTax"),
            "total": _field_value(fields, "Total"),
        },
        line_items=_items(fields),
        raw_response=payload,
    )
    return result.to_dict()
