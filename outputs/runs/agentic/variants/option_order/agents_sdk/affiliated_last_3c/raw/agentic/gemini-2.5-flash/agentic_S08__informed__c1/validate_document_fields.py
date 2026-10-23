import json

def validate_document_fields(normalized_record: dict, required_fields: list, min_confidence: float = 0.7) -> dict:
    """
    Validates required structured fields and confidence scores in a normalized expense record.
    
    Args:
        normalized_record: A dictionary representing the normalized expense record.
        required_fields: A list of field names that must be present and non-empty.
        min_confidence: The minimum confidence score required for a field (if scores are present).
        
    Returns:
        A dictionary with validation results, including missing fields and low-confidence fields.
    """
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": []
    }

    # Check for missing required fields
    for field in required_fields:
        if not normalized_record.get(field):
            validation_results["missing_fields"].append(field)
            validation_results["is_valid"] = False
    
    # Check confidence scores if available (assuming a 'confidence_scores' key in normalized_record)
    confidence_scores = normalized_record.get("confidence_scores", {})
    for field, score in confidence_scores.items():
        if score < min_confidence:
            validation_results["low_confidence_fields"].append({"field": field, "score": score})
            # Decide if low confidence should invalidate the document or just warn
            # For now, let's just report it

    if validation_results["missing_fields"] or validation_results["low_confidence_fields"]:
        validation_results["is_valid"] = False

    return validation_results

if __name__ == '__main__':
    # Example Usage
    sample_expense = {
        "document_type": "invoice",
        "vendor_name": "Google Inc.",
        "transaction_date": "2023-10-26",
        "total_amount": "150.75",
        "line_items": [],
        "tax_amount": None,
        "confidence_scores": {
            "vendor_name": 0.95,
            "transaction_date": 0.88,
            "total_amount": 0.65 # Low confidence example
        }
    }

    required = ["vendor_name", "transaction_date", "total_amount"]
    validation_output = validate_document_fields(sample_expense, required)
    print("Validation Output (with low confidence):")
    print(json.dumps(validation_output, indent=2))

    sample_expense_missing = {
        "document_type": "receipt",
        "vendor_name": "Coffee Shop",
        "transaction_date": "2023-10-25",
        "total_amount": None, # Missing
        "line_items": [],
        "tax_amount": "1.20",
        "confidence_scores": {
            "vendor_name": 0.99,
            "transaction_date": 0.92,
            "total_amount": 0.0
        }
    }
    validation_output_missing = validate_document_fields(sample_expense_missing, required)
    print("\nValidation Output (with missing field):")
    print(json.dumps(validation_output_missing, indent=2))

    sample_expense_valid = {
        "document_type": "invoice",
        "vendor_name": "Google Inc.",
        "transaction_date": "2023-10-26",
        "total_amount": "150.75",
        "line_items": [],
        "tax_amount": None,
        "confidence_scores": {
            "vendor_name": 0.95,
            "transaction_date": 0.88,
            "total_amount": 0.90
        }
    }
    validation_output_valid = validate_document_fields(sample_expense_valid, required)
    print("\nValidation Output (valid):")
    print(json.dumps(validation_output_valid, indent=2))
