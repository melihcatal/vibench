# [HELPER] document_models.py

# Local request, response, and normalization helpers for Structured Document Extraction

from typing import Dict, Any, List

# Standard expense schema used across later steps
StandardExpense = Dict[str, Any]

# Helper to build a request payload for Google Document AI (invoice format)
InvoicePayload = Dict[str, Any]


def build_invoice_request(file_path: str) -> InvoicePayload:
    """Construct a request payload for Google Document AI invoice extraction."""
    with open(file_path, "rb") as f:
        content = f.read()
    return {
        "document": {
            "content": content,
        },
        "parent": "projects/your-project/locations/us-central1",
        "features": ["INVOICE_DETECTION"],
    }


# Helper to build a request payload for Google Document AI receipt extraction
ReceiptPayload = Dict[str, Any]


def build_receipt_request(file_path: str) -> ReceiptPayload:
    with open(file_path, "rb") as f:
        content = f.read()
    return {
        "document": {
            "content": content,
        },
        "parent": "projects/your-project/locations/us-central1",
        "features": ["RECEIPT_DETECTION"],
    }


# Normalization uses the helper from normalize_expense.py
from normalize_expense import normalize_expense


def standardize_response(raw: Dict[str, Any]) -> StandardExpense:
    """Convert raw SDK response to the standard expense schema."""
    return normalize_expense(raw)
