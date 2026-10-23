import os
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _coerce_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        if isinstance(value, bool):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _field_value(data: Dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def _is_present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) > 0
    return True


def validate_document_fields(
    document: Dict[str, Any],
    required_fields: Optional[Iterable[str]] = None,
    confidence_threshold: float = 0.8,
) -> Dict[str, Any]:
    required_fields = list(required_fields or [])
    missing: List[str] = []
    low_confidence: List[Dict[str, Any]] = []
    present: List[str] = []

    for field in required_fields:
        value = _field_value(document, field)
        if not _is_present(value):
            missing.append(field)
            continue
        present.append(field)
        confidence = _coerce_float(_field_value(document, f"{field}_confidence"))
        if confidence is None:
            confidence = _coerce_float(_field_value(document, f"confidence.{field}"))
        if confidence is not None and confidence < confidence_threshold:
            low_confidence.append({"field": field, "confidence": confidence})

    score = 1.0
    if required_fields:
        score = max(0.0, (len(present) - len(low_confidence)) / max(1, len(required_fields)))

    return {
        "valid": not missing and not low_confidence,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "score": score,
        "required_fields": required_fields,
    }


def validate_document_fields_with_openai(
    document: Dict[str, Any],
    required_fields: Optional[Iterable[str]] = None,
    confidence_threshold: float = 0.8,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = {
        "document": document,
        "required_fields": list(required_fields or []),
        "confidence_threshold": confidence_threshold,
        "task": "Validate required structured fields and confidence scores",
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": [
                {
                    "role": "system",
                    "content": "Return only a compact JSON object with keys valid, missing_fields, low_confidence_fields, score.",
                },
                {"role": "user", "content": prompt},
            ],
            "text": {"format": {"type": "json_object"}},
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    for item in output:
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return {
                    "provider": "openai",
                    "model": OPENAI_MODEL,
                    "validation": content.get("text", {}),
                }
    return {"provider": "openai", "model": OPENAI_MODEL, "validation": data}
