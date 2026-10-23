from document_client import (
    get_document_intelligence_client,
    analyze_document_from_file,
    analyze_document_from_bytes,
    PREBUILT_INVOICE_MODEL_ID,
    extract_field_value,
    extract_field_confidence,
)
from document_models import InvoiceExtractionResult, FieldWithConfidence, LineItem


def extract_invoice_fields_from_file(file_path, content_type="application/pdf"):
    client = get_document_intelligence_client()
    result = analyze_document_from_file(
        client, PREBUILT_INVOICE_MODEL_ID, file_path, content_type
    )
    return _parse_invoice_result(result)


def extract_invoice_fields_from_bytes(file_bytes, content_type="application/pdf"):
    client = get_document_intelligence_client()
    result = analyze_document_from_bytes(
        client, PREBUILT_INVOICE_MODEL_ID, file_bytes, content_type
    )
    return _parse_invoice_result(result)


def _parse_invoice_result(azure_result):
    raw_fields = {}
    if hasattr(azure_result, "fields") and azure_result.fields:
        for key, field_obj in azure_result.fields.items():
            raw_fields[key] = {
                "value": extract_field_value(field_obj),
                "confidence": extract_field_confidence(field_obj),
            }

    fields = azure_result.fields if hasattr(azure_result, "fields") else {}

    vendor_name_field = fields.get("VendorName")
    invoice_date_field = fields.get("InvoiceDate")
    invoice_total_field = fields.get("InvoiceTotal")
    invoice_sub_total_field = fields.get("SubTotal")
    invoice_tax_field = fields.get("TotalTax")
    invoice_id_field = fields.get("InvoiceId")
    billing_address_field = fields.get("CustomerAddress")

    invoice_result = InvoiceExtractionResult(
        vendor_name=FieldWithConfidence(
            value=extract_field_value(vendor_name_field, ""),
            confidence=extract_field_confidence(vendor_name_field, 0.0),
        ),
        invoice_date=FieldWithConfidence(
            value=extract_field_value(invoice_date_field, ""),
            confidence=extract_field_confidence(invoice_date_field, 0.0),
        ),
        invoice_total=FieldWithConfidence(
            value=extract_field_value(invoice_total_field, 0.0),
            confidence=extract_field_confidence(invoice_total_field, 0.0),
        ),
        invoice_sub_total=FieldWithConfidence(
            value=extract_field_value(invoice_sub_total_field, 0.0),
            confidence=extract_field_confidence(invoice_sub_total_field, 0.0),
        ),
        invoice_tax=FieldWithConfidence(
            value=extract_field_value(invoice_tax_field, 0.0),
            confidence=extract_field_confidence(invoice_tax_field, 0.0),
        ),
        invoice_id=FieldWithConfidence(
            value=extract_field_value(invoice_id_field, ""),
            confidence=extract_field_confidence(invoice_id_field, 0.0),
        ),
        billing_address=FieldWithConfidence(
            value=extract_field_value(billing_address_field, ""),
            confidence=extract_field_confidence(billing_address_field, 0.0),
        ),
        raw_fields=raw_fields,
    )

    items_field = fields.get("Items")
    if items_field and hasattr(items_field, "value") and items_field.value:
        for item_dict in items_field.value:
            description = extract_field_value(item_dict.get("Description"), "")
            quantity = extract_field_value(item_dict.get("Quantity"), 0.0)
            unit_price = extract_field_value(item_dict.get("UnitPrice"), 0.0)
            amount = extract_field_value(item_dict.get("Amount"), 0.0)
            item_confidence = min(
                extract_field_confidence(item_dict.get("Description"), 0.0),
                extract_field_confidence(item_dict.get("Amount"), 0.0),
            )
            invoice_result.line_items.append(
                LineItem(
                    description=str(description) if description else "",
                    quantity=float(quantity) if quantity else 0.0,
                    unit_price=float(unit_price) if unit_price else 0.0,
                    amount=float(amount) if amount else 0.0,
                    confidence=item_confidence,
                )
            )

    return invoice_result
