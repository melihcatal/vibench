"""
Normalize extracted expense fields into a standard JSON schema.

Uses Azure AI Document Intelligence extracted fields and normalizes them
into a consistent expense record format for downstream processing.

Provider: Azure AI Document Intelligence (Form Recognizer)
SDK: azure-ai-documentintelligence
"""

import uuid
from datetime import datetime
from typing import Optional, Union

from document_models import (
    ExtractedInvoiceField,
    ExtractedReceiptField,
    NormalizedExpense,
)


def normalize_invoice_to_expense(
    extracted: ExtractedInvoiceField,
    document_id: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> NormalizedExpense:
    """
    Normalize extracted invoice fields into a standard NormalizedExpense schema.

    Args:
        extracted: ExtractedInvoiceField from Azure Document Intelligence analysis.
        document_id: Optional document identifier. Generated if not provided.
        metadata: Optional additional metadata to include.

    Returns:
        NormalizedExpense with standardized field mapping.
    """
    expense_id = document_id or str(uuid.uuid4())

    # Map vendor name from invoice extraction
    vendor = extracted.vendor_name or "Unknown Vendor"

    # Use invoice date as the expense date
    date = extracted.invoice_date or datetime.now().isoformat()

    # Use total or calculate from sub_total + tax
    total_amount = extracted.total
    if total_amount is None:
        sub_total = extracted.sub_total or 0.0
        tax = extracted.tax or 0.0
        total_amount = sub_total + tax

    currency = extracted.currency or "USD"
    tax_amount = extracted.tax or 0.0

    # Build line items from extracted data
    line_items = []
    for item in extracted.line_items:
        line_items.append({
            "description": item.get("Description", ""),
            "quantity": item.get("Quantity", 1),
            "unit_price": item.get("UnitPrice", 0.0),
            "amount": item.get("Amount", 0.0),
        })

    # Calculate overall confidence from available scores
    confidence_scores = extracted.confidence_scores
    if confidence_scores:
        confidence = sum(confidence_scores.values()) / len(confidence_scores)
    else:
        confidence = 0.0

    raw_fields = {
        "vendor_name": extracted.vendor_name,
        "vendor_address": extracted.vendor_address,
        "invoice_id": extracted.invoice_id,
        "invoice_date": extracted.invoice_date,
        "due_date": extracted.due_date,
        "sub_total": extracted.sub_total,
        "tax": extracted.tax,
        "total": extracted.total,
        "currency": extracted.currency,
    }

    expense = NormalizedExpense(
        expense_id=expense_id,
        document_type="invoice",
        vendor=vendor,
        date=date,
        total_amount=total_amount,
        currency=currency,
        tax_amount=tax_amount,
        line_items=line_items,
        raw_fields=raw_fields,
        confidence=confidence,
        metadata=metadata or {},
    )

    return expense


def normalize_receipt_to_expense(
    extracted: ExtractedReceiptField,
    document_id: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> NormalizedExpense:
    """
    Normalize extracted receipt fields into a standard NormalizedExpense schema.

    Args:
        extracted: ExtractedReceiptField from Azure Document Intelligence analysis.
        document_id: Optional document identifier. Generated if not provided.
        metadata: Optional additional metadata to include.

    Returns:
        NormalizedExpense with standardized field mapping.
    """
    expense_id = document_id or str(uuid.uuid4())

    # Map merchant name from receipt extraction
    vendor = extracted.merchant_name or "Unknown Merchant"

    # Use transaction date as the expense date
    date = extracted.transaction_date or datetime.now().isoformat()

    # Use total or calculate from subtotal + tax
    total_amount = extracted.total
    if total_amount is None:
        subtotal = extracted.subtotal or 0.0
        tax = extracted.tax or 0.0
        total_amount = subtotal + tax

    currency = extracted.currency or "USD"
    tax_amount = extracted.tax or 0.0

    # Build line items from extracted data
    line_items = []
    for item in extracted.items:
        line_items.append({
            "description": item.get("Description", ""),
            "quantity": item.get("Quantity", 1),
            "unit_price": item.get("Price", 0.0),
            "amount": item.get("TotalPrice", 0.0),
        })

    # Calculate overall confidence from available scores
    confidence_scores = extracted.confidence_scores
    if confidence_scores:
        confidence = sum(confidence_scores.values()) / len(confidence_scores)
    else:
        confidence = 0.0

    raw_fields = {
        "merchant_name": extracted.merchant_name,
        "merchant_address": extracted.merchant_address,
        "transaction_date": extracted.transaction_date,
        "transaction_time": extracted.transaction_time,
        "subtotal": extracted.subtotal,
        "tax": extracted.tax,
        "total": extracted.total,
        "currency": extracted.currency,
    }

    expense = NormalizedExpense(
        expense_id=expense_id,
        document_type="receipt",
        vendor=vendor,
        date=date,
        total_amount=total_amount,
        currency=currency,
        tax_amount=tax_amount,
        line_items=line_items,
        raw_fields=raw_fields,
        confidence=confidence,
        metadata=metadata or {},
    )

    return expense


def normalize_expense_fields(
    extracted: Union[ExtractedInvoiceField, ExtractedReceiptField],
    document_id: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> NormalizedExpense:
    """
    Normalize extracted expense fields from either invoice or receipt into a standard schema.

    Auto-detects the type of extraction result and routes to the appropriate normalizer.

    Args:
        extracted: ExtractedInvoiceField or ExtractedReceiptField from Azure analysis.
        document_id: Optional document identifier.
        metadata: Optional additional metadata.

    Returns:
        NormalizedExpense with standardized field mapping.
    """
    if isinstance(extracted, ExtractedInvoiceField):
        return normalize_invoice_to_expense(extracted, document_id, metadata)
    elif isinstance(extracted, ExtractedReceiptField):
        return normalize_receipt_to_expense(extracted, document_id, metadata)
    else:
        raise ValueError(
            f"Unsupported extraction type: {type(extracted).__name__}. "
            "Expected ExtractedInvoiceField or ExtractedReceiptField."
        )


def expense_to_dict(expense: NormalizedExpense) -> dict:
    """
    Convert a NormalizedExpense to a dictionary for JSON serialization.

    Args:
        expense: NormalizedExpense instance.

    Returns:
        Dictionary representation suitable for JSON serialization.
    """
    return {
        "expense_id": expense.expense_id,
        "document_type": expense.document_type,
        "vendor": expense.vendor,
        "date": expense.date,
        "total_amount": expense.total_amount,
        "currency": expense.currency,
        "tax_amount": expense.tax_amount,
        "line_items": expense.line_items,
        "confidence": expense.confidence,
        "raw_fields": expense.raw_fields,
        "metadata": expense.metadata,
    }
