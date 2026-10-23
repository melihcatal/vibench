import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests


OPENAI_RESPONSES_API = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class ValidationResult:
    valid: bool
    missing_fields: List[str]
    low_confidence_fields: List[str]
    confidence_threshold: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.valid,
            "missing_fields": self.missing_fields,
            "low_confidence_fields": self.low_confidence_fields,
            "confidence_threshold": self.confidence_threshold,
        }


def _extract_value(document: Dict[str, Any], path: str) -> Any:
    current: Any = document
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _normalize_fields(required_fields: Iterable[str]) -> List[str]:
    return [field.strip() for field in required_fields if field and field.strip()]


def validate_document_fields(
    document: Dict[str, Any],
    required_fields: Iterable[str],
    confidence_threshold: float = 0.8,
) -> ValidationResult:
    missing_fields: List[str] = []
    low_confidence_fields: List[str] = []

    for field in _normalize_fields(required_fields):
        value = _extract_value(document, field)
        if value is None or value == "":
            missing_fields.append(field)
            continue

        confidence_key = f"{field}.confidence"
        confidence_value = _extract_value(document, confidence_key)
        if isinstance(confidence_value, (int, float)) and confidence_value < confidence_threshold:
            low_confidence_fields.append(field)

    return ValidationResult(
        valid=not missing_fields and not low_confidence_fields,
        missing_fields=missing_fields,
        low_confidence_fields=low_confidence_fields,
        confidence_threshold=confidence_threshold,
    )


def validate_with_openai(document: Dict[str, Any], required_fields: Iterable[str], confidence_threshold: float = 0.8) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI validation")

    prompt = {
        "document": document,
        "required_fields": _normalize_fields(required_fields),
        "confidence_threshold": confidence_threshold,
        "instruction": "Validate required structured fields and confidence scores. Return JSON only with missing_fields, low_confidence_fields, and valid.",
    }

    response = requests.post(
        OPENAI_RESPONSES_API,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": json.dumps(prompt),
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    text = ""
    if isinstance(data, dict):
        output = data.get("output", [])
        for item in output:
            content = item.get("content", []) if isinstance(item, dict) else []
            for block in content:
                if isinstance(block, dict) and block.get("type") in {"output_text", "text"}:
                    text += block.get("text", "")

    if not text:
        return validate_document_fields(document, required_fields, confidence_threshold).to_dict()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    return validate_document_fields(document, required_fields, confidence_threshold).to_dict()


__all__ = ["validate_document_fields", "validate_with_openai", "ValidationResult"]
