from __future__ import annotations

from typing import Any, Dict, Iterable, List

from document_models import ValidationIssue, ValidationResult


GOOGLE_DOCUMENTAI_VALIDATION_TAG = "google-documentai-structured-fields"


def validate_document_fields(
    payload: Dict[str, Any],
    required_fields: Iterable[str],
    minimum_confidence: float = 0.5,
) -> ValidationResult:
    issues: List[ValidationIssue] = []
    for field in required_fields:
        value = payload.get(field)
        if value in (None, "", []):
            issues.append(
                ValidationIssue(field=field, message="missing required field")
            )
    confidence_keys = [key for key in payload.keys() if key.endswith("_confidence")]
    for key in confidence_keys:
        try:
            score = float(payload[key])
        except (TypeError, ValueError):
            issues.append(
                ValidationIssue(field=key, message="invalid confidence score")
            )
            continue
        if score < minimum_confidence:
            issues.append(
                ValidationIssue(
                    field=key,
                    message=f"confidence below threshold for {GOOGLE_DOCUMENTAI_VALIDATION_TAG}",
                )
            )
    return ValidationResult(valid=not issues, issues=issues)
