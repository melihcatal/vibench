from typing import Dict, Any


def validate_document_fields(
    extracted_data: Dict[str, Any], required_fields: list
) -> Dict[str, Any]:
    """
    Validates required structured fields and confidence scores using AWS Textract confidence metrics.
    """
    missing_fields = []
    invalid_confidence = []

    for field in required_fields:
        if field not in extracted_data or extracted_data.get(field) is None:
            missing_fields.append(field)

    confidence = extracted_data.get("confidence", 0.0)
    if confidence < 0.7:
        invalid_confidence.append(
            f"Confidence score {confidence} is below threshold 0.7"
        )

    return {
        "is_valid": not missing_fields and not invalid_confidence,
        "missing_fields": missing_fields,
        "confidence_issues": invalid_confidence,
        "confidence_score": confidence,
    }
