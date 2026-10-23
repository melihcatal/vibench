"""
Validate required structured fields and confidence scores for extracted documents.

Uses Azure AI Content Safety / Azure Document Intelligence confidence thresholds
to validate document extraction results.

Provider: Azure AI validation (uses Azure Document Intelligence confidence scoring)
SDK: azure-ai-documentintelligence (for model references)
Auth: AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT, AZURE_DOCUMENT_INTELLIGENCE_KEY
"""

from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpense,
)


# Azure Document Intelligence prebuilt model confidence thresholds
DEFAULT_CONFIDENCE_THRESHOLD = 0.75
CRITICAL_CONFIDENCE_THRESHOLD = 0.90


@dataclass
class ValidationFieldIssue:
    """Represents a validation issue for a specific field."""
    field_name: str
    issue_type: str  # "missing", "low_confidence", "invalid_value"
    message: str
    confidence: Optional[float] = None
    is_critical: bool = False


@dataclass
class ValidationResult:
    """Overall validation result for a document extraction."""
    is_valid: bool
    issues: List[ValidationFieldIssue]
    document_type: str
    critical_failures: int = 0
    warnings: int = 0
    overall_confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "document_type": self.document_type,
            "overall_confidence": self.overall_confidence,
            "critical_failures": self.critical_failures,
            "warnings": self.warnings,
            "issues": [
                {
                    "field_name": issue.field_name,
                    "issue_type": issue.issue_type,
                    "message": issue.message,
                    "confidence": issue.confidence,
                    "is_critical": issue.is_critical,
                }
                for issue in self.issues
            ],
        }


# Required fields per document type (Azure Document Intelligence prebuilt model field mapping)
REQUIRED_INVOICE_FIELDS = {
    "vendor_name": {"critical": True, "confidence_threshold": CRITICAL_CONFIDENCE_THRESHOLD},
    "invoice_number": {"critical": True, "confidence_threshold": CRITICAL_CONFIDENCE_THRESHOLD},
    "invoice_date": {"critical": True, "confidence_threshold": DEFAULT_CONFIDENCE_THRESHOLD},
    "total_amount": {"critical": True, "confidence_threshold": CRITICAL_CONFIDENCE_THRESHOLD},
    "tax_amount": {"critical": False, "confidence_threshold": DEFAULT_CONFIDENCE_THRESHOLD},
}

REQUIRED_RECEIPT_FIELDS = {
    "merchant_name": {"critical": True, "confidence_threshold": CRITICAL_CONFIDENCE_THRESHOLD},
    "receipt_date": {"critical": True, "confidence_threshold": DEFAULT_CONFIDENCE_THRESHOLD},
    "total_amount": {"critical": True, "confidence_threshold": CRITICAL_CONFIDENCE_THRESHOLD},
    "tax_amount": {"critical": False, "confidence_threshold": DEFAULT_CONFIDENCE_THRESHOLD},
}


def validate_document_fields(
    extraction_result: Union[InvoiceExtractionResult, ReceiptExtractionResult],
    confidence_threshold: Optional[float] = None,
    strict_mode: bool = False,
) -> ValidationResult:
    """
    Validate required structured fields and confidence scores for extracted documents.

    Uses Azure Document Intelligence prebuilt-invoice/prebuilt-receipt field
    confidence scoring to validate extraction quality.

    Args:
        extraction_result: The extraction result to validate.
        confidence_threshold: Override default confidence threshold (0.75).
        strict_mode: If True, treat all low-confidence warnings as failures.

    Returns:
        ValidationResult with validation status and any issues found.
    """
    issues = []
    critical_count = 0
    warning_count = 0

    if isinstance(extraction_result, InvoiceExtractionResult):
        doc_type = "invoice"
        required_fields = REQUIRED_INVOICE_FIELDS
        field_values = _get_invoice_field_values(extraction_result)
    elif isinstance(extraction_result, ReceiptExtractionResult):
        doc_type = "receipt"
        required_fields = REQUIRED_RECEIPT_FIELDS
        field_values = _get_receipt_field_values(extraction_result)
    else:
        return ValidationResult(
            is_valid=False,
            issues=[ValidationFieldIssue(
                field_name="document",
                issue_type="invalid_type",
                message=f"Unsupported document type: {type(extraction_result).__name__}",
                is_critical=True,
            )],
            document_type="unknown",
            critical_failures=1,
        )

    # Validate each required field
    for field_name, config in required_fields.items():
        is_critical = config["critical"] or strict_mode
        threshold = config["confidence_threshold"]
        if confidence_threshold is not None:
            threshold = confidence_threshold

        value = field_values.get(field_name)
        confidence = field_values.get(f"{field_name}_confidence", 0.0)

        # Check if field is missing
        if value is None or (isinstance(value, str) and not value.strip()):
            issue = ValidationFieldIssue(
                field_name=field_name,
                issue_type="missing",
                message=f"Required field '{field_name}' is missing or empty",
                confidence=confidence,
                is_critical=is_critical,
            )
            issues.append(issue)
            if is_critical:
                critical_count += 1
            else:
                warning_count += 1
            continue

        # Check confidence score
        if confidence < threshold:
            severity = "critical" if is_critical else "warning"
            issue = ValidationFieldIssue(
                field_name=field_name,
                issue_type="low_confidence",
                message=(
                    f"Field '{field_name}' has low confidence "
                    f"({confidence:.2%} < {threshold:.2%})"
                ),
                confidence=confidence,
                is_critical=is_critical,
            )
            issues.append(issue)
            if is_critical:
                critical_count += 1
            else:
                warning_count += 1

    # Validate line items (if present)
    if isinstance(extraction_result, InvoiceExtractionResult):
        line_items = extraction_result.line_items
        item_label = "line_item"
    else:
        line_items = extraction_result.items
        item_label = "item"

    if line_items:
        for i, item in enumerate(line_items):
            if not item.description or not item.description.strip():
                issue = ValidationFieldIssue(
                    field_name=f"{item_label}_{i}.description",
                    issue_type="missing",
                    message=f"{item_label.title()} {i} is missing a description",
                    confidence=item.confidence,
                    is_critical=False,
                )
                issues.append(issue)
                warning_count += 1

    # Compute overall confidence
    overall_confidence = _compute_overall_confidence(field_values, required_fields)

    is_valid = critical_count == 0

    return ValidationResult(
        is_valid=is_valid,
        issues=issues,
        document_type=doc_type,
        critical_failures=critical_count,
        warnings=warning_count,
        overall_confidence=round(overall_confidence, 4),
    )


