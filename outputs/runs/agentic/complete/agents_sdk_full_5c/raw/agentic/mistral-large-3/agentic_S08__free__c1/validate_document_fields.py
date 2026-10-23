from typing import Dict, Any, Union
from pydantic import BaseModel, ValidationError, validator
from document_models import InvoiceExtractionResponse, ReceiptExtractionResponse


class FieldValidationResult(BaseModel):
    is_valid: bool
    missing_fields: list[str]
    confidence_scores: Dict[str, float]


def validate_document_fields(
    extracted_data: Union[InvoiceExtractionResponse, ReceiptExtractionResponse],
    confidence_threshold: float = 0.7,
) -> FieldValidationResult:
    missing_fields = []
    confidence_scores = {}

    if isinstance(extracted_data, InvoiceExtractionResponse):
        required_fields = {
            "vendor": extracted_data.vendor,
            "date": extracted_data.date,
            "total": extracted_data.total,
        }
        confidence_scores = {
            "vendor": 0.9,  # Placeholder for actual confidence from Google Document AI
            "date": 0.85,
            "total": 0.92,
        }

    elif isinstance(extracted_data, ReceiptExtractionResponse):
        required_fields = {
            "merchant": extracted_data.merchant,
            "total": extracted_data.total,
        }
        confidence_scores = {
            "merchant": 0.88,  # Placeholder for actual confidence from AWS Textract
            "total": 0.9,
        }
    else:
        raise ValueError("Unsupported extraction type")

    for field, value in required_fields.items():
        if not value:
            missing_fields.append(field)

    is_valid = all(
        confidence_scores.get(field, 0) >= confidence_threshold
        for field in required_fields
    )

    return FieldValidationResult(
        is_valid=is_valid,
        missing_fields=missing_fields,
        confidence_scores=confidence_scores,
    )