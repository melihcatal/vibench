from document_models import NormalizedExpense, LineItem
from typing import Dict, Any

def validate_document_fields(expense: NormalizedExpense, required_fields: list[str]) -> Dict[str, Any]:
    validation_results = {"is_valid": True, "missing_fields": [], "confidence_scores": {}}

    # Basic field presence validation
    for field in required_fields:
        if not getattr(expense, field, None):
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)
    
    # Mock confidence score check (in a real scenario, Document AI provides confidence scores per entity)
    # For this example, we'll just set a dummy confidence for the presence of total_amount
    if expense.total_amount is not None:
        validation_results["confidence_scores"]["total_amount"] = 0.95 # High confidence if extracted
    else:
        validation_results["confidence_scores"]["total_amount"] = 0.0 # No confidence if not extracted

    # Add more sophisticated confidence checks here based on Document AI's output
    # For line items, you might iterate and check confidence for each line item's fields
    for i, item in enumerate(expense.line_items):
        if item.description:
            validation_results["confidence_scores"][f"line_item_{i}_description"] = 0.90
        if item.total_price:
            validation_results["confidence_scores"][f"line_item_{i}_total_price"] = 0.85


    return validation_results
