from typing import Union
from document_models import InvoiceResponse, ReceiptResponse, ValidationResult


def validate_document_fields(
    extracted_data: Union[InvoiceResponse, ReceiptResponse],
    min_confidence: float = 0.7,
) -> ValidationResult:
    """
    Validates required structured fields and confidence scores using provider-agnostic rules.
    """
    errors = []
    is_valid = True

    if extracted_data.confidence < min_confidence:
        errors.append(f"Confidence score {extracted_data.confidence} below threshold {min_confidence}")
        is_valid = False

    if isinstance(extracted_data, InvoiceResponse):
        if not extracted_data.vendor:
            errors.append("Vendor field is missing")
            is_valid = False
        if not extracted_data.date:
            errors.append("Date field is missing")
            is_valid = False
        if extracted_data.total <= 0:
            errors.append("Total amount is invalid")
            is_valid = False
    else:
        if not extracted_data.merchant:
            errors.append("Merchant field is missing")
            is_valid = False
        if extracted_data.total <= 0:
            errors.append("Total amount is invalid")
            is_valid = False

    return ValidationResult(is_valid=is_valid, errors=errors)