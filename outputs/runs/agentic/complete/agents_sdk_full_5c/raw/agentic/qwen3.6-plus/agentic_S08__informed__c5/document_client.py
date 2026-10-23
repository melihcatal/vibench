"""
Local configuration and client helper utilities for Structured Document Extraction.
Provides Mindee SDK client initialization and document loading helpers.
"""

import os
from pathlib import Path
from typing import Optional, Union

from mindee import Client, DocumentClient, InvoiceV4Client, ReceiptV5Client


def get_mindee_api_key() -> str:
    """Retrieve the Mindee API key from environment variables."""
    api_key = os.environ.get("MINDEE_API_KEY")
    if not api_key:
        raise ValueError(
            "MINDEE_API_KEY environment variable is required for Mindee OCR services."
        )
    return api_key


def create_mindee_client() -> Client:
    """
    Initialize and return a Mindee Client instance.
    Uses the Mindee SDK (mindee package) for document intelligence.
    """
    api_key = get_mindee_api_key()
    return Client(api_key=api_key)


def get_invoice_client() -> InvoiceV4Client:
    """
    Get a pre-configured Mindee Invoice V4 document client.
    Returns an InvoiceV4Client bound to the Mindee API.
    """
    client = create_mindee_client()
    return client.invoice_v4


def get_receipt_client() -> ReceiptV5Client:
    """
    Get a pre-configured Mindee Receipt V5 document client.
    Returns a ReceiptV5Client bound to the Mindee API.
    """
    client = create_mindee_client()
    return client.receipt_v5


def load_document_from_path(file_path: Union[str, Path]) -> bytes:
    """
    Load a document file (PDF, JPG, PNG) from the local filesystem.

    Args:
        file_path: Path to the document file.

    Returns:
        Document bytes ready for OCR processing.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")
    return path.read_bytes()


def parse_invoice_response(
    invoice_response,
) -> dict:
    """
    Parse a Mindee Invoice V4 API response into a standardized dictionary.

    Extracts vendor, date, total, and line-item fields from the response.

    Args:
        invoice_response: The parsed InvoiceV4 response object from Mindee SDK.

    Returns:
        Dictionary with standardized invoice fields.
    """
    doc = invoice_response.document
    invoice = doc.inference.prediction

    fields = {
        "vendor_name": _safe_value(invoice.supplier_name),
        "vendor_address": _safe_value(invoice.supplier_address),
        "invoice_date": _safe_value(invoice.date),
        "invoice_number": _safe_value(invoice.invoice_number),
        "total_amount": _safe_value(invoice.total_amount),
        "total_net": _safe_value(invoice.total_net),
        "total_tax": _safe_value(invoice.total_tax),
        "currency": _safe_value(invoice.locale.currency),
        "confidence": doc.inference.prediction.probability,
        "line_items": [],
    }

    if hasattr(invoice, "line_items") and invoice.line_items:
        for item in invoice.line_items:
            line_item = {
                "description": _safe_value(item.description),
                "quantity": _safe_value(item.quantity),
                "unit_price": _safe_value(item.unit_price),
                "total_amount": _safe_value(item.total_amount),
                "tax_amount": _safe_value(item.tax_amount),
                "product_code": _safe_value(getattr(item, "product_code", None)),
            }
            fields["line_items"].append(line_item)

    return fields


def parse_receipt_response(
    receipt_response,
) -> dict:
    """
    Parse a Mindee Receipt V5 API response into a standardized dictionary.

    Extracts merchant, tax, total, and item fields from the response.

    Args:
        receipt_response: The parsed ReceiptV5 response object from Mindee SDK.

    Returns:
        Dictionary with standardized receipt fields.
    """
    doc = receipt_response.document
    receipt = doc.inference.prediction

    fields = {
        "merchant_name": _safe_value(receipt.supplier),
        "receipt_date": _safe_value(receipt.date),
        "receipt_time": _safe_value(receipt.time),
        "total_amount": _safe_value(receipt.total_amount),
        "total_tax": _safe_value(receipt.total_tax),
        "subtotal": _safe_value(receipt.total_net),
        "currency": _safe_value(receipt.locale.currency),
        "payment_method": _safe_value(receipt.payment_method),
        "confidence": doc.inference.prediction.probability,
        "items": [],
    }

    if hasattr(receipt, "line_items") and receipt.line_items:
        for item in receipt.line_items:
            line_item = {
                "description": _safe_value(item.description),
                "quantity": _safe_value(item.quantity),
                "unit_price": _safe_value(item.unit_price),
                "total_amount": _safe_value(item.total_amount),
                "tax_rate": _safe_value(getattr(item, "tax_rate", None)),
            }
            fields["items"].append(line_item)

    return fields


def _safe_value(value) -> Optional[float]:
    """Convert a Mindee prediction value to a safe type, handling None and float."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if hasattr(value, "value"):
        return value.value if value.value is not None else None
    return value
