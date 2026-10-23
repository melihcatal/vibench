from __future__ import annotations

from document_client import begin_invoice_analysis, field_to_pair
from document_models import (
    DocumentSource,
    ExtractedField,
    InvoiceExtraction,
    LineItem,
    parse_float,
)


def extract_invoice_fields(source: DocumentSource) -> dict:
    poller = begin_invoice_analysis(source.content, source.mime_type)
    result = poller.result()
    document = result.documents[0] if result.documents else None
    fields = document.fields if document else {}

    vendor_value, vendor_confidence = field_to_pair(fields.get("VendorName"))
    date_value, date_confidence = field_to_pair(fields.get("InvoiceDate"))
    total_value, total_confidence = field_to_pair(fields.get("InvoiceTotal"))

    line_items = []
    items_field = fields.get("Items")
    if items_field and getattr(items_field, "value_array", None):
        for item in items_field.value_array:
            value_object = getattr(item, "value_object", {}) or {}
            description, item_conf = field_to_pair(value_object.get("Description"))
            quantity, _ = field_to_pair(value_object.get("Quantity"))
            unit_price, _ = field_to_pair(value_object.get("UnitPrice"))
            amount, _ = field_to_pair(value_object.get("Amount"))
            line_items.append(
                LineItem(
                    description=description,
                    quantity=parse_float(quantity),
                    unit_price=parse_float(unit_price),
                    amount=parse_float(amount),
                    confidence=item_conf,
                )
            )

    extraction = InvoiceExtraction(
        vendor=ExtractedField(value=vendor_value, confidence=vendor_confidence)
        if vendor_value is not None
        else None,
        invoice_date=ExtractedField(value=str(date_value), confidence=date_confidence)
        if date_value is not None
        else None,
        total=ExtractedField(
            value=parse_float(total_value), confidence=total_confidence
        )
        if total_value is not None
        else None,
        line_items=line_items,
        raw_response=result.as_dict(),
    )
    return extraction.to_dict()
