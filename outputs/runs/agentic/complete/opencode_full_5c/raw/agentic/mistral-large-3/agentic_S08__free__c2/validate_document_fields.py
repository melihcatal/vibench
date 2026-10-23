from typing import Dict, Any, List
from document_models import DocumentField


def validate_document_fields(
    fields: Dict[str, DocumentField],
    required_fields: List[str],
    min_confidence: float = 0.7,
) -> Dict[str, Any]:
    """Validate required structured fields and confidence scores using Google Cloud Document AI confidence thresholds."""
    validation_result = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "fields": {},
    }

    for field_name in required_fields:
        if field_name not in fields:
            validation_result["is_valid"] = False
            validation_result["missing_fields"].append(field_name)
            continue

        field_data = fields[field_name]
        if field_data["confidence"] < min_confidence:
            validation_result["is_valid"] = False
            validation_result["low_confidence_fields"].append(
                {"field_name": field_name, "confidence": field_data["confidence"]}
            )

        validation_result["fields"][field_name] = {
            "value": field_data["value"],
            "confidence": field_data["confidence"],
        }

    return validation_result
