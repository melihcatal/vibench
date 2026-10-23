from google.cloud import documentai

def validate_document_fields(extracted_data: dict, required_fields: list, confidence_threshold: float = 0.7) -> dict:
    """
    Validates required structured fields and their confidence scores.

    Args:
        extracted_data: A dictionary where keys are field names and values are
                        dictionaries containing 'value' and 'confidence'.
        required_fields: A list of field names that are required.
        confidence_threshold: The minimum confidence score required for a field to be considered valid.

    Returns:
        A dictionary with validation results, including an overall 'is_valid' status
        and detailed status for each required field.
    """
    validation_results = {
        "is_valid": True,
        "field_validations": {}
    }

    for field in required_fields:
        if field not in extracted_data:
            validation_results["is_valid"] = False
            validation_results["field_validations"][field] = {
                "present": False,
                "confidence_met": False,
                "message": f"Required field '{field}' is missing."
            }
        else:
            field_data = extracted_data[field]
            is_present = True
            confidence = field_data.get("confidence", 0.0)
            confidence_met = confidence >= confidence_threshold

            if not confidence_met:
                validation_results["is_valid"] = False
                validation_results["field_validations"][field] = {
                    "present": is_present,
                    "confidence_met": False,
                    "confidence_score": confidence,
                    "message": f"Confidence for '{field}' ({confidence:.2f}) is below threshold ({confidence_threshold:.2f})."
                }
            else:
                validation_results["field_validations"][field] = {
                    "present": is_present,
                    "confidence_met": True,
                    "confidence_score": confidence,
                    "message": f"Field '{field}' is present and confidence met."
                }
    return validation_results
