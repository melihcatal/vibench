from __future__ import annotations

from typing import Any, Dict

from document_client import (
    analyze_prebuilt_document,
    extract_line_items,
    field_confidence,
    field_currency_code,
    field_value,
    first_document,
)
from document_models import ExtractionResult, field_dict


def extract_receipt_fields(document_bytes: bytes) -> Dict[str, Any]:
    result = analyze_prebuilt_document(document_bytes, model_id="prebuilt-receipt")
    receipt = first_document(result)
    fields = getattr(receipt, "fields", {}) or {}
    merchant = fields.get("MerchantName")
    tax = fields.get("TotalTax")
    total = fields.get("Total")
    date = fields.get("TransactionDate")
    memo = fields.get("MerchantAddress")
    payload = ExtractionResult(
        document_type="receipt",
        provider="azure-document-intelligence",
        fields={
            "merchant": field_dict(field_value(merchant), field_confidence(merchant)),
            "date": field_dict(
                str(field_value(date)) if field_value(date) is not None else None,
                field_confidence(date),
            ),
            "tax": field_dict(field_value(tax), field_confidence(tax)),
            "total": field_dict(field_value(total), field_confidence(total)),
            "currency": field_dict(field_currency_code(total), field_confidence(total)),
            "memo": field_dict(field_value(memo), field_confidence(memo)),
        },
        line_items=extract_line_items(fields.get("Items")),
        raw_response={"model_id": "prebuilt-receipt"},
    )
    return payload.to_dict()
