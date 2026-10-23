from typing import Dict, Any

def validate_document_fields(
    extracted_fields: Dict[str, Any],
    required_fields: list[str],
    min_confidence: float = 0.7,
) -> Dict[str, Any]:
    """
    Validates required structured fields and their confidence scores using Google Cloud Document AI concepts.

    Args:
        extracted_fields: A dictionary where keys are field names and values are dictionaries
                          containing 'value' and 'confidence' (e.g., {'vendor': {'value': 'ABC Corp', 'confidence': 0.95}}).
                          The 'confidence' field is inspired by Google Cloud Document AI's output.
        required_fields: A list of field names that must be present and meet the minimum confidence.
        min_confidence: The minimum confidence score required for a field to be considered valid.

    Returns:
        A dictionary containing validation results, indicating which fields are valid and
        which failed validation, along with reasons.
    """
    validation_results = {
        "is_valid": True,
        "failed_fields": {},
        "missing_fields": [],
    }

    for field in required_fields:
        if field not in extracted_fields:
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)
            continue

        field_data = extracted_fields[field]
        if not isinstance(field_data, dict) or "value" not in field_data:
            # Assume a structure where value is directly accessible if not a dict with 'value' and 'confidence'
            # This handles cases where confidence might not be provided for all fields
            validation_results["is_valid"] = False
            validation_results["failed_fields"][field] = "Field data is malformed or missing 'value'."
            continue

        confidence = field_data.get("confidence") # This key is specific to Google Cloud Document AI output structure
        if confidence is None:
            # If confidence is not provided, we can either assume it passes or fails depending on policy.
            # For this example, if it's a required field and no confidence, we treat it as potentially invalid
            validation_results["is_valid"] = False
            validation_results["failed_fields"][field] = "Confidence score is missing for this required field."
            continue

        if confidence < min_confidence:
            validation_results["is_valid"] = False
            validation_results["failed_fields"][field] = (
                f"Confidence ({confidence:.2f}) is below minimum required ({min_confidence:.2f})."
            )

    return validation_results

