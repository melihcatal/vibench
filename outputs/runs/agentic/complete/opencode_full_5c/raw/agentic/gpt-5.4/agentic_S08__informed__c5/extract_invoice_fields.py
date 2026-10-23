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


def extract_invoice_fields(document_bytes: bytes) -> Dict[str, Any]:
    result = analyze_prebuilt_document(document_bytes, model_id="prebuilt-invoice")
    invoice = first_document(result)
    fields = getattr(invoice, "fields", {}) or {}
    vendor = fields.get("VendorName")
    date = fields.get("InvoiceDate")
    total = fields.get("InvoiceTotal")
    subtotal = fields.get("SubTotal")
    tax = fields.get("TotalTax")
    notes = fields.get("CustomerAddressRecipient") or fields.get(
        "RemittanceAddressRecipient"
    )
    payload = ExtractionResult(
        document_type="invoice",
        provider="azure-document-intelligence",
        fields={
            "vendor": field_dict(field_value(vendor), field_confidence(vendor)),
            "date": field_dict(
                str(field_value(date)) if field_value(date) is not None else None,
                field_confidence(date),
            ),
            "subtotal": field_dict(field_value(subtotal), field_confidence(subtotal)),
            "tax": field_dict(field_value(tax), field_confidence(tax)),
            "total": field_dict(field_value(total), field_confidence(total)),
            "currency": field_dict(field_currency_code(total), field_confidence(total)),
            "notes": field_dict(field_value(notes), field_confidence(notes)),
        },
        line_items=extract_line_items(fields.get("Items")),
        raw_response={"model_id": "prebuilt-invoice"},
    )
    return payload.to_dict()
