from __future__ import annotations

from typing import Any, Dict, List

from document_client import begin_analysis, load_document_bytes
from document_models import ExtractedDocument, ExtractedLineItem, coerce_float


AZURE_RECEIPT_MODEL_ID = "prebuilt-receipt"


def extract_receipt_fields(path: str) -> Dict[str, Any]:
    document_bytes = load_document_bytes(path)
    poller = begin_analysis(AZURE_RECEIPT_MODEL_ID, document_bytes)
    result = poller.result()
    if not result.documents:
        return ExtractedDocument(document_type="receipt").to_dict()

    doc = result.documents[0]
    fields = doc.fields or {}

    items: List[ExtractedLineItem] = []
    items_field = fields.get("Items")
    if items_field and getattr(items_field, "value", None):
        for item in items_field.value:
            item_values = getattr(item, "value", {}) or {}
            items.append(
                ExtractedLineItem(
                    description=getattr(item_values.get("Description"), "content", None),
                    quantity=coerce_float(getattr(item_values.get("Quantity"), "value", None)),
                    unit_price=coerce_float(getattr(item_values.get("Price"), "value", None)),
                    amount=coerce_float(getattr(item_values.get("TotalPrice"), "value", None)),
                    confidence=min(
                        [
                            c
                            for c in [
                                getattr(item_values.get("Description"), "confidence", None),
                                getattr(item_values.get("Quantity"), "confidence", None),
                                getattr(item_values.get("Price"), "confidence", None),
                                getattr(item_values.get("TotalPrice"), "confidence", None),
                            ]
                            if c is not None
                        ],
                        default=None,
                    ),
                )
            )

    extracted = ExtractedDocument(
        document_type="receipt",
        merchant=getattr(fields.get("MerchantName"), "content", None),
        invoice_date=str(getattr(fields.get("TransactionDate"), "value", "")) or None,
        total=coerce_float(getattr(fields.get("Total"), "value", None)),
        tax=coerce_float(getattr(fields.get("Tax"), "value", None)),
        currency=getattr(getattr(fields.get("Total"), "value", None), "currency_symbol", None),
        items=items,
        notes=getattr(fields.get("MerchantPhoneNumber"), "content", None),
        confidence={
            "merchant": getattr(fields.get("MerchantName"), "confidence", None),
            "tax": getattr(fields.get("Tax"), "confidence", None),
            "total": getattr(fields.get("Total"), "confidence", None),
            "items": getattr(items_field, "confidence", None),
        },
        raw_provider_response=result.to_dict(),
    )
    return extracted.to_dict()
