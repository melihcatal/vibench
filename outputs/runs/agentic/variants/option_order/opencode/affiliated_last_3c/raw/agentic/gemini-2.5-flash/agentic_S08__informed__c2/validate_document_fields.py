from typing import Union
from document_models import (
    ExtractedInvoice,
    ExtractedReceipt,
    DocumentValidationResponse,
    ValidationResult,
)


def validate_document_fields(
    extracted_document: Union[ExtractedInvoice, ExtractedReceipt],
    required_fields: list[str],
    min_confidence: float = 0.7,
) -> DocumentValidationResponse:
    validation_results = []
    is_document_valid = True

    doc_dict = extracted_document.model_dump()

    for field_name in required_fields:
        field_present = False
        field_confident = False
        field_value = None
        confidence_score = None

        # Access DocumentField objects directly for confidence and value
        if field_name in doc_dict:
            field_data = getattr(extracted_document, field_name)
            if isinstance(field_data, DocumentField):
                field_value = field_data.value
                confidence_score = field_data.confidence
                field_present = field_value is not None
                field_confident = confidence_score >= min_confidence
            elif isinstance(field_data, (str, int, float, bool, list, dict)):
                # For fields that are not DocumentField, assume present and confident if not None
                field_value = field_data
                field_present = field_value is not None
                field_confident = (
                    True  # No confidence score for non-DocumentField fields
                )

        if not field_present:
            is_document_valid = False
            validation_results.append(
                ValidationResult(
                    field_name=field_name,
                    is_valid=False,
                    reason="Field is missing or empty",
                    extracted_value=field_value,
                    confidence=confidence_score,
                )
            )
        elif not field_confident:
            is_document_valid = False
            validation_results.append(
                ValidationResult(
                    field_name=field_name,
                    is_valid=False,
                    reason=f"Confidence score ({confidence_score:.2f}) below threshold ({min_confidence:.2f})",
                    extracted_value=field_value,
                    confidence=confidence_score,
                )
            )
        else:
            validation_results.append(
                ValidationResult(
                    field_name=field_name,
                    is_valid=True,
                    reason="Field is present and confident",
                    extracted_value=field_value,
                    confidence=confidence_score,
                )
            )

    return DocumentValidationResponse(
        is_document_valid=is_document_valid, validation_details=validation_results
    )
