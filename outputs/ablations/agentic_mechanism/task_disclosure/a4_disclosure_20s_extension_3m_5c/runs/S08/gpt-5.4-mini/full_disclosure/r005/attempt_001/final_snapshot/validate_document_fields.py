import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


def _build_prompt(document_fields: Dict[str, Any], required_fields: List[str]) -> str:
    return (
        "Validate the following structured document fields and confidence scores. "
        "Return strict JSON with keys: valid, missing_fields, low_confidence_fields, issues. "
        "Treat a field as missing when its value is null, empty string, empty list, or empty object. "
        "Treat a field as low confidence when its confidence is missing or below 0.8. "
        "If a field has no confidence score, include it in low_confidence_fields when required. "
        "Document fields:\n\n"
        f"{json.dumps({'document_fields': document_fields, 'required_fields': required_fields}, ensure_ascii=False)}"
    )


def _extract_output_text(data: Dict[str, Any]) -> str:
    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")
    return output_text.strip()


def _fallback_validation(document_fields: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
    missing_fields = []
    low_confidence_fields = []
    issues = []
    for field in required_fields:
        value = document_fields.get(field)
        if value is None or value == "" or value == [] or value == {}:
            missing_fields.append(field)
            issues.append(f"Missing required field: {field}")
            continue
        confidence_key = f"{field}_confidence"
        confidence = document_fields.get(confidence_key)
        if confidence is None and isinstance(value, dict):
            confidence = value.get("confidence")
        if confidence is None or (isinstance(confidence, (int, float)) and confidence < 0.8):
            low_confidence_fields.append(field)
            if confidence is None:
                issues.append(f"Missing confidence for field: {field}")
            else:
                issues.append(f"Low confidence for field: {field}")
    return {
        "valid": not missing_fields and not low_confidence_fields,
        "missing_fields": missing_fields,
        "low_confidence_fields": low_confidence_fields,
        "issues": issues,
    }


def validate_document_fields(
    document_fields: Dict[str, Any],
    required_fields: Optional[List[str]] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    required = required_fields or ["vendor", "date", "total"]
    key = api_key or os.getenv(OPENAI_API_KEY_ENV)
    if not key:
        return _fallback_validation(document_fields, required)

    payload = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(document_fields, required),
        "temperature": 0,
    }
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output_text = _extract_output_text(data)
    if not output_text:
        return _fallback_validation(document_fields, required)

    try:
        parsed = json.loads(output_text)
    except Exception:
        return _fallback_validation(document_fields, required)

    fallback = _fallback_validation(document_fields, required)
    fallback.update({
        "valid": parsed.get("valid", fallback["valid"]),
        "missing_fields": parsed.get("missing_fields", fallback["missing_fields"]),
        "low_confidence_fields": parsed.get("low_confidence_fields", fallback["low_confidence_fields"]),
        "issues": parsed.get("issues", fallback["issues"]),
    })
    return fallback