def validate_normalized_expense(
    normalized: NormalizedExpense,
    confidence_threshold: Optional[float] = None,
) -> ValidationResult:
    """
    Validate a NormalizedExpense record for completeness and quality.

    Args:
        normalized: The normalized expense record to validate.
        confidence_threshold: Override default confidence threshold.

    Returns:
        ValidationResult with validation status.
    """
    issues = []
    critical_count = 0

    required_fields = ["vendor_or_merchant", "document_date", "total"]
    for field_name in required_fields:
        value = getattr(normalized, field_name, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            issue = ValidationFieldIssue(
                field_name=field_name,
                issue_type="missing",
                message=f"Normalized expense is missing required field '{field_name}'",
                is_critical=True,
            )
            issues.append(issue)
            critical_count += 1

    if normalized.total is not None and normalized.total <= 0:
        issue = ValidationFieldIssue(
            field_name="total",
            issue_type="invalid_value",
            message="Total amount must be positive",
            confidence=normalized.confidence,
            is_critical=True,
        )
        issues.append(issue)
        critical_count += 1

    if normalized.confidence < (confidence_threshold or DEFAULT_CONFIDENCE_THRESHOLD):
        issue = ValidationFieldIssue(
            field_name="overall_confidence",
            issue_type="low_confidence",
            message=f"Overall confidence {normalized.confidence:.2%} is below threshold",
            confidence=normalized.confidence,
            is_critical=False,
        )
        issues.append(issue)

    return ValidationResult(
        is_valid=critical_count == 0,
        issues=issues,
        document_type=normalized.source_document_type or "expense",
        critical_failures=critical_count,
        overall_confidence=normalized.confidence,
    )


def validate_batch(
    results: List[Union[InvoiceExtractionResult, ReceiptExtractionResult]],
    confidence_threshold: Optional[float] = None,
) -> List[ValidationResult]:
    """Validate a batch of extraction results."""
    return [
        validate_document_fields(r, confidence_threshold)
        for r in results
    ]


def _get_invoice_field_values(result: InvoiceExtractionResult) -> Dict[str, Any]:
    """Extract field values and confidences from InvoiceExtractionResult."""
    return {
        "vendor_name": result.vendor_name,
        "vendor_name_confidence": result.vendor_confidence,
        "invoice_number": result.invoice_number,
        "invoice_number_confidence": result.invoice_number_confidence,
        "invoice_date": result.invoice_date,
        "invoice_date_confidence": result.invoice_date_confidence,
        "total_amount": result.total_amount,
        "total_amount_confidence": result.total_confidence,
        "tax_amount": result.tax_amount,
        "tax_amount_confidence": result.tax_confidence,
    }


def _get_receipt_field_values(result: ReceiptExtractionResult) -> Dict[str, Any]:
    """Extract field values and confidences from ReceiptExtractionResult."""
    return {
        "merchant_name": result.merchant_name,
        "merchant_name_confidence": result.merchant_confidence,
        "receipt_date": result.receipt_date,
        "receipt_date_confidence": result.receipt_date_confidence,
        "total_amount": result.total_amount,
        "total_amount_confidence": result.total_confidence,
        "tax_amount": result.tax_amount,
        "tax_amount_confidence": result.tax_confidence,
    }


def _compute_overall_confidence(
    field_values: Dict[str, Any],
    required_fields: Dict[str, dict],
) -> float:
    """Compute the overall confidence score from field confidences."""
    confidences = []
    for field_name in required_fields:
        conf_key = f"{field_name}_confidence"
        conf = field_values.get(conf_key, 0.0)
        if conf and conf > 0:
            confidences.append(conf)
    if confidences:
        return sum(confidences) / len(confidences)
    return 0.0
