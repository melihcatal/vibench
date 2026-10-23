from __future__ import annotations

from typing import Any, Dict, List

from document_models import ValidationResult


def validate_document_fields(extracted: Dict[str, Any], required_fields: List[str] | None = None, min_confidence: float = 0.75) -> Dict[str, Any]:
    required_fields = required_fields or ["vendor", "date", "total"]
    missing = [field for field in required_fields if extracted.get(field) in (None, "")]
    low_conf = []
    confidence = extracted.get("confidence")
    if confidence is not None and confidence < min_confidence:
        low_conf.append("confidence")
    result = ValidationResult(valid=not missing and not low_conf, missing_fields=missing, low_confidence_fields=low_conf, details={"required_fields": required_fields, "min_confidence": min_confidence})
    return result.to_dict()
