from document_models import NormalizedExpense
from typing import Dict, Any

def validate_document_fields(normalized_expense: NormalizedExpense) -> Dict[str, Any]:
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "validation_errors": []
    }

    # Example of required fields. This can be extended based on business rules.
    required_fields = [
        "total_amount",
        "transaction_date",
    ]

    if not normalized_expense.vendor_name and not normalized_expense.merchant_name:
        validation_results["missing_fields"].append("vendor_name or merchant_name")
        validation_results["is_valid"] = False

    for field in required_fields:
        if getattr(normalized_expense, field) is None:
            validation_results["missing_fields"].append(field)
            validation_results["is_valid"] = False
    
    # Basic numerical validation for total_amount and tax_amount if they exist
    if normalized_expense.total_amount:
        try:
            float(normalized_expense.total_amount)
        except ValueError:
            validation_results["validation_errors"].append("total_amount is not a valid number")
            validation_results["is_valid"] = False
    
    if normalized_expense.tax_amount:
        try:
            float(normalized_expense.tax_amount)
        except ValueError:
            validation_results["validation_errors"].append("tax_amount is not a valid number")
            validation_results["is_valid"] = False

    # In a real scenario, confidence scores from the original extraction would be passed through
    # and validated here as well.

    return validation_results
