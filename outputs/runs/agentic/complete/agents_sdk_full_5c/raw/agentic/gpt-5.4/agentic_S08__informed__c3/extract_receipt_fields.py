from __future__ import annotations

from typing import BinaryIO, List

from document_client import DocumentExtractionConfig, field_confidence, field_content, get_document_client, get_field
from document_models import ExtractedDocument, LineItem, parse_float



def extract_receipt_fields(file_obj: BinaryIO) -> dict:
    config = DocumentExtractionConfig(model_id="prebuilt-invoice")
    client = get_document_client(config)
    poller = client.begin_analyze_document(model_id="prebuilt-invoice", body=file_obj)
    result = poller.result()
    document = result.documents[0]
    fields = document.fields

    merchant_field = get_field(fields, "VendorName", "MerchantName")
    tax_field = get_field(fields, "TotalTax", "Tax")
    total_field = get_field(fields, "InvoiceTotal", "Total")
    items_field = get_field(fields, "Items")

    items: List[LineItem] = []
    if items_field and getattr(items_field, "value_array", None):
        for item in items_field.value_array:
            item_fields = getattr(item, "value_object", {})
            items.append(
                LineItem(
                    description=str(field_content(item_fields.get("Description")) or ""),
                    quantity=parse_float(field_content(item_fields.get("Quantity"))),
                    unit_price=parse_float(field_content(item_fields.get("UnitPrice"))),
                    amount=parse_float(field_content(item_fields.get("Amount"))),
                    confidence=field_confidence(item_fields.get("Amount")),
                )
            )

    extracted = ExtractedDocument(
        document_type="receipt",
        merchant_name=field_content(merchant_field),
        total=parse_float(field_content(total_field)),
        tax=parse_float(field_content(tax_field)),
        items=items,
        confidence={
            "merchant_name": field_confidence(merchant_field) or 0.0,
            "tax": field_confidence(tax_field) or 0.0,
            "total": field_confidence(total_field) or 0.0,
        },
        raw_provider_response=result.as_dict(),
    )
    return {
        "document_type": extracted.document_type,
        "merchant_name": extracted.merchant_name,
        "tax": extracted.tax,
        "total": extracted.total,
        "items": [item.__dict__ for item in extracted.items],
        "confidence": extracted.confidence,
    }
