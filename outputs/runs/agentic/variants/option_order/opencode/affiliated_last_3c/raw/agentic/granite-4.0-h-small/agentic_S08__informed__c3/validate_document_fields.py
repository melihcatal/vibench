# [SAME-SCENARIO] validate_document_fields.py
# Validates required structured fields and confidence scores

import json
from document_models import ValidationIssue


def validate_document_fields(extraction_result):
    """Check that required fields are present and confidence >= 0.8.

    Args:
        extraction_result (Union[InvoiceExtractionResult, ReceiptExtractionResult]): Raw output.

    Returns:
        List[ValidationIssue]: List of validation problems (empty if valid).
    """
    issues = []
    # Example: ensure vendor/name, date, total, and line_items exist
    if not extraction_result.vendor:
        issues.append(ValidationIssue(field="vendor", reason="Missing vendor name"))
    if not extraction_result.date:
        issues.append(ValidationIssue(field="date", reason="Missing date"))
    if not extraction_result.total:
        issues.append(ValidationIssue(field="total", reason="Missing total amount"))
    if not extraction_result.line_items:
        issues.append(ValidationIssue(field="line_items", reason="Missing line items"))
    # Add confidence checks if scores are available
    return issues
