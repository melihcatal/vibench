"""Validate required structured fields and confidence scores for extracted documents."""

import os
from typing import List, Optional
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_models import (
    FieldValidation,
    DocumentValidationResult,
    InvoiceExtractionResult,
    ReceiptExtractionResult,
)
from document_client import get_document_intelligence_client


REQUIRED_INVOICE_FIELDS = [
    "VendorName",
    "InvoiceDate",
    "InvoiceTotal",
]

REQUIRED_RECEIPT_FIELDS = [
    "MerchantName",
    "Total",
]

MIN_CONFIDENCE_THRESHOLD = 0.5


def validate_invoice_fields(
    extraction: InvoiceExtractionResult,
    min_confidence: float = MIN_CONFIDENCE_THRESHOLD,
) -> DocumentValidationResult:
    """Validate that all required invoice fields are present with sufficient confidence.

    Uses Azure Document Intelligence field names for validation criteria.
    """
    field_validations = []
    errors = []

    raw = extraction.raw_fields or {}

    for field_name in REQUIRED_INVOICE_FIELDS:
        raw_field = raw.get(field_name)
        present = raw_field is not None and raw_field != ""

        field_val = FieldValidation(
            field_name=field_name,
            present=present,
            value=raw_field if present else None,
            confidence=extraction.confidence if present else 0.0,
        )

        if not present:
            field_val.valid = False
            field_val.errors.append(f"Required field '{field_name}' is missing")
            errors.append(f"Missing: {field_name}")
        elif field_val.confidence < min_confidence:
            field_val.valid = False
            field_val.errors.append(
                f"Field '{field_name}' confidence {field_val.confidence:.2f} "
                f"below threshold {min_confidence}"
            )
            errors.append(f"Low confidence: {field_name} ({field_val.confidence:.2f})")

        field_validations.append(field_val)

    all_present = all(fv.present for fv in field_validations)
    all_confident = all(
        fv.confidence >= min_confidence for fv in field_validations if fv.present
    )
    valid = all_present and all_confident

    return DocumentValidationResult(
        document_type="invoice",
        all_required_present=all_present,
        overall_confidence=extraction.confidence,
        field_validations=field_validations,
        valid=valid,
        errors=errors,
    )


def validate_receipt_fields(
    extraction: ReceiptExtractionResult,
    min_confidence: float = MIN_CONFIDENCE_THRESHOLD,
) -> DocumentValidationResult:
    """Validate that all required receipt fields are present with sufficient confidence.

    Uses Azure Document Intelligence field names for validation criteria.
    """
    field_validations = []
    errors = []

    raw = extraction.raw_fields or {}

    for field_name in REQUIRED_RECEIPT_FIELDS:
        raw_field = raw.get(field_name)
        present = raw_field is not None and raw_field != ""

        field_val = FieldValidation(
            field_name=field_name,
            present=present,
            value=raw_field if present else None,
            confidence=extraction.confidence if present else 0.0,
        )

        if not present:
            field_val.valid = False
            field_val.errors.append(f"Required field '{field_name}' is missing")
            errors.append(f"Missing: {field_name}")
        elif field_val.confidence < min_confidence:
            field_val.valid = False
            field_val.errors.append(
                f"Field '{field_name}' confidence {field_val.confidence:.2f} "
                f"below threshold {min_confidence}"
            )
            errors.append(f"Low confidence: {field_name} ({field_val.confidence:.2f})")

        field_validations.append(field_val)

    all_present = all(fv.present for fv in field_validations)
    all_confident = all(
        fv.confidence >= min_confidence for fv in field_validations if fv.present
    )
    valid = all_present and all_confident

    return DocumentValidationResult(
        document_type="receipt",
        all_required_present=all_present,
        overall_confidence=extraction.confidence,
        field_validations=field_validations,
        valid=valid,
        errors=errors,
    )


def validate_document_fields(
    extraction,
    document_type: str = "invoice",
    min_confidence: float = MIN_CONFIDENCE_THRESHOLD,
) -> DocumentValidationResult:
    """Validate structured fields based on document type.

    Routes to the appropriate validation function for invoice or receipt data.
    """
    if document_type.lower() == "receipt":
        return validate_receipt_fields(extraction, min_confidence=min_confidence)
    return validate_invoice_fields(extraction, min_confidence=min_confidence)


if __name__ == "__main__":
    from extract_invoice_fields import extract_invoice_fields
    import sys

    if len(sys.argv) > 1:
        extracted = extract_invoice_fields(sys.argv[1])
        result = validate_document_fields(extracted, document_type="invoice")
        print(result.model_dump_json(indent=2))
