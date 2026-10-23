from typing import Dict, List

from google.cloud import documentai_v1 as documentai


VALIDATION_PROVIDER = "google.cloud.documentai.v1.DocumentProcessorServiceClient"


def validate_document_fields(payload: Dict[str, object]) -> Dict[str, object]:
    required = ["vendor", "date", "total"]
    missing: List[str] = [field for field in required if not payload.get(field)]
    confidences = payload.get("confidences", {}) if isinstance(payload.get("confidences"), dict) else {}
    low_confidence = [k for k, v in confidences.items() if isinstance(v, (int, float)) and v < 0.8]
    return {
        "valid": not missing and not low_confidence,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "provider": VALIDATION_PROVIDER,
        "documentai_type": documentai.Document.__name__,
    }
