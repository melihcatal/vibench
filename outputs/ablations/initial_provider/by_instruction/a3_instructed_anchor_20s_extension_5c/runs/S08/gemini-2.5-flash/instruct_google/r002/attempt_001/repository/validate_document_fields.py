from typing import Dict, Any

def validate_expense_fields(expense_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates required structured fields and confidence scores in a normalized expense record.
    Returns a dictionary with validation results.
    """
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "validation_messages": []
    }

    required_fields = [
        ("document_type", "Document Type"),
        ("vendor_info.name", "Vendor Name"),
        ("transaction_date", "Transaction Date"),
        ("total_amount", "Total Amount"),
    ]

    for field_path, field_name in required_fields:
        current_value = expense_record
        path_parts = field_path.split('.')
        field_found = True
        for part in path_parts:
            if isinstance(current_value, dict) and part in current_value and current_value[part] is not None:
                current_value = current_value[part]
            else:
                field_found = False
                break
        
        if not field_found:
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field_name)
            validation_results["validation_messages"].append(f"Missing required field: {field_name}")

    # Basic confidence score check (assuming confidence scores are present in raw_extraction_data)
    # This is a placeholder and would need actual confidence score data from the extraction step
    if "raw_extraction_data" in expense_record and "confidence_scores" in expense_record["raw_extraction_data"]:
        for field, score in expense_record["raw_extraction_data"]["confidence_scores"].items():
            if score < 0.7:  # Example threshold
                validation_results["is_valid"] = False
                validation_results["low_confidence_fields"].append(field)
                validation_results["validation_messages"].append(f"Low confidence for field {field}: {score}")

    return validation_results
