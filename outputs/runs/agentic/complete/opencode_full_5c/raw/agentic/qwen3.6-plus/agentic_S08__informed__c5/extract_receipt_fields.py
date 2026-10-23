from document_client import (
    get_document_intelligence_client,
    analyze_document_from_file,
    analyze_document_from_bytes,
    PREBUILT_RECEIPT_MODEL_ID,
    extract_field_value,
    extract_field_confidence,
)
from document_models import ReceiptExtractionResult, FieldWithConfidence, LineItem


def extract_receipt_fields_from_file(file_path, content_type="application/pdf"):
    client = get_document_intelligence_client()
    result = analyze_document_from_file(
        client, PREBUILT_RECEIPT_MODEL_ID, file_path, content_type
    )
    return _parse_receipt_result(result)


def extract_receipt_fields_from_bytes(file_bytes, content_type="application/pdf"):
    client = get_document_intelligence_client()
    result = analyze_document_from_bytes(
        client, PREBUILT_RECEIPT_MODEL_ID, file_bytes, content_type
    )
    return _parse_receipt_result(result)


def _parse_receipt_result(azure_result):
    raw_fields = {}
    if hasattr(azure_result, "fields") and azure_result.fields:
        for key, field_obj in azure_result.fields.items():
            raw_fields[key] = {
                "value": extract_field_value(field_obj),
                "confidence": extract_field_confidence(field_obj),
            }

    fields = azure_result.fields if hasattr(azure_result, "fields") else {}

    merchant_name_field = fields.get("MerchantName")
    transaction_date_field = fields.get("TransactionDate")
    transaction_total_field = fields.get("Total")
    tax_field = fields.get("TotalTax")
    subtotal_field = fields.get("Subtotal")
    receipt_id_field = fields.get("TransactionId")

    receipt_result = ReceiptExtractionResult(
        merchant_name=FieldWithConfidence(
            value=extract_field_value(merchant_name_field, ""),
            confidence=extract_field_confidence(merchant_name_field, 0.0),
        ),
        transaction_date=FieldWithConfidence(
            value=extract_field_value(transaction_date_field, ""),
            confidence=extract_field_confidence(transaction_date_field, 0.0),
        ),
        transaction_total=FieldWithConfidence(
            value=extract_field_value(transaction_total_field, 0.0),
            confidence=extract_field_confidence(transaction_total_field, 0.0),
        ),
        tax=FieldWithConfidence(
            value=extract_field_value(tax_field, 0.0),
            confidence=extract_field_confidence(tax_field, 0.0),
        ),
        subtotal=FieldWithConfidence(
            value=extract_field_value(subtotal_field, 0.0),
            confidence=extract_field_confidence(subtotal_field, 0.0),
        ),
        receipt_id=FieldWithConfidence(
            value=extract_field_value(receipt_id_field, ""),
            confidence=extract_field_confidence(receipt_id_field, 0.0),
        ),
        raw_fields=raw_fields,
    )

    items_field = fields.get("Items")
    if items_field and hasattr(items_field, "value") and items_field.value:
        for item_dict in items_field.value:
            name = extract_field_value(item_dict.get("Name"), "")
            total_price = extract_field_value(item_dict.get("TotalPrice"), 0.0)
            quantity = extract_field_value(item_dict.get("Quantity"), 0.0)
            price = extract_field_value(item_dict.get("Price"), 0.0)
            item_confidence = min(
                extract_field_confidence(item_dict.get("Name"), 0.0),
                extract_field_confidence(item_dict.get("TotalPrice"), 0.0),
            )
            receipt_result.items.append(
                LineItem(
                    description=str(name) if name else "",
                    quantity=float(quantity) if quantity else 1.0,
                    unit_price=float(price) if price else 0.0,
                    amount=float(total_price) if total_price else 0.0,
                    confidence=item_confidence,
                )
            )

    return receipt_result
