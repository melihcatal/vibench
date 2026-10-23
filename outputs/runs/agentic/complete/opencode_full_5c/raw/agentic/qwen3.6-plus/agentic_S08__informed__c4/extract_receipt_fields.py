from document_client import (
    get_document_intelligence_client,
    read_file_bytes,
    build_poller_response,
    extract_field_value,
    extract_confidence,
    extract_line_items_from_table,
)
from document_models import ReceiptExtractionResult, ExtractedField


def extract_receipt_fields(file_path: str) -> ReceiptExtractionResult:
    client = get_document_intelligence_client()
    document_bytes = read_file_bytes(file_path)

    poller = client.begin_analyze_document(
        "prebuilt-receipt",
        document_bytes,
    )
    result = build_poller_response(poller)

    fields = result.fields if result.fields else {}

    merchant_field = fields.get("MerchantName")
    merchant_value = extract_field_value(merchant_field)
    merchant_confidence = extract_confidence(merchant_field)

    tax_field = fields.get("TotalTax")
    tax_value = extract_field_value(tax_field)
    tax_confidence = extract_confidence(tax_field)

    total_field = fields.get("Total")
    total_value = extract_field_value(total_field)
    total_confidence = extract_confidence(total_field)

    items = []
    items_field = fields.get("Items")
    if items_field and hasattr(items_field, "value") and items_field.value:
        for idx, item_obj in enumerate(items_field.value):
            item_fields = item_obj.value if hasattr(item_obj, "value") else {}
            description = extract_field_value(item_fields.get("Description"))
            price = extract_field_value(item_fields.get("TotalPrice"))
            items.append(
                {
                    "description": description,
                    "price": price,
                    "confidence": extract_confidence(item_obj),
                }
            )

    if not items and result.pages:
        items = extract_line_items_from_table(result.pages)

    receipt_result = ReceiptExtractionResult(
        merchant=ExtractedField(
            name="merchant", value=merchant_value, confidence=merchant_confidence
        ),
        tax=ExtractedField(name="tax", value=tax_value, confidence=tax_confidence),
        total=ExtractedField(
            name="total", value=total_value, confidence=total_confidence
        ),
        items=items,
        raw_response={
            "model_id": "prebuilt-receipt",
            "service": "azure-document-intelligence",
        },
    )
    return receipt_result
