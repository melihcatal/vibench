from document_models import ExtractedDocument
from typing import Dict, Any

def validate_document_fields(extracted_document: ExtractedDocument, required_fields: list[str], min_confidence: float = 0.7) -> Dict[str, Any]:
    validation_results = {"is_valid": True, "missing_fields": [], "low_confidence_fields": []}

    # Check for missing required fields
    for field in required_fields:
        if not getattr(extracted_document, field, None):
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)

    # Check for low confidence fields
    for field, confidence in extracted_document.confidence.items():
        if confidence < min_confidence:
            validation_results["is_valid"] = False
            validation_results["low_confidence_fields"].append({"field": field, "confidence": confidence})

    return validation_results
