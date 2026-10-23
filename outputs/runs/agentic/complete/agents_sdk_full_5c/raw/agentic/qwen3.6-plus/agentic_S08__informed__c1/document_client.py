"""
Local configuration and client helper utilities for Structured Document Extraction.

Provides Mindee Invoice API client setup, configuration loading, and shared
extraction helpers for document processing.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from mindee import Client, InvoicesV4PredictResponse


# Mindee API client configuration
MINDEE_API_KEY_ENV = "MINDEE_API_KEY"
MINDEE_DEFAULT_CONFIDENCE_THRESHOLD = 0.5


def get_mindee_api_key() -> str:
    """Retrieve Mindee API key from environment."""
    api_key = os.environ.get(MINDEE_API_KEY_ENV)
    if not api_key:
        raise EnvironmentError(
            f"Mindee API key not found. Set the {MINDEE_API_KEY_ENV} environment variable."
        )
    return api_key


def create_mindee_client(api_key: Optional[str] = None) -> Client:
    """
    Create and configure a Mindee client for Invoice OCR extraction.

    Uses the Mindee SDK (mindee package) with the v4 Invoice API.
    """
    key = api_key or get_mindee_api_key()
    client = Client(invoice_api_key=key)
    return client


def load_document_bytes(file_path: str) -> bytes:
    """Load document bytes from a local file path."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Document file not found: {file_path}")
    return path.read_bytes()


def detect_mime_type(file_path: str) -> str:
    """Detect MIME type based on file extension."""
    ext = Path(file_path).suffix.lower()
    mime_map = {
        ".pdf": "application/pdf",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".tiff": "image/tiff",
        ".tif": "image/tiff",
    }
    return mime_map.get(ext, "application/octet-stream")


def parse_mindee_invoice_response(response: InvoicesV4PredictResponse) -> Dict[str, Any]:
    """
    Parse Mindee Invoice v4 API response into a structured dictionary.

    Maps Mindee-specific field names to our internal schema fields.
    """
    prediction = response.document.inference.prediction

    result = {
        "raw_fields": {},
        "confidence_scores": {},
    }

    # Vendor information
    if prediction.supplier:
        supplier = prediction.supplier
        vendor_info = {
            "name": supplier.name.value if supplier.name else None,
            "address": supplier.address.value if supplier.address else None,
            "tax_id": supplier.tax_id.value if supplier.tax_id else None,
            "company_registration": supplier.company_registration.value if supplier.company_registration else None,
        }
        result["vendor"] = vendor_info

    # Invoice number
    if prediction.invoice_number:
        result["invoice_number"] = prediction.invoice_number.value
        result["confidence_scores"]["invoice_number"] = {
            "value": prediction.invoice_number.confidence,
            "label": "invoice_number",
        }
    else:
        result["invoice_number"] = None

    # Invoice date
    if prediction.date:
        result["invoice_date"] = prediction.date.value
        result["confidence_scores"]["invoice_date"] = {
            "value": prediction.date.confidence,
            "label": "invoice_date",
        }
    else:
        result["invoice_date"] = None

    # Due date
    if prediction.due_date:
        result["due_date"] = prediction.due_date.value
        result["confidence_scores"]["due_date"] = {
            "value": prediction.due_date.confidence,
            "label": "due_date",
        }
    else:
        result["due_date"] = None

    # Totals
    if prediction.total_amount:
        result["total_amount"] = str(prediction.total_amount.value)
        result["confidence_scores"]["total_amount"] = {
            "value": prediction.total_amount.confidence,
            "label": "total_amount",
        }
    else:
        result["total_amount"] = None

    if prediction.total_net:
        result["subtotal"] = str(prediction.total_net.value)
        result["confidence_scores"]["subtotal"] = {
            "value": prediction.total_net.confidence,
            "label": "subtotal",
        }
    else:
        result["subtotal"] = None

    if prediction.total_tax:
        result["tax_amount"] = str(prediction.total_tax.value)
        result["confidence_scores"]["tax_amount"] = {
            "value": prediction.total_tax.confidence,
            "label": "tax_amount",
        }
    else:
        result["tax_amount"] = None

    # Currency
    if prediction.locale:
        result["currency"] = prediction.locale.currency
        result["raw_fields"]["locale_language"] = prediction.locale.language

    # Line items
    line_items = []
    if prediction.line_items:
        for idx, item in enumerate(prediction.line_items):
            line_item = {
                "description": item.description if item.description else "",
                "quantity": float(item.quantity) if item.quantity else None,
                "unit_price": str(item.unit_price) if item.unit_price else None,
                "total_price": str(item.total_amount) if item.total_amount else None,
                "confidence": item.confidence if hasattr(item, "confidence") else None,
            }
            line_items.append(line_item)
    result["line_items"] = line_items

    # Store raw fields for debugging/auditing
    result["raw_fields"]["supplier"] = result.get("vendor")
    result["raw_fields"]["line_items_count"] = len(line_items)
    result["raw_fields"]["locale"] = prediction.locale.value if prediction.locale else None

    return result


def parse_mindee_receipt_response(response) -> Dict[str, Any]:
    """
    Parse Mindee Receipt v5 API response into a structured dictionary.

    Maps Mindee-specific field names to our internal schema fields.
    """
    prediction = response.document.inference.prediction

    result = {
        "raw_fields": {},
        "confidence_scores": {},
    }

    # Merchant information
    if prediction.supplier:
        supplier = prediction.supplier
        merchant_info = {
            "name": supplier.name.value if supplier.name else None,
            "address": supplier.address.value if supplier.address else None,
            "phone_number": supplier.phone_number.value if hasattr(supplier, "phone_number") and supplier.phone_number else None,
        }
        result["merchant"] = merchant_info
    else:
        result["merchant"] = None

    # Receipt date and time
    if prediction.date:
        result["receipt_date"] = prediction.date.value
        result["confidence_scores"]["receipt_date"] = {
            "value": prediction.date.confidence,
            "label": "receipt_date",
        }
    else:
        result["receipt_date"] = None

    if prediction.time:
        result["receipt_time"] = prediction.time.value
    else:
        result["receipt_time"] = None

    # Total
    if prediction.total_amount:
        result["total_amount"] = str(prediction.total_amount.value)
        result["confidence_scores"]["total_amount"] = {
            "value": prediction.total_amount.confidence,
            "label": "total_amount",
        }
    else:
        result["total_amount"] = None

    # Tax
    if prediction.taxes:
        total_tax = sum(t.value for t in prediction.taxes if t.value)
        result["tax_amount"] = str(total_tax)
        result["confidence_scores"]["tax_amount"] = {
            "value": prediction.taxes[0].confidence if prediction.taxes else 0.0,
            "label": "tax_amount",
        }
    else:
        result["tax_amount"] = None

    # Currency
    if prediction.locale:
        result["currency"] = prediction.locale.currency

    # Line items
    items = []
    if prediction.line_items:
        for item in prediction.line_items:
            line_item = {
                "description": item.description if item.description else "",
                "quantity": float(item.quantity) if item.quantity else None,
                "unit_price": str(item.unit_price) if item.unit_price else None,
                "total_price": str(item.total_amount) if item.total_amount else None,
                "confidence": item.confidence if hasattr(item, "confidence") else None,
            }
            items.append(line_item)
    result["items"] = items

    result["raw_fields"]["items_count"] = len(items)

    return result
