"""
Validate required structured fields and confidence scores
for documents processed through Mindee OCR.

Provider: Mindee OCR (mindee SDK) — validation of Mindee extraction results
Auth: MINDEE_API_KEY environment variable
"""

import os
from typing import Dict, Any, List, Optional

from mindee import Client

from document_models import (
    validate_required_fields,
    validate_confidence_scores,
)


INVOICE_REQUIRED_FIELDS = [
    "vendor_name",
    "invoice_date",
    "total_amount",
]

RECEIPT_REQUIRED_FIELDS = [
    "merchant_name",
    "total_amount",
    "total_tax",
]


def validate_document_fields(
    extracted_fields: Dict[str, Any],
    document_type: str = "invoice",
    min_confidence: float = 0.5,
) -> Dict[str, Any]:
    """
    Validate required structured fields and confidence scores for a document.

    Checks that mandatory fields are present and that the overall document
    and field confidence scores meet the minimum threshold.

    Args:
        extracted_fields: Dictionary of extracted fields from Mindee OCR.
        document_type: "invoice" or "receipt" to determine required fields.
        min_confidence: Minimum confidence threshold (0.0 to 1.0).

    Returns:
        Validation result dictionary with:
            - valid: Boolean indicating if all checks passed.
            - missing_fields: List of missing required field names.
            - low_confidence_fields: List of fields below confidence threshold.
            - errors: List of error messages.
            - document_confidence: Overall document confidence score.
    """
    if document_type.lower() == "invoice":
        required_keys = INVOICE_REQUIRED_FIELDS
    elif document_type.lower() == "receipt":
        required_keys = RECEIPT_REQUIRED_FIELDS
    else:
        raise ValueError(
            f"Unsupported document type: {document_type}. "
            f"Use 'invoice' or 'receipt'."
        )

    required_validation = validate_required_fields(
        fields=extracted_fields,
        required_keys=required_keys,
        min_confidence=min_confidence,
    )

    confidence_validation = validate_confidence_scores(
        fields=extracted_fields,
        min_field_confidence=min_confidence,
    )

    all_valid = (
        required_validation["valid"]
        and confidence_validation["passes_threshold"]
    )

    errors = list(required_validation.get("errors", []))
    if not confidence_validation["passes_threshold"]:
        errors.append(
            f"Document confidence {confidence_validation.get('document_confidence', 'N/A')} "
            f"is below minimum {min_confidence}"
        )

    return {
        "valid": all_valid,
        "document_type": document_type,
        "required_fields": required_validation,
        "confidence_check": confidence_validation,
        "missing_fields": required_validation.get("missing_fields", []),
        "low_confidence_fields": confidence_validation.get("low_confidence_fields", []),
        "errors": errors,
    }


def validate_invoice_fields(
    extracted_fields: Dict[str, Any],
    min_confidence: float = 0.5,
) -> Dict[str, Any]:
    """
    Convenience function to validate invoice-specific fields.

    Args:
        extracted_fields: Extracted invoice fields from Mindee Invoice V4.
        min_confidence: Minimum confidence threshold.

    Returns:
        Validation result dictionary.
    """
    return validate_document_fields(
        extracted_fields=extracted_fields,
        document_type="invoice",
        min_confidence=min_confidence,
    )


def validate_receipt_fields(
    extracted_fields: Dict[str, Any],
    min_confidence: float = 0.5,
) -> Dict[str, Any]:
    """
    Convenience function to validate receipt-specific fields.

    Args:
        extracted_fields: Extracted receipt fields from Mindee Receipt V5.
        min_confidence: Minimum confidence threshold.

    Returns:
        Validation result dictionary.
    """
    return validate_document_fields(
        extracted_fields=extracted_fields,
        document_type="receipt",
        min_confidence=min_confidence,
    )


def get_field_confidence_report(
    extracted_fields: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate a detailed confidence report for all extracted fields.

    Args:
        extracted_fields: Dictionary of extracted fields from Mindee.

    Returns:
        Report with per-field confidence and overall assessment.
    """
    report = {
        "document_confidence": extracted_fields.get("confidence"),
        "fields": {},
    }

    for key, value in extracted_fields.items():
        if key in ("confidence", "line_items", "items", "vendor_address"):
            continue
        field_confidence = None
        if isinstance(value, dict) and "confidence" in value:
            field_confidence = value["confidence"]
        report["fields"][key] = {
            "value": value,
            "confidence": field_confidence,
            "present": value is not None,
        }

    return report
