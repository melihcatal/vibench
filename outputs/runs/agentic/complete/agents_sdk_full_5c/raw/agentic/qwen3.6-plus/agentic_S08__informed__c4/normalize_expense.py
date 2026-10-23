"""
Normalize extracted expense fields into a standard JSON schema.

Uses the local data models and helpers from document_models.py and document_client.py
to transform invoice and receipt extraction results into a unified NormalizedExpense record.
"""

import json
import uuid
from typing import Optional, Union

from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpense,
    build_normalized_expense_from_invoice,
    build_normalized_expense_from_receipt,
)
from document_client import (
    normalize_amount,
    normalize_date,
)


def normalize_expense(
    extraction_result: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    expense_id: Optional[str] = None,
    currency: str = "USD",
) -> NormalizedExpense:
    """
    Normalize extracted invoice or receipt fields into a standard JSON schema.

    Args:
        extraction_result: An InvoiceExtractionResult or ReceiptExtractionResult.
        expense_id: Optional unique ID for the expense record.
        currency: Currency code (default: USD).

    Returns:
        NormalizedExpense conforming to the standard schema.
    """
    if not expense_id:
        expense_id = str(uuid.uuid4())

    if isinstance(extraction_result, InvoiceExtractionResult):
        normalized = build_normalized_expense_from_invoice(extraction_result, expense_id)
    elif isinstance(extraction_result, ReceiptExtractionResult):
        normalized = build_normalized_expense_from_receipt(extraction_result, expense_id)
    else:
        raise TypeError(
            f"Expected InvoiceExtractionResult or ReceiptExtractionResult, "
            f"got {type(extraction_result).__name__}"
        )

    normalized.expense_id = expense_id
    normalized.currency = currency

    # Ensure totals are computed correctly
    if normalized.line_items and normalized.total is None:
        item_totals = [
            float(item.get("total_price", 0) or 0)
            for item in normalized.line_items
        ]
        if item_totals:
            normalized.total = round(sum(item_totals) + (normalized.tax or 0), 2)

    if normalized.total is not None and normalized.tax is not None:
        if normalized.subtotal is None:
            normalized.subtotal = round(normalized.total - normalized.tax, 2)

    # Re-validate confidence
    if normalized.confidence <= 0 and normalized.raw_extraction:
        normalized.confidence = _compute_average_confidence(extraction_result)

    return normalized


def normalize_to_json(
    extraction_result: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    expense_id: Optional[str] = None,
    currency: str = "USD",
    indent: int = 2,
) -> str:
    """
    Normalize and serialize an extraction result to a JSON string.

    Args:
        extraction_result: An InvoiceExtractionResult or ReceiptExtractionResult.
        expense_id: Optional unique ID.
        currency: Currency code.
        indent: JSON indentation level.

    Returns:
        JSON string of the normalized expense.
    """
    normalized = normalize_expense(extraction_result, expense_id, currency)
    return normalized.to_json()


def normalize_batch(
    results: list,
    currency: str = "USD",
) -> list:
    """
    Normalize a batch of extraction results into a list of NormalizedExpense records.

    Args:
        results: List of InvoiceExtractionResult or ReceiptExtractionResult objects.
        currency: Currency code for all records.

    Returns:
        List of NormalizedExpense objects.
    """
    normalized_list = []
    for result in results:
        normalized = normalize_expense(result, currency=currency)
        normalized_list.append(normalized)
    return normalized_list


def normalize_to_dict(
    extraction_result: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    expense_id: Optional[str] = None,
    currency: str = "USD",
) -> dict:
    """
    Normalize an extraction result and return as a dictionary.

    Args:
        extraction_result: An InvoiceExtractionResult or ReceiptExtractionResult.
        expense_id: Optional unique ID.
        currency: Currency code.

    Returns:
        Dictionary representation of the normalized expense.
    """
    normalized = normalize_expense(extraction_result, expense_id, currency)
    return normalized.to_dict()


def _compute_average_confidence(
    extraction_result: Union[InvoiceExtractionResult, ReceiptExtractionResult],
) -> float:
    """Compute the average confidence score across all extracted fields."""
    confidences = []

    if isinstance(extraction_result, InvoiceExtractionResult):
        confidences = [
            extraction_result.vendor_confidence,
            extraction_result.invoice_date_confidence,
            extraction_result.total_confidence,
            extraction_result.tax_confidence,
        ]
    elif isinstance(extraction_result, ReceiptExtractionResult):
        confidences = [
            extraction_result.merchant_confidence,
            extraction_result.receipt_date_confidence,
            extraction_result.total_confidence,
            extraction_result.tax_confidence,
        ]

    confidences = [c for c in confidences if c and c > 0]
    if confidences:
        return round(sum(confidences) / len(confidences), 4)
    return 0.0
