import os
from typing import Optional

from document_client import (
    get_document_client,
    analyze_document_bytes,
    analyze_document_url,
    extract_field_value,
    extract_field_confidence,
    extract_line_items_from_table,
    PREBUILT_RECEIPT_MODEL_ID,
)
from document_models import ReceiptExtractionResult, ReceiptItem


def extract_receipt_fields_from_bytes(
    document_bytes: bytes,
    content_type: str = "application/pdf",
) -> ReceiptExtractionResult:
    client = get_document_client()
    result = analyze_document_bytes(
        client, document_bytes, PREBUILT_RECEIPT_MODEL_ID, content_type
    )

    field_confidences = {}

    merchant_name_field = (
        result.documents[0].fields.get("MerchantName") if result.documents else None
    )
    merchant_address_field = (
        result.documents[0].fields.get("MerchantAddress") if result.documents else None
    )
    transaction_date_field = (
        result.documents[0].fields.get("TransactionDate") if result.documents else None
    )
    transaction_time_field = (
        result.documents[0].fields.get("TransactionTime") if result.documents else None
    )
    subtotal_field = (
        result.documents[0].fields.get("Subtotal") if result.documents else None
    )
    total_tax_field = (
        result.documents[0].fields.get("TotalTax") if result.documents else None
    )
    total_amount_field = (
        result.documents[0].fields.get("Total") if result.documents else None
    )
    currency_field = (
        result.documents[0].fields.get("CurrencyCode") if result.documents else None
    )

    merchant_name = extract_field_value(merchant_name_field, "")
    merchant_address = extract_field_value(merchant_address_field, "")
    transaction_date = extract_field_value(transaction_date_field, "")
    transaction_time = extract_field_value(transaction_time_field, "")
    subtotal = extract_field_value(subtotal_field, 0.0)
    total_tax = extract_field_value(total_tax_field, 0.0)
    total_amount = extract_field_value(total_amount_field, 0.0)
    currency = extract_field_value(currency_field, "")

    field_confidences["merchant_name"] = extract_field_confidence(merchant_name_field)
    field_confidences["merchant_address"] = extract_field_confidence(
        merchant_address_field
    )
    field_confidences["transaction_date"] = extract_field_confidence(
        transaction_date_field
    )
    field_confidences["transaction_time"] = extract_field_confidence(
        transaction_time_field
    )
    field_confidences["subtotal"] = extract_field_confidence(subtotal_field)
    field_confidences["total_tax"] = extract_field_confidence(total_tax_field)
    field_confidences["total_amount"] = extract_field_confidence(total_amount_field)
    field_confidences["currency"] = extract_field_confidence(currency_field)

    items = []
    items_field = result.documents[0].fields.get("Items") if result.documents else None
    if items_field and hasattr(items_field, "value_array"):
        for item_value in items_field.value_array:
            item_fields = (
                item_value.value_object if hasattr(item_value, "value_object") else {}
            )
            name = extract_field_value(item_fields.get("Name"), "")
            qty = extract_field_value(item_fields.get("Quantity"), 0.0)
            total_price = extract_field_value(item_fields.get("TotalPrice"), 0.0)
            items.append(
                ReceiptItem(
                    name=name,
                    quantity=qty,
                    total_price=total_price,
                    confidence=extract_field_confidence(item_fields.get("Name")),
                )
            )

    if not items and result.tables:
        items_raw = extract_line_items_from_table(result.tables[0])
        for row in items_raw:
            items.append(
                ReceiptItem(
                    name=str(row.get(0, "")),
                    quantity=float(row.get(1, 0)),
                    total_price=float(row.get(2, 0)),
                )
            )

    raw_confidence = 0.0
    if result.documents:
        confidences = [v for v in field_confidences.values() if v > 0]
        raw_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    return ReceiptExtractionResult(
        merchant_name=merchant_name,
        merchant_address=merchant_address,
        transaction_date=transaction_date,
        transaction_time=transaction_time,
        subtotal=subtotal,
        total_tax=total_tax,
        total_amount=total_amount,
        currency=currency,
        items=items,
        raw_confidence=raw_confidence,
        field_confidences=field_confidences,
    )


