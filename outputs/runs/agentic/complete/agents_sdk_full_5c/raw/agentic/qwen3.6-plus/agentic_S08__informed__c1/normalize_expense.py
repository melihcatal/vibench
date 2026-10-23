"""
[SAME-SCENARIO] Normalize extracted expense fields into a standard JSON schema.

Takes InvoiceExtractionResult or ReceiptExtractionResult objects from the
same-scenario extraction step and converts them into a NormalizedExpenseRecord
conforming to a standardized expense JSON schema.
Provider: Mindee - Invoice/Receipt OCR upstream; normalization is applied via local schema
SDK: mindee (upstream dependency)
Auth: MINDEE_API_KEY
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict, List, Union

from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpenseRecord,
    ExpenseCategory,
    compute_overall_confidence,
)


def _map_category_from_vendor(vendor_name: str | None) -> ExpenseCategory:
    """Heuristically map vendor name to an expense category."""
    if not vendor_name:
        return ExpenseCategory.OTHER

    name_lower = vendor_name.lower()

    travel_keywords = ["airline", "hotel", "uber", "lyft", "taxi", "car rental", "booking", "airbnb"]
    meals_keywords = ["restaurant", "cafe", "grill", "diner", "pizza", "coffee", "starbucks", "doordash", "ubereats"]
    office_keywords = ["office depot", "staples", "paper", "supply", "printer", "ink"]
    software_keywords = ["software", "cloud", "aws", "azure", "saas", "subscription", "github", "slack", "atlassian"]
    utility_keywords = ["electric", "water", "gas", "internet", "telecom", "utility", "power"]

    for kw in travel_keywords:
        if kw in name_lower:
            return ExpenseCategory.TRAVEL
    for kw in meals_keywords:
        if kw in name_lower:
            return ExpenseCategory.MEALS
    for kw in office_keywords:
        if kw in name_lower:
            return ExpenseCategory.OFFICE_SUPPLIES
    for kw in software_keywords:
        if kw in name_lower:
            return ExpenseCategory.SOFTWARE
    for kw in utility_keywords:
        if kw in name_lower:
            return ExpenseCategory.UTILITIES

    return ExpenseCategory.OTHER


def normalize_expense_from_invoice(
    invoice: InvoiceExtractionResult,
    category: ExpenseCategory | None = None,
    notes: str | None = None,
) -> NormalizedExpenseRecord:
    """
    Normalize an InvoiceExtractionResult into a NormalizedExpenseRecord.

    Args:
        invoice: The extracted invoice result from Mindee Invoice OCR.
        category: Optional expense category override. If None, inferred from vendor name.
        notes: Optional notes or memo to attach to the record.

    Returns:
        NormalizedExpenseRecord conforming to the standard JSON schema.
    """
    if category is None:
        category = _map_category_from_vendor(
            invoice.vendor.name if invoice.vendor else None
        )

    line_items_normalized = []
    for item in invoice.line_items:
        line_items_normalized.append({
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": str(item.unit_price) if item.unit_price else None,
            "total_price": str(item.total_price) if item.total_price else None,
            "confidence": item.confidence,
        })

    overall_confidence = compute_overall_confidence(invoice.confidence_scores)

    record = NormalizedExpenseRecord(
        expense_id=str(uuid.uuid4()),
        document_type="invoice",
        vendor_name=invoice.vendor.name if invoice.vendor else None,
        vendor_address=invoice.vendor.address if invoice.vendor else None,
        vendor_tax_id=invoice.vendor.tax_id if invoice.vendor else None,
        document_date=invoice.invoice_date,
        document_number=invoice.invoice_number,
        category=category,
        subtotal=invoice.subtotal,
        tax_amount=invoice.tax_amount,
        tip_amount=None,
        total_amount=invoice.total_amount,
        currency=invoice.currency or "USD",
        line_items=line_items_normalized,
        notes=notes,
        extracted_at=datetime.utcnow(),
        confidence=overall_confidence,
        raw_extraction=invoice.model_dump() if hasattr(invoice, "model_dump") else invoice.dict(),
    )

    return record


def normalize_expense_from_receipt(
    receipt: ReceiptExtractionResult,
    category: ExpenseCategory | None = None,
    notes: str | None = None,
) -> NormalizedExpenseRecord:
    """
    Normalize a ReceiptExtractionResult into a NormalizedExpenseRecord.

    Args:
        receipt: The extracted receipt result from Mindee Receipt OCR.
        category: Optional expense category override. If None, inferred from merchant name.
        notes: Optional notes or memo to attach to the record.

    Returns:
        NormalizedExpenseRecord conforming to the standard JSON schema.
    """
    if category is None:
        category = _map_category_from_vendor(
            receipt.merchant.name if receipt.merchant else None
        )

    items_normalized = []
    for item in receipt.items:
        items_normalized.append({
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": str(item.unit_price) if item.unit_price else None,
            "total_price": str(item.total_price) if item.total_price else None,
            "confidence": item.confidence,
        })

    overall_confidence = compute_overall_confidence(receipt.confidence_scores)

    record = NormalizedExpenseRecord(
        expense_id=str(uuid.uuid4()),
        document_type="receipt",
        vendor_name=receipt.merchant.name if receipt.merchant else None,
        vendor_address=receipt.merchant.address if receipt.merchant else None,
        vendor_tax_id=receipt.merchant.tax_id if receipt.merchant else None,
        document_date=receipt.receipt_date,
        document_number=receipt.receipt_number,
        category=category,
        subtotal=None,
        tax_amount=receipt.tax_amount,
        tip_amount=receipt.tip_amount,
        total_amount=receipt.total_amount,
        currency=receipt.currency or "USD",
        line_items=items_normalized,
        notes=notes,
        extracted_at=datetime.utcnow(),
        confidence=overall_confidence,
        raw_extraction=receipt.model_dump() if hasattr(receipt, "model_dump") else receipt.dict(),
    )

    return record


def normalize_expense(
    extraction: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    category: ExpenseCategory | None = None,
    notes: str | None = None,
) -> NormalizedExpenseRecord:
    """
    Normalize any extraction result (invoice or receipt) into a standard JSON schema.

    Provider: Mindee Invoice/Receipt OCR (upstream source).
    Uses the same Mindee API credentials (MINDEE_API_KEY) that the extraction
    files rely on.

    Args:
        extraction: Either an InvoiceExtractionResult or ReceiptExtractionResult.
        category: Optional expense category override.
        notes: Optional notes or memo.

    Returns:
        NormalizedExpenseRecord.
    """
    if isinstance(extraction, InvoiceExtractionResult):
        return normalize_expense_from_invoice(extraction, category=category, notes=notes)
    elif isinstance(extraction, ReceiptExtractionResult):
        return normalize_expense_from_receipt(extraction, category=category, notes=notes)
    else:
        raise TypeError(
            f"Unsupported extraction type: {type(extraction)}. "
            "Expected InvoiceExtractionResult or ReceiptExtractionResult from Mindee OCR."
        )
