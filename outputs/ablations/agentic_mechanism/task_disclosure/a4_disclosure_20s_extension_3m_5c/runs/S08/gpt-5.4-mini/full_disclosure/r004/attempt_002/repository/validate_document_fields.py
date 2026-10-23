from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass(frozen=True)
class ValidationIssue:
    field: str
    code: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    issues: List[ValidationIssue]
    normalized: Dict[str, Any]


def _get_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")
    return api_key


def _confidence_value(value: Any) -> Optional[float]:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def _normalize_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(data)
    if "fields" not in normalized and any(k in normalized for k in ("vendor", "date", "total", "items")):
        normalized = {"fields": normalized}
    return normalized


def _required_field_issues(fields: Dict[str, Any], required_fields: Sequence[str]) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    for field in required_fields:
        value = fields.get(field)
        if value is None or value == "" or value == [] or value == {}:
            issues.append(ValidationIssue(field=field, code="missing_required_field", message=f"{field} is required"))
    return issues


def _confidence_issues(fields: Dict[str, Any], required_fields: Sequence[str], min_confidence: float) -> List[ValidationIssue]:
    issues: List[ValidationIssue] = []
    for field in required_fields:
        confidence = _confidence_value(fields.get(f"{field}_confidence", fields.get("confidence")))
        if confidence is None:
            issues.append(ValidationIssue(field=field, code="missing_confidence", message=f"{field} confidence is required"))
        elif confidence < min_confidence:
            issues.append(ValidationIssue(field=field, code="low_confidence", message=f"{field} confidence below threshold"))
    return issues


def validate_document_fields(
    payload: Dict[str, Any],
    required_fields: Optional[Sequence[str]] = None,
    min_confidence: float = 0.8,
) -> ValidationResult:
    normalized = _normalize_fields(payload)
    fields = normalized.get("fields", {})
    if not isinstance(fields, dict):
        raise TypeError("payload['fields'] must be a mapping")
    required_fields = tuple(required_fields or ("vendor", "date", "total"))
    issues = _required_field_issues(fields, required_fields)
    issues.extend(_confidence_issues(fields, required_fields, min_confidence))
    valid = len(issues) == 0
    return ValidationResult(valid=valid, issues=issues, normalized=normalized)


def validate_document_fields_with_openai(payload: Dict[str, Any], min_confidence: float = 0.8) -> ValidationResult:
    api_key = _get_api_key()
    body = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": "Validate structured document extraction output for required fields and confidence scores. Return JSON only.",
            },
            {
                "role": "user",
                "content": json.dumps({"payload": payload, "min_confidence": min_confidence}),
            },
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "document_validation",
                "schema": {
                    "type": "object",
                    "properties": {
                        "valid": {"type": "boolean"},
                        "issues": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "field": {"type": "string"},
                                    "code": {"type": "string"},
                                    "message": {"type": "string"},
                                },
                                "required": ["field", "code", "message"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["valid", "issues"],
                    "additionalProperties": False,
                },
            },
        },
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    text = ""
    for item in output:
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text += content.get("text", "")
    parsed = json.loads(text or "{}")
    issues = [ValidationIssue(**issue) for issue in parsed.get("issues", [])]
    return ValidationResult(valid=bool(parsed.get("valid", False)), issues=issues, normalized=_normalize_fields(payload))
