import os
from typing import Union
from document_models import (
    ExtractedInvoiceFields,
    ExtractedReceiptFields,
    NormalizedExpenseRecord,
    normalize_expense_record,
)

CURRENCY_MAP = {
    "USD": "USD",
    "EUR": "EUR",
    "GBP": "GBP",
    "CAD": "CAD",
    "AUD": "AUD",
    "JPY": "JPY",
}


def normalize_expense(
    extracted_data: Union[ExtractedInvoiceFields, ExtractedReceiptFields],
    document_type: str,
    currency: str = "USD",
) -> NormalizedExpenseRecord:
    resolved_currency = CURRENCY_MAP.get(currency.upper(), "USD")
    record = normalize_expense_record(extracted_data, document_type, resolved_currency)
    return record


def normalize_expense_to_dict(
    extracted_data: Union[ExtractedInvoiceFields, ExtractedReceiptFields],
    document_type: str,
    currency: str = "USD",
) -> dict:
    record = normalize_expense(extracted_data, document_type, currency)
    return {
        "document_type": record.document_type,
        "vendor_or_merchant": record.vendor_or_merchant,
        "document_id": record.document_id,
        "date": record.date,
        "total_amount": record.total_amount,
        "tax_amount": record.tax_amount,
        "subtotal": record.subtotal,
        "line_items": record.line_items,
        "currency": record.currency,
        "confidence": record.confidence,
        "normalized_at": record.normalized_at,
    }


def normalize_multiple_expenses(documents: list, default_currency: str = "USD") -> list:
    normalized_records = []
    for doc in documents:
        extracted_data = doc["extracted_data"]
        document_type = doc["document_type"]
        currency = doc.get("currency", default_currency)
        record = normalize_expense(extracted_data, document_type, currency)
        normalized_records.append(record)
    return normalized_records
