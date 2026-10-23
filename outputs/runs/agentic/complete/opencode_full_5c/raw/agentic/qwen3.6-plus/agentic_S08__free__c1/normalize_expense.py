import os
from typing import Union
from datetime import datetime

from document_models import (
    InvoiceExtraction,
    ReceiptExtraction,
    NormalizedExpense,
    invoice_to_normalized,
    receipt_to_normalized,
)


STANDARD_EXPENSE_SCHEMA = {
    "required_fields": [
        "document_type",
        "vendor_or_merchant",
        "transaction_date",
        "total_amount",
        "currency",
    ],
    "optional_fields": [
        "tax_amount",
        "line_items",
        "metadata",
        "normalized_at",
    ],
    "field_types": {
        "document_type": str,
        "vendor_or_merchant": str,
        "transaction_date": str,
        "total_amount": (int, float),
        "tax_amount": (int, float),
        "currency": str,
        "line_items": list,
        "metadata": dict,
        "normalized_at": str,
    },
}


def normalize_expense(
    extraction: Union[InvoiceExtraction, ReceiptExtraction],
) -> NormalizedExpense:
    if isinstance(extraction, InvoiceExtraction):
        normalized = invoice_to_normalized(extraction)
    elif isinstance(extraction, ReceiptExtraction):
        normalized = receipt_to_normalized(extraction)
    else:
        raise TypeError(
            f"Unsupported extraction type: {type(extraction).__name__}. "
            "Expected InvoiceExtraction or ReceiptExtraction."
        )

    normalized = _apply_standardization(normalized)
    return normalized


def _apply_standardization(normalized: NormalizedExpense) -> NormalizedExpense:
    normalized.currency = normalized.currency.upper() if normalized.currency else "USD"

    if normalized.transaction_date:
        normalized.transaction_date = _normalize_date(normalized.transaction_date)

    normalized.total_amount = round(abs(normalized.total_amount), 2)
    normalized.tax_amount = round(abs(normalized.tax_amount), 2)

    if normalized.line_items:
        for item in normalized.line_items:
            if "price" in item:
                item["price"] = round(abs(item.get("price", 0.0)), 2)
            if "total" in item:
                item["total"] = round(abs(item.get("total", 0.0)), 2)
            if "quantity" in item:
                item["quantity"] = abs(item.get("quantity", 1.0))

    if not normalized.normalized_at:
        normalized.normalized_at = datetime.utcnow().isoformat()

    return normalized


def _normalize_date(date_str: str) -> str:
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%m-%d-%Y",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str


def validate_schema(normalized: NormalizedExpense) -> dict:
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
    }
    data = normalized.to_json()

    for field_name in STANDARD_EXPENSE_SCHEMA["required_fields"]:
        if field_name not in data or not data[field_name]:
            result["valid"] = False
            result["errors"].append(f"Missing required field: {field_name}")

    for field_name, expected_type in STANDARD_EXPENSE_SCHEMA["field_types"].items():
        if field_name in data and data[field_name] is not None:
            value = data[field_name]
            if not isinstance(value, expected_type):
                result["warnings"].append(
                    f"Field '{field_name}' expected type {expected_type}, got {type(value).__name__}"
                )

    if normalized.total_amount < 0:
        result["warnings"].append("total_amount is negative")

    if normalized.tax_amount < 0:
        result["warnings"].append("tax_amount is negative")

    return result
