from typing import Dict, Any, List, Optional
from document_models import DocumentValidationResult
from normalize_expense import NormalizedExpense

def validate_document_fields(normalized_expense: Dict[str, Any]) -> List[DocumentValidationResult]:
    validation_results: List[DocumentValidationResult] = []

    # Required fields for both invoices and receipts
    required_fields = {
        "vendor_merchant_name": {"min_confidence": 0.7, "type": str},
        "transaction_date": {"min_confidence": 0.7, "type": str},
        "total_amount": {"min_confidence": 0.7, "type": (int, float)},
    }

    # Simulate confidence for demonstration purposes, in a real scenario this would come from the extraction
    # For this exercise, we'll assume a high confidence if the field is present
    # and a low confidence if it's missing, to mimic a real validation.
    
    # Check for required fields and their simulated confidence
    for field_name, requirements in required_fields.items():
        field_value = normalized_expense.get(field_name)
        if field_value is None or (isinstance(field_value, str) and not field_value.strip()):
            validation_results.append(DocumentValidationResult(
                field_name=field_name,
                is_valid=False,
                confidence=0.1, # Low confidence for missing field
                message=f"Required field '{field_name}' is missing or empty."
            ))
        else:
            # Further validation can be added here, e.g., type checking, format checking
            if not isinstance(field_value, requirements["type"]):
                 validation_results.append(DocumentValidationResult(
                    field_name=field_name,
                    is_valid=False,
                    confidence=0.5, # Medium confidence for type mismatch
                    message=f"Field '{field_name}' has incorrect type. Expected {requirements['type']}, got {type(field_value)}."
                ))
            else:
                validation_results.append(DocumentValidationResult(
                    field_name=field_name,
                    is_valid=True,
                    confidence=0.95, # High confidence for present and seemingly valid field
                    message=f"Field '{field_name}' is present and valid."
                ))

    # Additional validation logic for specific document types or business rules can go here
    if normalized_expense.get("document_type") == "receipt":
        if normalized_expense.get("tax_amount") is None:
            validation_results.append(DocumentValidationResult(
                field_name="tax_amount",
                is_valid=False,
                confidence=0.3,
                message="Receipt is missing tax amount."
            ))
        else:
            validation_results.append(DocumentValidationResult(
                field_name="tax_amount",
                is_valid=True,
                confidence=0.9,
                message="Tax amount present."
            ))
            
    # For line items, we'll check if they are present and have some basic info
    if not normalized_expense.get("items"): # This covers both invoices (line_items) and receipts (items)
         validation_results.append(DocumentValidationResult(
            field_name="items",
            is_valid=False,
            confidence=0.2,
            message="No line items or items found."
        ))
    else:
        validation_results.append(DocumentValidationResult(
            field_name="items",
            is_valid=True,
            confidence=0.9,
            message="Line items or items found."
        ))

    return validation_results