def extract_receipt_fields_from_url(
    document_url: str,
) -> ReceiptExtractionResult:
    client = get_document_client()
    result = analyze_document_url(client, document_url, PREBUILT_RECEIPT_MODEL_ID)

    field_confidences = {}

    merchant_name_field = (
        result.documents[0].fields.get("MerchantName") if result.documents else None
    )
    merchant_address_field = (
        result.documents[0].fields.get("MerchantAddress") if result.documents else None
    )
    transaction_date_field = (
        result.documents[0].fields.get("TransactionDate") if result.documents else None
    )
    transaction_time_field = (
        result.documents[0].fields.get("TransactionTime") if result.documents else None
    )
    subtotal_field = (
        result.documents[0].fields.get("Subtotal") if result.documents else None
    )
    total_tax_field = (
        result.documents[0].fields.get("TotalTax") if result.documents else None
    )
    total_amount_field = (
        result.documents[0].fields.get("Total") if result.documents else None
    )
    currency_field = (
        result.documents[0].fields.get("CurrencyCode") if result.documents else None
    )

    merchant_name = extract_field_value(merchant_name_field, "")
    merchant_address = extract_field_value(merchant_address_field, "")
    transaction_date = extract_field_value(transaction_date_field, "")
    transaction_time = extract_field_value(transaction_time_field, "")
    subtotal = extract_field_value(subtotal_field, 0.0)
    total_tax = extract_field_value(total_tax_field, 0.0)
    total_amount = extract_field_value(total_amount_field, 0.0)
    currency = extract_field_value(currency_field, "")

    field_confidences["merchant_name"] = extract_field_confidence(merchant_name_field)
    field_confidences["merchant_address"] = extract_field_confidence(
        merchant_address_field
    )
    field_confidences["transaction_date"] = extract_field_confidence(
        transaction_date_field
    )
    field_confidences["transaction_time"] = extract_field_confidence(
        transaction_time_field
    )
    field_confidences["subtotal"] = extract_field_confidence(subtotal_field)
    field_confidences["total_tax"] = extract_field_confidence(total_tax_field)
    field_confidences["total_amount"] = extract_field_confidence(total_amount_field)
    field_confidences["currency"] = extract_field_confidence(currency_field)

    items = []
    items_field = result.documents[0].fields.get("Items") if result.documents else None
    if items_field and hasattr(items_field, "value_array"):
        for item_value in items_field.value_array:
            item_fields = (
                item_value.value_object if hasattr(item_value, "value_object") else {}
            )
            name = extract_field_value(item_fields.get("Name"), "")
            qty = extract_field_value(item_fields.get("Quantity"), 0.0)
            total_price = extract_field_value(item_fields.get("TotalPrice"), 0.0)
            items.append(
                ReceiptItem(
                    name=name,
                    quantity=qty,
                    total_price=total_price,
                    confidence=extract_field_confidence(item_fields.get("Name")),
                )
            )

    if not items and result.tables:
        items_raw = extract_line_items_from_table(result.tables[0])
        for row in items_raw:
            items.append(
                ReceiptItem(
                    name=str(row.get(0, "")),
                    quantity=float(row.get(1, 0)),
                    total_price=float(row.get(2, 0)),
                )
            )

    raw_confidence = 0.0
    if result.documents:
        confidences = [v for v in field_confidences.values() if v > 0]
        raw_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    return ReceiptExtractionResult(
        merchant_name=merchant_name,
        merchant_address=merchant_address,
        transaction_date=transaction_date,
        transaction_time=transaction_time,
        subtotal=subtotal,
        total_tax=total_tax,
        total_amount=total_amount,
        currency=currency,
        items=items,
        raw_confidence=raw_confidence,
        field_confidences=field_confidences,
    )
