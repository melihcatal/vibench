"""
Validate required structured fields and confidence scores from document extraction.

Validates that Azure AI Document Intelligence extraction results contain all
required fields with acceptable confidence scores before downstream processing.

Provider: Azure AI Document Intelligence (Form Recognizer)
SDK: azure-ai-documentintelligence
"""

from dataclasses import dataclass, field
from typing import Optional, Union

from document_models import (
    ExtractedInvoiceField,
    ExtractedReceiptField,
    validate_field_confidence,
)


INVOICE_REQUIRED_FIELDS = [
    "vendor_name",
    "invoice_date",
    "total",
]

RECEIPT_REQUIRED_FIELDS = [
    "merchant_name",
    "transaction_date",
    "total",
]


@dataclass
class ValidationResult:
    """Result of document field validation."""
    is_valid: bool
    document_type: str
    issues: list[str] = field(default_factory=list)
    confidence_scores: dict[str, float] = field(default_factory=dict)
    missing_fields: list[str] = field(default_factory=list)
    low_confidence_fields: list[str] = field(default_factory=list)


def validate_invoice_fields(
    extracted: ExtractedInvoiceField,
    required_fields: Optional[list[str]] = None,
    min_confidence: float = 0.7,
) -> ValidationResult:
    """
    Validate extracted invoice fields for completeness and confidence.

    Checks that required fields are present and their confidence scores
    meet the minimum threshold from Azure AI Document Intelligence.

    Args:
        extracted: ExtractedInvoiceField from Azure prebuilt-invoice model.
        required_fields: List of required field names. Defaults to INVOICE_REQUIRED_FIELDS.
        min_confidence: Minimum acceptable confidence score (0.0 to 1.0).

    Returns:
        ValidationResult indicating validity and any issues found.
    """
    fields_to_check = required_fields or INVOICE_REQUIRED_FIELDS

    is_valid, issues = validate_field_confidence(
        extracted.confidence_scores,
        fields_to_check,
        min_confidence,
    )

    missing = []
    low_conf = []
    for field_name in fields_to_check:
        if field_name not in extracted.confidence_scores:
            missing.append(field_name)
        elif extracted.confidence_scores[field_name] < min_confidence:
            low_conf.append(field_name)

    return ValidationResult(
        is_valid=is_valid,
        document_type="invoice",
        issues=issues,
        confidence_scores=extracted.confidence_scores,
        missing_fields=missing,
        low_confidence_fields=low_conf,
    )


def validate_receipt_fields(
    extracted: ExtractedReceiptField,
    required_fields: Optional[list[str]] = None,
    min_confidence: float = 0.7,
) -> ValidationResult:
    """
    Validate extracted receipt fields for completeness and confidence.

    Checks that required fields are present and their confidence scores
    meet the minimum threshold from Azure AI Document Intelligence.

    Args:
        extracted: ExtractedReceiptField from Azure prebuilt-receipt model.
        required_fields: List of required field names. Defaults to RECEIPT_REQUIRED_FIELDS.
        min_confidence: Minimum acceptable confidence score (0.0 to 1.0).

    Returns:
        ValidationResult indicating validity and any issues found.
    """
    fields_to_check = required_fields or RECEIPT_REQUIRED_FIELDS

    is_valid, issues = validate_field_confidence(
        extracted.confidence_scores,
        fields_to_check,
        min_confidence,
    )

    missing = []
    low_conf = []
    for field_name in fields_to_check:
        if field_name not in extracted.confidence_scores:
            missing.append(field_name)
        elif extracted.confidence_scores[field_name] < min_confidence:
            low_conf.append(field_name)

    return ValidationResult(
        is_valid=is_valid,
        document_type="receipt",
        issues=issues,
        confidence_scores=extracted.confidence_scores,
        missing_fields=missing,
        low_confidence_fields=low_conf,
    )


def validate_document_fields(
    extracted: Union[ExtractedInvoiceField, ExtractedReceiptField],
    required_fields: Optional[list[str]] = None,
    min_confidence: float = 0.7,
) -> ValidationResult:
    """
    Validate extracted document fields from either invoice or receipt.

    Auto-detects the document type and applies the appropriate validation rules
    for Azure AI Document Intelligence extraction results.

    Args:
        extracted: ExtractedInvoiceField or ExtractedReceiptField from Azure analysis.
        required_fields: Optional override for required field names.
        min_confidence: Minimum acceptable confidence score (0.0 to 1.0).

    Returns:
        ValidationResult indicating validity and any issues found.
    """
    if isinstance(extracted, ExtractedInvoiceField):
        return validate_invoice_fields(
            extracted,
            required_fields=required_fields,
            min_confidence=min_confidence,
        )
    elif isinstance(extracted, ExtractedReceiptField):
        return validate_receipt_fields(
            extracted,
            required_fields=required_fields,
            min_confidence=min_confidence,
        )
    else:
        raise ValueError(
            f"Unsupported extraction type: {type(extracted).__name__}. "
            "Expected ExtractedInvoiceField or ExtractedReceiptField."
        )


def format_validation_report(result: ValidationResult) -> dict:
    """
    Format validation result into a structured report dictionary.

    Args:
        result: ValidationResult from validation functions.

    Returns:
        Dictionary with formatted validation report.
    """
    return {
        "document_type": result.document_type,
        "is_valid": result.is_valid,
        "issues": result.issues,
        "missing_fields": result.missing_fields,
        "low_confidence_fields": result.low_confidence_fields,
        "confidence_scores": result.confidence_scores,
    }
