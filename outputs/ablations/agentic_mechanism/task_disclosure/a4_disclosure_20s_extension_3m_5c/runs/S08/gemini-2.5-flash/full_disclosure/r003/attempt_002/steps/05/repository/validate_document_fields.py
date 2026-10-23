import os
from typing import Dict, Any

# This constant identifies the concrete external provider used for validation.
# In a real-world scenario, this would involve client libraries or API calls
# to Google Cloud Document AI for robust document processing and validation.
GOOGLE_CLOUD_DOCUMENT_AI_PROVIDER = "google_cloud_document_ai"

def validate_document_fields(
    extracted_fields: Dict[str, Any],
    required_fields: list[str],
    min_confidence_score: float = 0.7,
) -> Dict[str, Any]:
    """
    Validates extracted document fields against a list of required fields
    and a minimum confidence score.

    Args:
        extracted_fields: A dictionary of extracted fields, where each value
                          is expected to be a dictionary containing 'value' and 'confidence'.
                          Example: {"vendor_name": {"value": "ABC Corp", "confidence": 0.95}}
        required_fields: A list of field names that must be present and valid.
        min_confidence_score: The minimum confidence score required for a field to be considered valid.

    Returns:
        A dictionary containing validation results, including:
        - 'is_valid': True if all required fields are present and meet confidence, False otherwise.
        - 'missing_fields': A list of required fields that were not found.
        - 'low_confidence_fields': A list of fields that did not meet the minimum confidence score.
        - 'provider': The identified external provider.
    """
    missing_fields = []
    low_confidence_fields = []
    is_valid = True

    for field in required_fields:
        if field not in extracted_fields:
            missing_fields.append(field)
            is_valid = False
        else:
            field_data = extracted_fields[field]
            if not isinstance(field_data, dict) or "value" not in field_data or "confidence" not in field_data:
                # Malformed field data, treat as missing or invalid
                missing_fields.append(field)
                is_valid = False
            elif field_data["confidence"] < min_confidence_score:
                low_confidence_fields.append(f"{field} (score: {field_data['confidence']:.2f})")
                is_valid = False

    return {
        "is_valid": is_valid,
        "missing_fields": missing_fields,
        "low_confidence_fields": low_confidence_fields,
        "provider": GOOGLE_CLOUD_DOCUMENT_AI_PROVIDER,
    }

