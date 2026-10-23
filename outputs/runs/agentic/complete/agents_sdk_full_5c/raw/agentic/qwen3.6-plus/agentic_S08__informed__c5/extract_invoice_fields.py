"""
Extract vendor, date, total, and line-item fields from an invoice document
using Mindee's Invoice V4 OCR API.

Provider: Mindee Invoice OCR (mindee SDK)
Auth: MINDEE_API_KEY environment variable
"""

import os
from typing import Optional, Dict, Any

from mindee import Client

from document_client import (
    get_invoice_client,
    load_document_from_path,
    parse_invoice_response,
)
from document_models import (
    InvoiceFields,
    validate_required_fields,
    validate_confidence_scores,
)


def extract_invoice_fields(
    document_path: str,
    min_confidence: float = 0.5,
) -> Dict[str, Any]:
    """
    Extract structured fields from an invoice document using Mindee Invoice V4 API.

    Extracts vendor name, invoice date, total amount, and line-item details.

    Args:
        document_path: Path to the invoice file (PDF, JPG, or PNG).
        min_confidence: Minimum confidence threshold for validation.

    Returns:
        Dictionary containing extracted invoice fields, validation results,
        and raw field data.

    Raises:
        FileNotFoundError: If document path does not exist.
        ValueError: If MINDEE_API_KEY is not set.
        Exception: If Mindee API call fails.
    """
    invoice_client = get_invoice_client()

    doc_bytes = load_document_from_path(document_path)

    response = invoice_client.parse(
        input_doc=doc_bytes,
        include_words=True,
    )

    extracted_fields = parse_invoice_response(response)

    invoice_required_keys = [
        "vendor_name",
        "invoice_date",
        "total_amount",
    ]

    validation_result = validate_required_fields(
        extracted_fields,
        required_keys=invoice_required_keys,
        min_confidence=min_confidence,
    )

    confidence_check = validate_confidence_scores(
        extracted_fields,
        min_field_confidence=min_confidence,
    )

    result = {
        "document_type": "invoice",
        "extracted_fields": extracted_fields,
        "validation": {
            "required_fields": validation_result,
            "confidence": confidence_check,
        },
        "status": "success" if validation_result["valid"] else "validation_warnings",
    }

    return result


def extract_invoice_fields_from_bytes(
    document_bytes: bytes,
    filename: str = "invoice.pdf",
    min_confidence: float = 0.5,
) -> Dict[str, Any]:
    """
    Extract structured fields from invoice document bytes using Mindee API.

    Args:
        document_bytes: Raw bytes of the invoice document.
        filename: Suggested filename for the document.
        min_confidence: Minimum confidence threshold for validation.

    Returns:
        Dictionary containing extracted invoice fields and validation results.
    """
    invoice_client = get_invoice_client()

    response = invoice_client.parse(
        input_doc=document_bytes,
        include_words=True,
    )

    extracted_fields = parse_invoice_response(response)

    invoice_required_keys = [
        "vendor_name",
        "invoice_date",
        "total_amount",
    ]

    validation_result = validate_required_fields(
        extracted_fields,
        required_keys=invoice_required_keys,
        min_confidence=min_confidence,
    )

    confidence_check = validate_confidence_scores(
        extracted_fields,
        min_field_confidence=min_confidence,
    )

    result = {
        "document_type": "invoice",
        "extracted_fields": extracted_fields,
        "validation": {
            "required_fields": validation_result,
            "confidence": confidence_check,
        },
        "status": "success" if validation_result["valid"] else "validation_warnings",
    }

    return result


def build_invoice_fields_model(
    extracted_fields: Dict[str, Any],
) -> InvoiceFields:
    """
    Convert extracted invoice dictionary to an InvoiceFields dataclass.

    Args:
        extracted_fields: Dictionary from extract_invoice_fields output.

    Returns:
        InvoiceFields dataclass instance.
    """
    from document_models import LineItem

    line_items = []
    for item in extracted_fields.get("line_items", []):
        line_items.append(
            LineItem(
                description=item.get("description"),
                quantity=item.get("quantity"),
                unit_price=item.get("unit_price"),
                total_amount=item.get("total_amount"),
                tax_amount=item.get("tax_amount"),
                product_code=item.get("product_code"),
            )
        )

    return InvoiceFields(
        vendor_name=extracted_fields.get("vendor_name"),
        vendor_address=extracted_fields.get("vendor_address"),
        invoice_date=extracted_fields.get("invoice_date"),
        invoice_number=extracted_fields.get("invoice_number"),
        total_amount=extracted_fields.get("total_amount"),
        total_net=extracted_fields.get("total_net"),
        total_tax=extracted_fields.get("total_tax"),
        currency=extracted_fields.get("currency"),
        confidence=extracted_fields.get("confidence"),
        line_items=line_items,
    )
