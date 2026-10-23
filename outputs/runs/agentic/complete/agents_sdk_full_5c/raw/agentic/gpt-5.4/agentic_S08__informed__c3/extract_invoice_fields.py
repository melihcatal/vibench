from __future__ import annotations

from typing import BinaryIO, List

from document_client import DocumentExtractionConfig, field_confidence, field_content, get_document_client, get_field
from document_models import ExtractedDocument, LineItem, normalize_date, parse_float



def extract_invoice_fields(file_obj: BinaryIO) -> dict:
    config = DocumentExtractionConfig(model_id="prebuilt-invoice")
    client = get_document_client(config)
    poller = client.begin_analyze_document(model_id="prebuilt-invoice", body=file_obj)
    result = poller.result()
    document = result.documents[0]
    fields = document.fields

    vendor_field = get_field(fields, "VendorName", "VendorAddressRecipient")
    date_field = get_field(fields, "InvoiceDate", "TransactionDate")
    total_field = get_field(fields, "InvoiceTotal", "Total")
    items_field = get_field(fields, "Items")
    currency_field = get_field(fields, "CurrencyCode")

    line_items: List[LineItem] = []
    if items_field and getattr(items_field, "value_array", None):
        for item in items_field.value_array:
            item_fields = getattr(item, "value_object", {})
            description = field_content(item_fields.get("Description")) or ""
            quantity = parse_float(field_content(item_fields.get("Quantity")))
            unit_price = parse_float(field_content(item_fields.get("UnitPrice")))
            amount = parse_float(field_content(item_fields.get("Amount")))
            confidence = field_confidence(item_fields.get("Amount"))
            line_items.append(
                LineItem(
                    description=str(description),
                    quantity=quantity,
                    unit_price=unit_price,
                    amount=amount,
                    confidence=confidence,
                )
            )

    extracted = ExtractedDocument(
        document_type="invoice",
        vendor_name=field_content(vendor_field),
        invoice_date=normalize_date(str(field_content(date_field)) if field_content(date_field) is not None else None),
        total=parse_float(field_content(total_field)),
        currency=field_content(currency_field),
        line_items=line_items,
        confidence={
            "vendor_name": field_confidence(vendor_field) or 0.0,
            "invoice_date": field_confidence(date_field) or 0.0,
            "total": field_confidence(total_field) or 0.0,
        },
        raw_provider_response=result.as_dict(),
    )
    return {
        "document_type": extracted.document_type,
        "vendor_name": extracted.vendor_name,
        "invoice_date": extracted.invoice_date,
        "total": extracted.total,
        "currency": extracted.currency,
        "line_items": [item.__dict__ for item in extracted.line_items],
        "confidence": extracted.confidence,
    }
