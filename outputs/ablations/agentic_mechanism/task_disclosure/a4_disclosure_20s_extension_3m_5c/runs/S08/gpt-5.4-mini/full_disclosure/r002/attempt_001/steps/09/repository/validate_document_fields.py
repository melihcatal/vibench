import os
from typing import Any, Dict, Iterable, List, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")
DEFAULT_REQUIRED_FIELDS = ("vendor", "date", "total")
MIN_CONFIDENCE = float(os.getenv("DOCUMENT_MIN_CONFIDENCE", "0.75"))


def _coerce_confidence(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        num = float(value)
    elif isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if not cleaned:
            return None
        try:
            num = float(cleaned)
        except ValueError:
            return None
    else:
        return None
    if num < 0:
        return 0.0
    if num > 1:
        if num <= 100:
            return num / 100.0
        return 1.0
    return num


def _missing_fields(document_fields: Dict[str, Any], required_fields: Iterable[str]) -> List[str]:
    missing = []
    for field in required_fields:
        value = document_fields.get(field)
        if value is None:
            missing.append(field)
        elif isinstance(value, str) and not value.strip():
            missing.append(field)
    return missing


def validate_document_fields(
    document_fields: Dict[str, Any],
    required_fields: Optional[Iterable[str]] = None,
    min_confidence: Optional[float] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    required = tuple(required_fields) if required_fields is not None else DEFAULT_REQUIRED_FIELDS
    threshold = MIN_CONFIDENCE if min_confidence is None else float(min_confidence)
    missing = _missing_fields(document_fields, required)
    confidence = _coerce_confidence(
        document_fields.get("confidence")
        or document_fields.get("overall_confidence")
        or document_fields.get("score")
    )
    confidence_ok = confidence is None or confidence >= threshold
    validation_payload = {
        "required_fields": list(required),
        "missing_fields": missing,
        "confidence": confidence,
        "min_confidence": threshold,
        "confidence_ok": confidence_ok,
        "document_fields": document_fields,
    }
    response = client.responses.create(
        model=model or DEFAULT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Validate structured document extraction results for required fields and confidence scores. Return a concise JSON-compatible assessment.",
            },
            {
                "role": "user",
                "content": str(validation_payload),
            },
        ],
    )
    text = getattr(response, "output_text", None)
    result = {
        "provider": "openai",
        "model": model or DEFAULT_MODEL,
        "required_fields": list(required),
        "missing_fields": missing,
        "confidence": confidence,
        "min_confidence": threshold,
        "confidence_ok": confidence_ok,
        "valid": not missing and confidence_ok,
    }
    if text:
        result["assessment"] = text
    return result
