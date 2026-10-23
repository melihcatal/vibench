from document_models import NormalizedExpense, ValidationResult, LineItem
from typing import List


def validate_document_fields(
    expense: NormalizedExpense, required_fields: List[str], min_confidence: float = 0.7
) -> ValidationResult:
    """
    Validates required structured fields and confidence scores of a NormalizedExpense object.
    This validation applies to data previously extracted by services like Google Document AI or Amazon Textract.
    """
    missing_fields = []
    low_confidence_fields = []

    # Validate required fields
    if (
        "vendor_or_merchant_name" in required_fields
        and not expense.vendor_or_merchant_name
    ):
        missing_fields.append("vendor_or_merchant_name")
    if "transaction_date" in required_fields and not expense.transaction_date:
        missing_fields.append("transaction_date")
    if "total_amount" in required_fields and expense.total_amount is None:
        missing_fields.append("total_amount")

    # Validate confidence (example for overall extraction confidence)
    if expense.raw_extraction_confidence < min_confidence:
        low_confidence_fields.append("raw_extraction_confidence")

    is_valid = not missing_fields and not low_confidence_fields
    message = (
        "Document fields validated successfully." if is_valid else "Validation failed."
    )

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        message=message,
    )
