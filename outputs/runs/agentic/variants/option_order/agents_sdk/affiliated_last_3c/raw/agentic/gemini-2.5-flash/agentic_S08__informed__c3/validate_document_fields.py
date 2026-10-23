from typing import Dict, Any, List
from document_models import ExpenseDocument

def validate_document_fields(expense_doc: ExpenseDocument, required_fields: List[str]) -> Dict[str, Any]:
    """
    Validates required structured fields in an ExpenseDocument.
    """
    validation_results = {"is_valid": True, "missing_fields": [], "invalid_values": []}

    for field in required_fields:
        if not hasattr(expense_doc, field) or getattr(expense_doc, field) is None:
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)
        
        # Basic type validation example (can be expanded)
        if field == "total_amount" and getattr(expense_doc, field) is not None:
            if not isinstance(getattr(expense_doc, field), (int, float)):
                validation_results["is_valid"] = False
                validation_results["invalid_values"].append({"field": field, "reason": "Not a valid number"})
        
        if field == "line_items" and getattr(expense_doc, field) is not None:
            if not isinstance(getattr(expense_doc, field), list):
                validation_results["is_valid"] = False
                validation_results["invalid_values"].append({"field": field, "reason": "Not a list"})

    return validation_results
