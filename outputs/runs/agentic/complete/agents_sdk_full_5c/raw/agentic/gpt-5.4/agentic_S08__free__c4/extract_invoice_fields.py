from __future__ import annotations

from typing import Any, Dict, List

from document_client import begin_analysis, load_document_bytes
from document_models import ExtractedDocument, ExtractedLineItem, coerce_float


AZURE_INVOICE_MODEL_ID = "prebuilt-invoice"


def extract_invoice_fields(path: str) -> Dict[str, Any]:
    document_bytes = load_document_bytes(path)
    poller = begin_analysis(AZURE_INVOICE_MODEL_ID, document_bytes)
    result = poller.result()
    if not result.documents:
        return ExtractedDocument(document_type="invoice").to_dict()

    doc = result.documents[0]
    fields = doc.fields or {}

    line_items: List[ExtractedLineItem] = []
    items_field = fields.get("Items")
    if items_field and getattr(items_field, "value", None):
        for item in items_field.value:
            item_values = getattr(item, "value", {}) or {}
            line_items.append(
                ExtractedLineItem(
                    description=getattr(item_values.get("Description"), "content", None),
                    quantity=coerce_float(getattr(item_values.get("Quantity"), "value", None)),
                    unit_price=coerce_float(getattr(item_values.get("UnitPrice"), "value", None)),
                    amount=coerce_float(getattr(item_values.get("Amount"), "value", None)),
                    confidence=min(
                        [
                            c
                            for c in [
                                getattr(item_values.get("Description"), "confidence", None),
                                getattr(item_values.get("Quantity"), "confidence", None),
                                getattr(item_values.get("UnitPrice"), "confidence", None),
                                getattr(item_values.get("Amount"), "confidence", None),
                            ]
                            if c is not None
                        ],
                        default=None,
                    ),
                )
            )

    extracted = ExtractedDocument(
        document_type="invoice",
        vendor=getattr(fields.get("VendorName"), "content", None),
        invoice_date=str(getattr(fields.get("InvoiceDate"), "value", "")) or None,
        total=coerce_float(getattr(fields.get("InvoiceTotal"), "value", None)),
        currency=getattr(getattr(fields.get("InvoiceTotal"), "value", None), "currency_symbol", None),
        line_items=line_items,
        notes=getattr(fields.get("CustomerAddressRecipient"), "content", None),
        confidence={
            "vendor": getattr(fields.get("VendorName"), "confidence", None),
            "date": getattr(fields.get("InvoiceDate"), "confidence", None),
            "total": getattr(fields.get("InvoiceTotal"), "confidence", None),
            "line_items": getattr(items_field, "confidence", None),
        },
        raw_provider_response=result.to_dict(),
    )
    return extracted.to_dict()
