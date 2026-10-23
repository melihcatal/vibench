from typing import Dict, Any, List
from document_models import ExtractionResult

def validate_document_fields(
    extraction_result: ExtractionResult,
    required_fields: List[str],
    min_confidence: float = 0.7
) -> Dict[str, Any]:
    validation_report = {
        "is_valid": True,
        "missing_fields": [],
        "low_confidence_fields": [],
        "overall_confidence_ok": True,
        "errors": []
    }

    if not extraction_result.success:
        validation_report["is_valid"] = False
        validation_report["errors"].append(f"Extraction failed: {extraction_result.error}")
        return validation_report

    extracted_data = extraction_result.data
    if not extracted_data:
        validation_report["is_valid"] = False
        validation_report["errors"].append("No data extracted.")
        return validation_report

    # Validate required fields presence
    for field in required_fields:
        if extracted_data.get(field) is None:
            validation_report["is_valid"] = False
            validation_report["missing_fields"].append(field)

    # Validate confidence (if available and relevant for the document type)
    # For simplicity, we assume a single overall confidence from the ExtractionResult
    # In a real scenario, confidence would be per-field or more granular.
    if extraction_result.confidence is not None and extraction_result.confidence < min_confidence:
        validation_report["is_valid"] = False
        validation_report["overall_confidence_ok"] = False
        validation_report["low_confidence_fields"].append(f"Overall confidence ({extraction_result.confidence:.2f}) below threshold ({min_confidence:.2f})")

    return validation_report
