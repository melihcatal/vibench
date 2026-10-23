from __future__ import annotations

from document_client import begin_invoice_analysis, field_to_pair
from document_models import (
    DocumentSource,
    ExtractedField,
    LineItem,
    ReceiptExtraction,
    parse_float,
)


def extract_receipt_fields(source: DocumentSource) -> dict:
    poller = begin_invoice_analysis(source.content, source.mime_type)
    result = poller.result()
    document = result.documents[0] if result.documents else None
    fields = document.fields if document else {}

    merchant_value, merchant_confidence = field_to_pair(fields.get("MerchantName"))
    tax_value, tax_confidence = field_to_pair(fields.get("TotalTax"))
    total_value, total_confidence = field_to_pair(fields.get("Total"))

    items = []
    items_field = fields.get("Items")
    if items_field and getattr(items_field, "value_array", None):
        for item in items_field.value_array:
            value_object = getattr(item, "value_object", {}) or {}
            description, item_conf = field_to_pair(value_object.get("Description"))
            quantity, _ = field_to_pair(value_object.get("Quantity"))
            amount, _ = field_to_pair(value_object.get("TotalPrice"))
            items.append(
                LineItem(
                    description=description,
                    quantity=parse_float(quantity),
                    amount=parse_float(amount),
                    confidence=item_conf,
                )
            )

    extraction = ReceiptExtraction(
        merchant=ExtractedField(value=merchant_value, confidence=merchant_confidence)
        if merchant_value is not None
        else None,
        tax=ExtractedField(value=parse_float(tax_value), confidence=tax_confidence)
        if tax_value is not None
        else None,
        total=ExtractedField(
            value=parse_float(total_value), confidence=total_confidence
        )
        if total_value is not None
        else None,
        items=items,
        raw_response=result.as_dict(),
    )
    return extraction.to_dict()
