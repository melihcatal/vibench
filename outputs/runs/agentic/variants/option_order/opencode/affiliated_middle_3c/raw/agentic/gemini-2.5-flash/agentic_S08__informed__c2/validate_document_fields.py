from typing import List, Dict, Any
from document_models import (
    DocumentValidationResponse,
    DocumentValidationResult,
    NormalizedExpense,
)


def validate_document_fields(
    expense_record: NormalizedExpense, required_fields: List[str]
) -> DocumentValidationResponse:
    validation_results = []
    is_valid = True

    record_dict = expense_record.dict()

    for field in required_fields:
        is_present = record_dict.get(field) is not None
        confidence = None  # In a real scenario, you might get confidence from the extraction step
        message = None

        if not is_present:
            is_valid = False
            message = f"Required field '{field}' is missing."

        validation_results.append(
            DocumentValidationResult(
                field_name=field,
                is_present=is_present,
                confidence=confidence,
                message=message,
            )
        )

    return DocumentValidationResponse(
        is_valid=is_valid, validation_results=validation_results
    )
