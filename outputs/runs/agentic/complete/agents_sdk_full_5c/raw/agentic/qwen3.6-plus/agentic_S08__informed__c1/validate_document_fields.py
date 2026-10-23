"""
[SAME-SCENARIO] Validate required structured fields and confidence scores from Mindee OCR extraction results.

Validates that extracted invoice and receipt documents from the Mindee Invoice OCR API
contain all required fields with acceptable confidence levels.
Provider: Mindee - Invoice/Receipt OCR validation
SDK: mindee (upstream dependency)
Auth: MINDEE_API_KEY
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    ValidationResult,
    ConfidenceScore,
    compute_overall_confidence,
)


# Default confidence threshold below which fields are flagged as low-confidence
DEFAULT_CONFIDENCE_THRESHOLD = 0.5

# Required fields for invoice extraction (Mindee invoice_v4 API)
REQUIRED_INVOICE_FIELDS = [
    "vendor",
    "invoice_date",
    "total_amount",
]

# Required fields for receipt extraction (Mindee expense_receipts_v5 API)
REQUIRED_RECEIPT_FIELDS = [
    "merchant",
    "receipt_date",
    "total_amount",
]

# High-value fields that should have higher confidence
HIGH_CONFIDENCE_FIELDS = [
    "total_amount",
    "invoice_number",
    "receipt_number",
    "invoice_date",
    "receipt_date",
    "tax_amount",
]


def _validate_required_fields(
    data: Dict[str, Any],
    required_fields: List[str],
) -> List[str]:
    """Check which required fields are missing or None."""
    missing = []
    for field in required_fields:
        value = data.get(field)
        if value is None:
            missing.append(field)
        elif isinstance(value, str) and not value.strip():
            missing.append(field)
    return missing


def _check_low_confidence(
    confidence_scores: Dict[str, ConfidenceScore],
    threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> List[str]:
    """Identify fields with confidence below the threshold."""
    low_conf = []
    for field_name, score in confidence_scores.items():
        if score.value < threshold:
            low_conf.append(field_name)
    return low_conf


def _check_high_confidence_fields(
    confidence_scores: Dict[str, ConfidenceScore],
    threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> List[str]:
    """Identify high-value fields with unacceptably low confidence."""
    warnings = []
    for field_name in HIGH_CONFIDENCE_FIELDS:
        score = confidence_scores.get(field_name)
        if score is not None and score.value < threshold:
            warnings.append(
                f"High-value field '{field_name}' has low confidence: {score.value:.2f}"
            )
    return warnings


def _get_all_fields_as_dict(extraction: Union[InvoiceExtractionResult, ReceiptExtractionResult]) -> Dict[str, Any]:
    """Convert extraction result to a flat dictionary for validation."""
    if hasattr(extraction, "model_dump"):
        return extraction.model_dump()
    elif hasattr(extraction, "dict"):
        return extraction.dict()
    return {}


def validate_document_fields(
    extraction: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    required_fields: Optional[List[str]] = None,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> ValidationResult:
    """
    Validate required structured fields and confidence scores from Mindee OCR extraction.

    Checks:
    - All required fields are present and non-empty
    - Confidence scores are above the configured threshold
    - High-value fields (total, date, number) have acceptable confidence

    Args:
        extraction: An InvoiceExtractionResult or ReceiptExtractionResult from Mindee.
        required_fields: Custom list of required field names. Defaults based on document type.
        confidence_threshold: Minimum acceptable confidence score (0.0 to 1.0).

    Returns:
        ValidationResult with is_valid flag, missing/low-confidence fields, and warnings.
    """
    data = _get_all_fields_as_dict(extraction)
    doc_type = data.get("document_type", extraction.document_type)

    if required_fields is None:
        if doc_type == "invoice":
            required_fields = REQUIRED_INVOICE_FIELDS
        elif doc_type == "receipt":
            required_fields = REQUIRED_RECEIPT_FIELDS
        else:
            required_fields = []

    confidence_scores = data.get("confidence_scores", {})
    if hasattr(confidence_scores, "items"):
        scores_dict = {}
        for k, v in confidence_scores.items():
            if isinstance(v, ConfidenceScore):
                scores_dict[k] = v
            elif isinstance(v, dict):
                scores_dict[k] = ConfidenceScore(value=v.get("value", 0.0), label=v.get("label", k))
        confidence_scores = scores_dict

    missing_fields = _validate_required_fields(data, required_fields)
    low_confidence_fields = _check_low_confidence(confidence_scores, confidence_threshold)
    high_conf_warnings = _check_high_confidence_fields(confidence_scores, confidence_threshold)

    overall_confidence = compute_overall_confidence(confidence_scores)

    is_valid = len(missing_fields) == 0

    errors = []
    if missing_fields:
        errors.append(f"Missing required fields: {', '.join(missing_fields)}")

    warnings = list(high_conf_warnings)
    if low_confidence_fields:
        warnings.append(
            f"Fields below confidence threshold ({confidence_threshold}): {', '.join(low_confidence_fields)}"
        )

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        errors=errors,
        warnings=warnings,
        overall_confidence=overall_confidence,
    )


def validate_invoice_fields(
    invoice: InvoiceExtractionResult,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> ValidationResult:
    """Validate an invoice extraction result from Mindee Invoice OCR."""
    return validate_document_fields(
        invoice,
        required_fields=REQUIRED_INVOICE_FIELDS,
        confidence_threshold=confidence_threshold,
    )


def validate_receipt_fields(
    receipt: ReceiptExtractionResult,
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD,
) -> ValidationResult:
    """Validate a receipt extraction result from Mindee Receipt OCR."""
    return validate_document_fields(
        receipt,
        required_fields=REQUIRED_RECEIPT_FIELDS,
        confidence_threshold=confidence_threshold,
    )
