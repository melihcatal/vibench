import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class ValidationIssue:
    field: str
    message: str
    severity: str = "error"


@dataclass
class ValidationResult:
    valid: bool
    score: float
    issues: List[ValidationIssue]
    normalized: Dict[str, Any]


def _env_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return api_key


def _confidence_of(value: Any) -> Optional[float]:
    if isinstance(value, dict):
        for key in ("confidence", "score", "probability"):
            if key in value:
                try:
                    return float(value[key])
                except (TypeError, ValueError):
                    return None
    return None


def _is_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) > 0
    return True


def _flatten_fields(fields: Dict[str, Any], prefix: str = "") -> Iterable[Tuple[str, Any]]:
    for key, value in fields.items():
        path = f"{prefix}.{key}" if prefix else key
        yield path, value
        if isinstance(value, dict):
            yield from _flatten_fields(value, path)


def validate_document_fields(
    document: Dict[str, Any],
    required_fields: Sequence[str],
    min_confidence: float = 0.8,
) -> ValidationResult:
    issues: List[ValidationIssue] = []
    normalized = dict(document)
    score_parts: List[float] = []

    for field in required_fields:
        current: Any = document
        for part in field.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                current = None
                break

        if not _is_present(current):
            issues.append(ValidationIssue(field=field, message="missing required field"))
            score_parts.append(0.0)
            continue

        confidence = _confidence_of(current)
        if confidence is None:
            confidence = _confidence_of(document.get(field))
        if confidence is None and isinstance(current, dict):
            confidence = _confidence_of(current.get("metadata", {}))

        if confidence is None:
            issues.append(ValidationIssue(field=field, message="missing confidence score", severity="warning"))
            score_parts.append(0.5)
        else:
            score_parts.append(max(0.0, min(1.0, confidence)))
            if confidence < min_confidence:
                issues.append(
                    ValidationIssue(
                        field=field,
                        message=f"confidence below minimum threshold {min_confidence}",
                    )
                )

    if not score_parts:
        overall_score = 0.0
    else:
        overall_score = sum(score_parts) / len(score_parts)

    valid = not any(issue.severity == "error" for issue in issues)
    return ValidationResult(valid=valid, score=overall_score, issues=issues, normalized=normalized)


def validate_document_fields_with_openai(
    document: Dict[str, Any],
    required_fields: Sequence[str],
    min_confidence: float = 0.8,
) -> ValidationResult:
    api_key = _env_api_key()
    prompt = {
        "document": document,
        "required_fields": list(required_fields),
        "min_confidence": min_confidence,
        "task": "Validate required structured fields and confidence scores. Return JSON with keys valid, score, issues, normalized.",
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You validate structured document extraction output."},
                {"role": "user", "content": str(prompt)},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    if isinstance(content, dict):
        payload = content
    else:
        import json

        payload = json.loads(content)
    issues = [ValidationIssue(**item) for item in payload.get("issues", [])]
    normalized = payload.get("normalized", dict(document))
    return ValidationResult(
        valid=bool(payload.get("valid", False)),
        score=float(payload.get("score", 0.0)),
        issues=issues,
        normalized=normalized,
    )
