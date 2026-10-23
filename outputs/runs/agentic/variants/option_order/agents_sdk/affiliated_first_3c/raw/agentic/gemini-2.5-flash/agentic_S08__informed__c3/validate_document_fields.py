from typing import List
from document_models import DocumentExtractionResult, ExtractedField, NormalizedExpense

def validate_document_fields(
    extraction_result: DocumentExtractionResult,
    required_fields: List[str],
    min_confidence: float = 0.7
) -> bool:
    is_valid = True

    for field_name in required_fields:
        if field_name not in extraction_result.fields or \
           extraction_result.fields[field_name].value is None or \
           (extraction_result.fields[field_name].confidence is not None and \
            extraction_result.fields[field_name].confidence < min_confidence):
            is_valid = False
            break

    # Optionally, validate line items if any are expected
    # This is a simple check; more complex validation could involve checking each line item's fields
    # if required_fields includes 'line_items' and extraction_result.line_items is empty
    if "line_items" in required_fields and not extraction_result.line_items:
        is_valid = False

    return is_valid

def update_validation_status(normalized_expense: NormalizedExpense, is_valid: bool) -> NormalizedExpense:
    if is_valid:
        normalized_expense.validation_status = "VALID"
    else:
        normalized_expense.validation_status = "INVALID"
    return normalized_expense
