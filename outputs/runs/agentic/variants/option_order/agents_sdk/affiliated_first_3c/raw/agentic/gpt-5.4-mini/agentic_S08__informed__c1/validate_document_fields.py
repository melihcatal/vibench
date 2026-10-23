from __future__ import annotations

from typing import Any, Dict, List

from document_models import ValidationResult, normalize_amount, normalize_text


def validate_document_fields(extracted: Dict[str, Any]) -> Dict[str, Any]:
    required = ["vendor", "date", "total"]
    missing: List[str] = []
    low_confidence: List[str] = []

    for field in required:
        value = extracted.get(field)
        if value in (None, "", [], {}):
            missing.append(field)

    confidence_map = extracted.get("field_confidence", {}) or {}
    for field in required:
        score = float(confidence_map.get(field, 1.0))
        if score < 0.75:
            low_confidence.append(field)

    valid = not missing and not low_confidence
    score = max(0.0, 1.0 - (0.2 * len(missing)) - (0.1 * len(low_confidence)))
    result = ValidationResult(valid=valid, missing_fields=missing, low_confidence_fields=low_confidence, score=score)
    return {
        "valid": result.valid,
        "missing_fields": result.missing_fields,
        "low_confidence_fields": result.low_confidence_fields,
        "score": result.score,
    }
