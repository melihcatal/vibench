from __future__ import annotations

from typing import Any, Dict, List, Optional

from document_client import get_document_intelligence_client
from document_models import ExtractedExpense, extracted_field, line_item_from_values


def _field(result: Any, name: str) -> Optional[Any]:
    fields = getattr(result, "fields", {}) or {}
    return fields.get(name)


def _field_value(field: Any) -> Any:
    if field is None:
        return None
    if getattr(field, "value_currency", None) is not None:
        return field.value_currency.amount
    if getattr(field, "value_date", None) is not None:
        return field.value_date.isoformat()
    if getattr(field, "value_string", None) is not None:
        return field.value_string
    if getattr(field, "value_number", None) is not None:
        return field.value_number
    if getattr(field, "content", None) is not None:
        return field.content
    return None


def _confidence(field: Any) -> Optional[float]:
    return getattr(field, "confidence", None) if field is not None else None


def _parse_items(items_field: Any) -> List[Any]:
    parsed = []
    values = getattr(items_field, "value_array", None) or []
    for item in values:
        item_fields = getattr(item.value_object, "items", lambda: [])()
        mapped = {k: v for k, v in item_fields}
        parsed.append(
            line_item_from_values(
                description=_field_value(mapped.get("Description")),
                quantity=_field_value(mapped.get("Quantity")),
                unit_price=_field_value(mapped.get("Price")),
                amount=_field_value(mapped.get("TotalPrice")),
                confidence=min(
                    [
                        c
                        for c in [
                            _confidence(mapped.get("Description")),
                            _confidence(mapped.get("TotalPrice")),
                        ]
                        if c is not None
                    ],
                    default=None,
                ),
            )
        )
    return parsed


def extract_receipt_fields(
    document_bytes: bytes, mime_type: str = "application/pdf"
) -> Dict[str, Any]:
    client = get_document_intelligence_client()
    poller = client.begin_analyze_document(
        "prebuilt-receipt",
        body=document_bytes,
        content_type=mime_type,
    )
    result = poller.result()
    receipt = result.documents[0]
    merchant = _field(receipt, "MerchantName")
    tax = _field(receipt, "TotalTax")
    total = _field(receipt, "Total")
    items = _parse_items(_field(receipt, "Items"))
    expense = ExtractedExpense(
        document_type="receipt",
        merchant=extracted_field(_field_value(merchant), _confidence(merchant)),
        tax=extracted_field(_field_value(tax), _confidence(tax)),
        total=extracted_field(_field_value(total), _confidence(total)),
        currency=extracted_field(
            getattr(getattr(total, "value_currency", None), "currency_code", None),
            _confidence(total),
        ),
        items=items,
        raw_provider_response=result.as_dict(),
    )
    return {
        "provider": "azure-document-intelligence",
        "model_id": "prebuilt-receipt",
        "expense": expense,
    }
