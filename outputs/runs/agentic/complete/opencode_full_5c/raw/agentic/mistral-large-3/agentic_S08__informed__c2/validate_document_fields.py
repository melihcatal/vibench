from typing import Dict, Any, List


def validate_document_fields(
    extracted_data: Dict[str, Any], required_fields: List[str]
) -> Dict[str, Any]:
    """
    Validates required structured fields and confidence scores.
    """
    validation_result = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "confidence_score": 1.0,
    }

    # Check for missing fields
    for field in required_fields:
        if field not in extracted_data or not extracted_data.get(field):
            validation_result["is_valid"] = False
            validation_result["missing_fields"].append(field)

    # Check confidence score if provided
    confidence = extracted_data.get("confidence", 1.0)
    if confidence < 0.7:
        validation_result["is_valid"] = False
        validation_result["low_confidence_fields"].append("overall")
        validation_result["confidence_score"] = confidence

    # Provider-specific confidence checks
    if extracted_data.get("provider") == "google_document_ai":
        if confidence < 0.8:
            validation_result["is_valid"] = False
            validation_result["low_confidence_fields"].append("overall")
    elif extracted_data.get("provider") == "amazon_textract":
        if confidence < 0.75:
            validation_result["is_valid"] = False
            validation_result["low_confidence_fields"].append("overall")

    return validation_result
