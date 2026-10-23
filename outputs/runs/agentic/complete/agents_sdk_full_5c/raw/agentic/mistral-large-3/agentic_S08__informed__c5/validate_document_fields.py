from typing import Dict, Any, Union
from pydantic import ValidationError
from document_models import InvoiceExtractionResponse, ReceiptExtractionResponse, NormalizedExpense, ValidationResult


def validate_document_fields(
    extraction_result: Union[InvoiceExtractionResponse, ReceiptExtractionResponse],
    normalized_expense: NormalizedExpense
) -> ValidationResult:
    required_fields = {
        "vendor_merchant": str,
        "date": str,
        "total_amount": float
    }
    errors = []
    confidence = getattr(extraction_result, "confidence", 0.0)

    for field, field_type in required_fields.items():
        value = getattr(normalized_expense, field, None)
        if not value or not isinstance(value, field_type):
            errors.append(f"Missing or invalid {field}")

    if confidence < 0.7:
        errors.append(f"Low confidence score: {confidence}")

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        confidence=confidence
    )