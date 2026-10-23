from typing import Dict, Any, Union
from pydantic import ValidationError
from document_models import InvoiceExtractionResponse, ReceiptExtractionResponse, ValidationResult


def validate_document_fields(
    extracted_data: Union[InvoiceExtractionResponse, ReceiptExtractionResponse],
    confidence_threshold: float = 0.8
) -> ValidationResult:
    errors = []
    confidence = 1.0

    if isinstance(extracted_data, InvoiceExtractionResponse):
        if not extracted_data.vendor:
            errors.append("Missing vendor name")
        if not extracted_data.date:
            errors.append("Missing invoice date")
        if extracted_data.total <= 0:
            errors.append("Invalid total amount")
        if len(extracted_data.line_items) == 0:
            errors.append("No line items found")

    elif isinstance(extracted_data, ReceiptExtractionResponse):
        if not extracted_data.merchant:
            errors.append("Missing merchant name")
        if extracted_data.total <= 0:
            errors.append("Invalid total amount")
        if len(extracted_data.items) == 0:
            errors.append("No items found")

    # Simulate confidence check (in practice, use provider's confidence scores)
    if hasattr(extracted_data, "_confidence"):
        confidence = extracted_data._confidence
        if confidence < confidence_threshold:
            errors.append(f"Low confidence score: {confidence}")

    return ValidationResult(
        is_valid=len(errors) == 0,
        errors=errors,
        confidence=confidence
    )