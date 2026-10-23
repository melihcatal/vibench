from document_models import (
    NormalizedExpense,
    DocumentValidationResult,
    FieldValidationResult,
)
from typing import List


class DocumentValidator:
    def validate_expense(
        self,
        expense: NormalizedExpense,
        required_fields: List[str],
        min_confidence: float = 0.7,
    ) -> DocumentValidationResult:
        validation_errors = []
        is_valid = True

        for field in required_fields:
            field_value = getattr(expense, field, None)
            confidence_score = expense.confidence_scores.get(field, 0.0)

            if field_value is None:
                is_valid = False
                validation_errors.append(
                    FieldValidationResult(
                        field_name=field,
                        is_valid=False,
                        reason=f"Required field '{field}' is missing.",
                        confidence=confidence_score,
                    )
                )
            elif confidence_score < min_confidence:
                is_valid = False
                validation_errors.append(
                    FieldValidationResult(
                        field_name=field,
                        is_valid=False,
                        reason=f"Confidence score for '{field}' ({confidence_score:.2f}) is below minimum threshold ({min_confidence:.2f}).",
                        confidence=confidence_score,
                    )
                )

        return DocumentValidationResult(
            is_valid=is_valid, validation_errors=validation_errors
        )
