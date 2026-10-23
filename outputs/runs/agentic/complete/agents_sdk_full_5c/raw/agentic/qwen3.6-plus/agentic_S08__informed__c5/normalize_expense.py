"""
Normalize extracted expense fields into a standard JSON schema
using Mindee OCR extraction results.

Provider: Mindee OCR (mindee SDK) — normalization builds on Mindee-extracted fields
Auth: MINDEE_API_KEY environment variable
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, Union

from document_models import (
    NormalizedExpense,
    DocumentType,
    normalize_invoice_to_expense,
    normalize_receipt_to_expense,
)


def normalize_expense_fields(
    extracted_fields: Dict[str, Any],
    document_type: str = "invoice",
    expense_id: Optional[str] = None,
) -> NormalizedExpense:
    """
    Normalize extracted document fields into a standard expense record.

    Supports both invoice and receipt field schemas from Mindee OCR.
    The output conforms to a unified NormalizedExpense schema.

    Args:
        extracted_fields: Dictionary of fields extracted by Mindee OCR
                          (from extract_invoice_fields or extract_receipt_fields).
        document_type: Type of document — "invoice" or "receipt".
        expense_id: Optional unique expense identifier. Generated if not provided.

    Returns:
        NormalizedExpense dataclass instance with standardized fields.
    """
    if expense_id is None:
        expense_id = str(uuid.uuid4())

    if document_type.lower() == "invoice":
        return normalize_invoice_to_expense(
            invoice_fields=extracted_fields,
            expense_id=expense_id,
        )
    elif document_type.lower() == "receipt":
        return normalize_receipt_to_expense(
            receipt_fields=extracted_fields,
            expense_id=expense_id,
        )
    else:
        raise ValueError(
            f"Unsupported document type: {document_type}. "
            f"Use 'invoice' or 'receipt'."
        )


def normalize_to_json(
    extracted_fields: Dict[str, Any],
    document_type: str = "invoice",
    expense_id: Optional[str] = None,
    indent: int = 2,
) -> str:
    """
    Normalize extracted fields to a JSON string conforming to the expense schema.

    Args:
        extracted_fields: Dictionary of extracted fields from Mindee OCR.
        document_type: "invoice" or "receipt".
        expense_id: Optional unique identifier.
        indent: JSON indentation level.

    Returns:
        JSON string of the normalized expense record.
    """
    expense = normalize_expense_fields(
        extracted_fields=extracted_fields,
        document_type=document_type,
        expense_id=expense_id,
    )
    return expense.to_json(indent=indent)


def normalize_batch_expenses(
    documents: list,
    document_type: str = "invoice",
) -> list:
    """
    Normalize a batch of extracted document fields into expense records.

    Each document dict must contain extracted_fields and optionally expense_id.

    Args:
        documents: List of dicts with keys 'extracted_fields' and optional 'expense_id'.
        document_type: "invoice" or "receipt" for all documents in batch.

    Returns:
        List of NormalizedExpense dataclass instances.
    """
    normalized = []
    for doc in documents:
        expense = normalize_expense_fields(
            extracted_fields=doc["extracted_fields"],
            document_type=document_type,
            expense_id=doc.get("expense_id"),
        )
        normalized.append(expense)
    return normalized


def merge_expense_records(
    primary: NormalizedExpense,
    secondary: Dict[str, Any],
) -> NormalizedExpense:
    """
    Merge supplemental data into an existing normalized expense record.

    Useful for combining Mindee OCR extraction with manual corrections
    or additional metadata.

    Args:
        primary: Existing NormalizedExpense record.
        secondary: Dictionary of supplemental fields to merge.

    Returns:
        Updated NormalizedExpense with merged fields.
    """
    for key, value in secondary.items():
        if hasattr(primary, key) and value is not None:
            setattr(primary, key, value)

    primary.normalized_at = datetime.utcnow().isoformat()
    return primary


def expense_to_store_dict(
    expense: NormalizedExpense,
) -> Dict[str, Any]:
    """
    Convert a NormalizedExpense to a dictionary suitable for persistence.

    Args:
        expense: NormalizedExpense instance.

    Returns:
        Dictionary representation ready for storage in a document store.
    """
    return expense.to_dict()
