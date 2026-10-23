from typing import Dict, Any, List, Tuple
from document_models import InvoiceData, ReceiptData, ExtractedField, FieldConfidence


def validate_document_fields(
    extracted_data: Any, required_fields: List[str] = None, min_confidence: float = 0.7
) -> Tuple[bool, List[str]]:
    """
    Validate required structured fields and confidence scores.

    Args:
        extracted_data: InvoiceData, ReceiptData, or list of ExtractedField objects
        required_fields: List of required field names
        min_confidence: Minimum confidence threshold

    Returns:
        Tuple of (is_valid, list_of_validation_errors)
    """
    errors = []

    if required_fields is None:
        if isinstance(extracted_data, InvoiceData):
            required_fields = ["vendor_name", "invoice_date", "total_amount"]
        elif isinstance(extracted_data, ReceiptData):
            required_fields = ["merchant_name", "transaction_date", "total_amount"]
        else:
            required_fields = []

    if isinstance(extracted_data, InvoiceData):
        if not extracted_data.vendor_name:
            errors.append("Missing required field: vendor_name")
        if not extracted_data.invoice_date:
            errors.append("Missing required field: invoice_date")
        if extracted_data.total_amount <= 0:
            errors.append("Invalid total_amount (must be positive)")

        for field in extracted_data.extracted_fields:
            if field.confidence < min_confidence:
                errors.append(
                    f"Low confidence ({field.confidence:.2f}) for field: {field.name}"
                )

        if extracted_data.confidence_score < min_confidence:
            errors.append(
                f"Overall confidence score too low: {extracted_data.confidence_score:.2f}"
            )

    elif isinstance(extracted_data, ReceiptData):
        if not extracted_data.merchant_name:
            errors.append("Missing required field: merchant_name")
        if not extracted_data.transaction_date:
            errors.append("Missing required field: transaction_date")
        if extracted_data.total_amount <= 0:
            errors.append("Invalid total_amount (must be positive)")

        for field in extracted_data.extracted_fields:
            if field.confidence < min_confidence:
                errors.append(
                    f"Low confidence ({field.confidence:.2f}) for field: {field.name}"
                )

        if extracted_data.confidence_score < min_confidence:
            errors.append(
                f"Overall confidence score too low: {extracted_data.confidence_score:.2f}"
            )

    elif isinstance(extracted_data, list) and all(
        isinstance(f, ExtractedField) for f in extracted_data
    ):
        extracted_fields = extracted_data

        field_names = [f.name for f in extracted_fields]
        for required_field in required_fields:
            if required_field not in field_names:
                errors.append(f"Missing required field: {required_field}")

        for field in extracted_fields:
            if field.confidence < min_confidence:
                errors.append(
                    f"Low confidence ({field.confidence:.2f}) for field: {field.name}"
                )

    else:
        errors.append(f"Unsupported data type: {type(extracted_data)}")

    return len(errors) == 0, errors


def get_field_confidence_level(confidence_score: float) -> FieldConfidence:
    """
    Get confidence level enum from confidence score.

    Args:
        confidence_score: Confidence score (0.0 to 1.0)

    Returns:
        FieldConfidence enum value
    """
    if confidence_score >= 0.8:
        return FieldConfidence.HIGH
    elif confidence_score >= 0.6:
        return FieldConfidence.MEDIUM
    else:
        return FieldConfidence.LOW


def validate_extracted_field(
    field: ExtractedField, expected_type: type = None, min_confidence: float = 0.7
) -> Tuple[bool, List[str]]:
    """
    Validate a single extracted field.

    Args:
        field: ExtractedField object
        expected_type: Expected Python type for field value
        min_confidence: Minimum confidence threshold

    Returns:
        Tuple of (is_valid, list_of_validation_errors)
    """
    errors = []

    if not field.name:
        errors.append("Field name is empty")

    if field.value is None:
        errors.append(f"Field value is None for: {field.name}")

    if field.confidence < min_confidence:
        errors.append(f"Confidence too low: {field.confidence:.2f}")

    if expected_type and not isinstance(field.value, expected_type):
        errors.append(f"Expected type {expected_type}, got {type(field.value)}")

    return len(errors) == 0, errors


def calculate_overall_confidence(extracted_fields: List[ExtractedField]) -> float:
    """
    Calculate overall confidence score from extracted fields.

    Args:
        extracted_fields: List of ExtractedField objects

    Returns:
        Overall confidence score (0.0 to 1.0)
    """
    if not extracted_fields:
        return 0.0

    total_confidence = sum(field.confidence for field in extracted_fields)
    return total_confidence / len(extracted_fields)
