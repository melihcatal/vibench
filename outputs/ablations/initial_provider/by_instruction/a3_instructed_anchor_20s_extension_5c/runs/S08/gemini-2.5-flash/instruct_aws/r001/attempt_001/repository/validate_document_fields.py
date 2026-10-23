from typing import Dict, Any

def validate_document_fields(normalized_data: Dict[str, Any], required_fields: list[str], min_confidence: float = 0.8) -> Dict[str, Any]:
    """
    Validates required structured fields and optionally checks confidence scores.
    Returns a dictionary with validation status and any missing/low-confidence fields.
    """
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": []
    }

    for field in required_fields:
        if field not in normalized_data or normalized_data[field] is None:
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)
        # Placeholder for confidence score validation. 
        # In a real scenario, confidence would be part of normalized_data.
        # For example: normalized_data[field]['confidence'] < min_confidence
        # if field in normalized_data and normalized_data[field] is not None and \
        #    isinstance(normalized_data[field], dict) and \
        #    normalized_data[field].get('confidence', 1.0) < min_confidence:
        #    validation_results["is_valid"] = False
        #    validation_results["low_confidence_fields"].append(field)

    # Example: Check line items if present and required
    if "line_items" in required_fields and not normalized_data.get("line_items"):
        validation_results["is_valid"] = False
        validation_results["missing_fields"].append("line_items")

    return validation_results
