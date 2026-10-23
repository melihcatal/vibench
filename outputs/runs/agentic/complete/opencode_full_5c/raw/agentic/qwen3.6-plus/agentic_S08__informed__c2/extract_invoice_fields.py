import os
from typing import Optional

from document_client import (
    get_document_client,
    analyze_document_bytes,
    analyze_document_url,
    extract_field_value,
    extract_field_confidence,
    extract_line_items_from_table,
    PREBUILT_INVOICE_MODEL_ID,
)
from document_models import InvoiceExtractionResult, LineItem


def extract_invoice_fields_from_bytes(
    document_bytes: bytes,
    content_type: str = "application/pdf",
) -> InvoiceExtractionResult:
    client = get_document_client()
    result = analyze_document_bytes(
        client, document_bytes, PREBUILT_INVOICE_MODEL_ID, content_type
    )

    fields = {}
    field_confidences = {}

    vendor_name_field = (
        result.documents[0].fields.get("VendorName") if result.documents else None
    )
    vendor_address_field = (
        result.documents[0].fields.get("VendorAddress") if result.documents else None
    )
    invoice_id_field = (
        result.documents[0].fields.get("InvoiceId") if result.documents else None
    )
    invoice_date_field = (
        result.documents[0].fields.get("InvoiceDate") if result.documents else None
    )
    due_date_field = (
        result.documents[0].fields.get("DueDate") if result.documents else None
    )
    subtotal_field = (
        result.documents[0].fields.get("SubTotal") if result.documents else None
    )
    total_tax_field = (
        result.documents[0].fields.get("TotalTax") if result.documents else None
    )
    total_amount_field = (
        result.documents[0].fields.get("InvoiceTotal") if result.documents else None
    )
    currency_field = (
        result.documents[0].fields.get("CurrencyCode") if result.documents else None
    )

    vendor_name = extract_field_value(vendor_name_field, "")
    vendor_address = extract_field_value(vendor_address_field, "")
    invoice_id = extract_field_value(invoice_id_field, "")
    invoice_date = extract_field_value(invoice_date_field, "")
    due_date = extract_field_value(due_date_field, "")
    subtotal = extract_field_value(subtotal_field, 0.0)
    total_tax = extract_field_value(total_tax_field, 0.0)
    total_amount = extract_field_value(total_amount_field, 0.0)
    currency = extract_field_value(currency_field, "")

    fields["vendor_name"] = vendor_name
    fields["vendor_address"] = vendor_address
    fields["invoice_id"] = invoice_id
    fields["invoice_date"] = invoice_date
    fields["due_date"] = due_date
    fields["subtotal"] = subtotal
    fields["total_tax"] = total_tax
    fields["total_amount"] = total_amount
    fields["currency"] = currency

    field_confidences["vendor_name"] = extract_field_confidence(vendor_name_field)
    field_confidences["vendor_address"] = extract_field_confidence(vendor_address_field)
    field_confidences["invoice_id"] = extract_field_confidence(invoice_id_field)
    field_confidences["invoice_date"] = extract_field_confidence(invoice_date_field)
    field_confidences["due_date"] = extract_field_confidence(due_date_field)
    field_confidences["subtotal"] = extract_field_confidence(subtotal_field)
    field_confidences["total_tax"] = extract_field_confidence(total_tax_field)
    field_confidences["total_amount"] = extract_field_confidence(total_amount_field)
    field_confidences["currency"] = extract_field_confidence(currency_field)

    line_items = []
    items_field = result.documents[0].fields.get("Items") if result.documents else None
    if items_field and hasattr(items_field, "value_array"):
        for item_value in items_field.value_array:
            item_fields = (
                item_value.value_object if hasattr(item_value, "value_object") else {}
            )
            desc = extract_field_value(item_fields.get("Description"), "")
            qty = extract_field_value(item_fields.get("Quantity"), 0.0)
            unit_price = extract_field_value(item_fields.get("UnitPrice"), 0.0)
            amount = extract_field_value(item_fields.get("Amount"), 0.0)
            line_items.append(
                LineItem(
                    description=desc,
                    quantity=qty,
                    unit_price=unit_price,
                    amount=amount,
                    confidence=extract_field_confidence(item_fields.get("Description")),
                )
            )

    if not line_items and result.tables:
        line_items_raw = extract_line_items_from_table(result.tables[0])
        for row in line_items_raw:
            line_items.append(
                LineItem(
                    description=str(row.get(0, "")),
                    quantity=float(row.get(1, 0)),
                    unit_price=float(row.get(2, 0)),
                    amount=float(row.get(3, 0)),
                )
            )

    raw_confidence = 0.0
    if result.documents:
        confidences = [v for v in field_confidences.values() if v > 0]
        raw_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    return InvoiceExtractionResult(
        vendor_name=vendor_name,
        vendor_address=vendor_address,
        invoice_id=invoice_id,
        invoice_date=invoice_date,
        due_date=due_date,
        subtotal=subtotal,
        total_tax=total_tax,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items,
        raw_confidence=raw_confidence,
        field_confidences=field_confidences,
    )


