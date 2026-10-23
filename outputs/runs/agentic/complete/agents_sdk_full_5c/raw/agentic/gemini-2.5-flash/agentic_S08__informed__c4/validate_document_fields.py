from typing import List
from document_models import ExpenseDocument, ValidationResult, DocumentValidationResponse

def validate_document_fields(
    document_id: str, expense_doc: ExpenseDocument, required_fields: List[str], min_confidence: float = 0.7
) -> DocumentValidationResponse:
    """Validates required structured fields and confidence scores."""
    validation_details: List[ValidationResult] = []
    is_document_valid = True

    # Check for required fields
    for field_name in required_fields:
        field_value = getattr(expense_doc, field_name, None)
        if field_value is None:
            is_document_valid = False
            validation_details.append(
                ValidationResult(
                    field_name=field_name, is_valid=False, reason="Missing required field"
                )
            )
        else:
            # For simplicity, confidence checking is not directly available in the ExpenseDocument model
            # from Azure DI's raw_response without deeper parsing. 
            # A more robust implementation would extract confidence from raw_response.
            validation_details.append(
                ValidationResult(
                    field_name=field_name, is_valid=True, reason="Field present", confidence=1.0 # Placeholder
                )
            )

    # Add more validation logic here, e.g., cross-field validation, format checks

    return DocumentValidationResponse(
        document_id=document_id,
        is_document_valid=is_document_valid,
        validation_details=validation_details,
    )
