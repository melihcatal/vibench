from document_models import NormalizedExpense
from typing import Dict, Any

def validate_document_fields(expense: NormalizedExpense, required_fields: list[str]) -> Dict[str, Any]:
    validation_results = {"is_valid": True, "missing_fields": [], "field_validations": {}}

    for field in required_fields:
        if not getattr(expense, field, None):
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)
            validation_results["field_validations"][field] = {"present": False, "reason": "missing"}
        else:
            validation_results["field_validations"][field] = {"present": True}
    
    # Placeholder for confidence score validation, if applicable in the future
    # if expense.raw_extraction_data and "confidence" in expense.raw_extraction_data:
    #     if expense.raw_extraction_data["confidence"] < 0.7: # Example threshold
    #         validation_results["is_valid"] = False
    #         validation_results["field_validations"]["document_confidence"] = {"valid": False, "reason": "low confidence"}

    expense.validation_results = validation_results
    return validation_results