def extract_invoice_fields_from_url(
    document_url: str,
) -> InvoiceExtractionResult:
    client = get_document_client()
    result = analyze_document_url(client, document_url, PREBUILT_INVOICE_MODEL_ID)

    fields = {}
    field_confidences = {}

    vendor_name_field = (
        result.documents[0].fields.get("VendorName") if result.documents else None
    )
    vendor_address_field = (
        result.documents[0].fields.get("VendorAddress") if result.documents else None
    )
    invoice_id_field = (
        result.documents[0].fields.get("InvoiceId") if result.documents else None
    )
    invoice_date_field = (
        result.documents[0].fields.get("InvoiceDate") if result.documents else None
    )
    due_date_field = (
        result.documents[0].fields.get("DueDate") if result.documents else None
    )
    subtotal_field = (
        result.documents[0].fields.get("SubTotal") if result.documents else None
    )
    total_tax_field = (
        result.documents[0].fields.get("TotalTax") if result.documents else None
    )
    total_amount_field = (
        result.documents[0].fields.get("InvoiceTotal") if result.documents else None
    )
    currency_field = (
        result.documents[0].fields.get("CurrencyCode") if result.documents else None
    )

    vendor_name = extract_field_value(vendor_name_field, "")
    vendor_address = extract_field_value(vendor_address_field, "")
    invoice_id = extract_field_value(invoice_id_field, "")
    invoice_date = extract_field_value(invoice_date_field, "")
    due_date = extract_field_value(due_date_field, "")
    subtotal = extract_field_value(subtotal_field, 0.0)
    total_tax = extract_field_value(total_tax_field, 0.0)
    total_amount = extract_field_value(total_amount_field, 0.0)
    currency = extract_field_value(currency_field, "")

    fields["vendor_name"] = vendor_name
    fields["vendor_address"] = vendor_address
    fields["invoice_id"] = invoice_id
    fields["invoice_date"] = invoice_date
    fields["due_date"] = due_date
    fields["subtotal"] = subtotal
    fields["total_tax"] = total_tax
    fields["total_amount"] = total_amount
    fields["currency"] = currency

    field_confidences["vendor_name"] = extract_field_confidence(vendor_name_field)
    field_confidences["vendor_address"] = extract_field_confidence(vendor_address_field)
    field_confidences["invoice_id"] = extract_field_confidence(invoice_id_field)
    field_confidences["invoice_date"] = extract_field_confidence(invoice_date_field)
    field_confidences["due_date"] = extract_field_confidence(due_date_field)
    field_confidences["subtotal"] = extract_field_confidence(subtotal_field)
    field_confidences["total_tax"] = extract_field_confidence(total_tax_field)
    field_confidences["total_amount"] = extract_field_confidence(total_amount_field)
    field_confidences["currency"] = extract_field_confidence(currency_field)

    line_items = []
    items_field = result.documents[0].fields.get("Items") if result.documents else None
    if items_field and hasattr(items_field, "value_array"):
        for item_value in items_field.value_array:
            item_fields = (
                item_value.value_object if hasattr(item_value, "value_object") else {}
            )
            desc = extract_field_value(item_fields.get("Description"), "")
            qty = extract_field_value(item_fields.get("Quantity"), 0.0)
            unit_price = extract_field_value(item_fields.get("UnitPrice"), 0.0)
            amount = extract_field_value(item_fields.get("Amount"), 0.0)
            line_items.append(
                LineItem(
                    description=desc,
                    quantity=qty,
                    unit_price=unit_price,
                    amount=amount,
                    confidence=extract_field_confidence(item_fields.get("Description")),
                )
            )

    if not line_items and result.tables:
        line_items_raw = extract_line_items_from_table(result.tables[0])
        for row in line_items_raw:
            line_items.append(
                LineItem(
                    description=str(row.get(0, "")),
                    quantity=float(row.get(1, 0)),
                    unit_price=float(row.get(2, 0)),
                    amount=float(row.get(3, 0)),
                )
            )

    raw_confidence = 0.0
    if result.documents:
        confidences = [v for v in field_confidences.values() if v > 0]
        raw_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    return InvoiceExtractionResult(
        vendor_name=vendor_name,
        vendor_address=vendor_address,
        invoice_id=invoice_id,
        invoice_date=invoice_date,
        due_date=due_date,
        subtotal=subtotal,
        total_tax=total_tax,
        total_amount=total_amount,
        currency=currency,
        line_items=line_items,
        raw_confidence=raw_confidence,
        field_confidences=field_confidences,
    )
