"""
Extract merchant, tax, total, and items from a receipt document
using Mindee's Receipt V5 OCR API.

Provider: Mindee Receipt OCR (mindee SDK)
Auth: MINDEE_API_KEY environment variable
"""

import os
from typing import Optional, Dict, Any

from mindee import Client

from document_client import (
    get_receipt_client,
    load_document_from_path,
    parse_receipt_response,
)
from document_models import (
    ReceiptFields,
    validate_required_fields,
    validate_confidence_scores,
)


def extract_receipt_fields(
    document_path: str,
    min_confidence: float = 0.5,
) -> Dict[str, Any]:
    """
    Extract structured fields from a receipt document using Mindee Receipt V5 API.

    Extracts merchant name, tax amount, total amount, and line item details.

    Args:
        document_path: Path to the receipt file (PDF, JPG, or PNG).
        min_confidence: Minimum confidence threshold for validation.

    Returns:
        Dictionary containing extracted receipt fields, validation results,
        and raw field data.

    Raises:
        FileNotFoundError: If document path does not exist.
        ValueError: If MINDEE_API_KEY is not set.
        Exception: If Mindee API call fails.
    """
    receipt_client = get_receipt_client()

    doc_bytes = load_document_from_path(document_path)

    response = receipt_client.parse(
        input_doc=doc_bytes,
        include_words=True,
    )

    extracted_fields = parse_receipt_response(response)

    receipt_required_keys = [
        "merchant_name",
        "total_amount",
        "total_tax",
    ]

    validation_result = validate_required_fields(
        extracted_fields,
        required_keys=receipt_required_keys,
        min_confidence=min_confidence,
    )

    confidence_check = validate_confidence_scores(
        extracted_fields,
        min_field_confidence=min_confidence,
    )

    result = {
        "document_type": "receipt",
        "extracted_fields": extracted_fields,
        "validation": {
            "required_fields": validation_result,
            "confidence": confidence_check,
        },
        "status": "success" if validation_result["valid"] else "validation_warnings",
    }

    return result


def extract_receipt_fields_from_bytes(
    document_bytes: bytes,
    filename: str = "receipt.png",
    min_confidence: float = 0.5,
) -> Dict[str, Any]:
    """
    Extract structured fields from receipt document bytes using Mindee API.

    Args:
        document_bytes: Raw bytes of the receipt document.
        filename: Suggested filename for the document.
        min_confidence: Minimum confidence threshold for validation.

    Returns:
        Dictionary containing extracted receipt fields and validation results.
    """
    receipt_client = get_receipt_client()

    response = receipt_client.parse(
        input_doc=document_bytes,
        include_words=True,
    )

    extracted_fields = parse_receipt_response(response)

    receipt_required_keys = [
        "merchant_name",
        "total_amount",
        "total_tax",
    ]

    validation_result = validate_required_fields(
        extracted_fields,
        required_keys=receipt_required_keys,
        min_confidence=min_confidence,
    )

    confidence_check = validate_confidence_scores(
        extracted_fields,
        min_field_confidence=min_confidence,
    )

    result = {
        "document_type": "receipt",
        "extracted_fields": extracted_fields,
        "validation": {
            "required_fields": validation_result,
            "confidence": confidence_check,
        },
        "status": "success" if validation_result["valid"] else "validation_warnings",
    }

    return result


def build_receipt_fields_model(
    extracted_fields: Dict[str, Any],
) -> ReceiptFields:
    """
    Convert extracted receipt dictionary to a ReceiptFields dataclass.

    Args:
        extracted_fields: Dictionary from extract_receipt_fields output.

    Returns:
        ReceiptFields dataclass instance.
    """
    from document_models import LineItem

    items = []
    for item in extracted_fields.get("items", []):
        items.append(
            LineItem(
                description=item.get("description"),
                quantity=item.get("quantity"),
                unit_price=item.get("unit_price"),
                total_amount=item.get("total_amount"),
                tax_rate=item.get("tax_rate"),
            )
        )

    return ReceiptFields(
        merchant_name=extracted_fields.get("merchant_name"),
        receipt_date=extracted_fields.get("receipt_date"),
        receipt_time=extracted_fields.get("receipt_time"),
        total_amount=extracted_fields.get("total_amount"),
        total_tax=extracted_fields.get("total_tax"),
        subtotal=extracted_fields.get("subtotal"),
        currency=extracted_fields.get("currency"),
        payment_method=extracted_fields.get("payment_method"),
        confidence=extracted_fields.get("confidence"),
        items=items,
    )
