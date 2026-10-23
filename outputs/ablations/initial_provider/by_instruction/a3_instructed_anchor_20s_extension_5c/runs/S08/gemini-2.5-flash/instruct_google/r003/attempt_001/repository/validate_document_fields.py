from typing import List
from document_models import ExpenseNormalizationSchema

def validate_document_fields(expense_record: ExpenseNormalizationSchema, required_fields: List[str], min_confidence: float = 0.7) -> ExpenseNormalizationSchema:
    validation_errors = []

    for field in required_fields:
        field_value = getattr(expense_record, field, None)
        if field_value is None:
            validation_errors.append(f"Missing required field: {field}")
        
        # Check confidence score if available for the field
        if field in expense_record.confidence_scores:
            if expense_record.confidence_scores[field] < min_confidence:
                validation_errors.append(f"Low confidence for field {field}: {expense_record.confidence_scores[field]:.2f} (min {min_confidence:.2f})")

    if validation_errors:
        expense_record.validation_status = f"failed: {'; '.join(validation_errors)}"
    else:
        expense_record.validation_status = "validated"

    return expense_record
