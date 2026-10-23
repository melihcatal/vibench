from typing import Dict, Any, List
from document_models import NormalizedExpense, DocumentValidationResponse, ValidationResult
import os

# Placeholder for a conceptual external validation service API key
# In a real scenario, this might connect to a managed validation service like AWS Step Functions,
# Azure Logic Apps, or a custom microservice for data quality checks.
VALIDATION_SERVICE_API_KEY = os.environ.get("VALIDATION_SERVICE_API_KEY", "mock-validation-key")

def validate_document_fields(expense_record: NormalizedExpense, required_fields: List[str], min_confidence: float = 0.8) -> DocumentValidationResponse:
    validation_results: List[ValidationResult] = []
    is_document_valid = True

    for field_name in required_fields:
        field_value = getattr(expense_record, field_name, None)
        confidence = expense_record.confidence_scores.get(field_name, 0.0)

        is_valid = True
        reason = None

        if field_value is None:
            is_valid = False
            reason = f"Required field '{field_name}' is missing."
        elif confidence < min_confidence:
            is_valid = False
            reason = f"Confidence for field '{field_name}' ({confidence:.2f}) is below the minimum required ({min_confidence:.2f})."

        validation_results.append(ValidationResult(
            field_name=field_name,
            is_valid=is_valid,
            reason=reason,
            confidence=confidence
        ))

        if not is_valid:
            is_document_valid = False

    return DocumentValidationResponse(
        document_type=expense_record.document_type,
        is_valid=is_document_valid,
        validation_results=validation_results
    )
