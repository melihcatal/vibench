from __future__ import annotations

from typing import Any, Dict, Union

from document_models import (
    ExtractedInvoice,
    ExtractedReceipt,
    normalized_expense_schema,
    to_float,
)


def normalize_expense(
    document: Union[ExtractedInvoice, ExtractedReceipt],
    source_id: str | None = None,
    currency: str | None = None,
) -> Dict[str, Any]:
    if isinstance(document, ExtractedInvoice):
        return normalized_expense_schema(
            kind="invoice",
            source_id=source_id,
            currency=currency,
            vendor=document.vendor.value if document.vendor else None,
            date=document.invoice_date.value if document.invoice_date else None,
            total=to_float(document.total.value) if document.total else None,
            tax=None,
            items=document.line_items,
            extra={
                "provider": "google-documentai",
                "vendor_confidence": document.vendor.confidence
                if document.vendor
                else 0.0,
            },
        )
    return normalized_expense_schema(
        kind="receipt",
        source_id=source_id,
        currency=currency,
        vendor=document.merchant.value if document.merchant else None,
        date=None,
        total=to_float(document.total.value) if document.total else None,
        tax=to_float(document.tax.value) if document.tax else None,
        items=document.items,
        extra={
            "provider": "google-documentai",
            "merchant_confidence": document.merchant.confidence
            if document.merchant
            else 0.0,
        },
    )
