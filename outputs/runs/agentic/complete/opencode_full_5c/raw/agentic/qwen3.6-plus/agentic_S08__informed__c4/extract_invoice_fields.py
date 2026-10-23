from document_client import (
    get_document_intelligence_client,
    read_file_bytes,
    build_poller_response,
    extract_field_value,
    extract_confidence,
    extract_line_items_from_table,
)
from document_models import InvoiceExtractionResult, ExtractedField


def extract_invoice_fields(file_path: str) -> InvoiceExtractionResult:
    client = get_document_intelligence_client()
    document_bytes = read_file_bytes(file_path)

    poller = client.begin_analyze_document(
        "prebuilt-invoice",
        document_bytes,
    )
    result = build_poller_response(poller)

    fields = result.fields if result.fields else {}

    vendor_field = fields.get("VendorName")
    vendor_value = extract_field_value(vendor_field)
    vendor_confidence = extract_confidence(vendor_field)

    date_field = fields.get("InvoiceDate")
    date_value = extract_field_value(date_field)
    date_confidence = extract_confidence(date_field)

    total_field = fields.get("InvoiceTotal")
    total_value = extract_field_value(total_field)
    total_confidence = extract_confidence(total_field)

    items = []
    items_field = fields.get("Items")
    if items_field and hasattr(items_field, "value") and items_field.value:
        for idx, item_obj in enumerate(items_field.value):
            item_fields = item_obj.value if hasattr(item_obj, "value") else {}
            description = extract_field_value(item_fields.get("Description"))
            amount = extract_field_value(item_fields.get("Amount"))
            quantity = extract_field_value(item_fields.get("Quantity"))
            items.append(
                {
                    "description": description,
                    "amount": amount,
                    "quantity": quantity,
                    "confidence": extract_confidence(item_obj),
                }
            )

    if not items and result.pages:
        items = extract_line_items_from_table(result.pages)

    invoice_result = InvoiceExtractionResult(
        vendor=ExtractedField(
            name="vendor", value=vendor_value, confidence=vendor_confidence
        ),
        invoice_date=ExtractedField(
            name="invoice_date", value=date_value, confidence=date_confidence
        ),
        total=ExtractedField(
            name="total", value=total_value, confidence=total_confidence
        ),
        line_items=items,
        raw_response={
            "model_id": "prebuilt-invoice",
            "service": "azure-document-intelligence",
        },
    )
    return invoice_result
