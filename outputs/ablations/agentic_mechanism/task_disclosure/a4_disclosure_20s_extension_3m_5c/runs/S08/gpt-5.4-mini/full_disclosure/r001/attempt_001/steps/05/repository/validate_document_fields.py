import json
import os
from typing import Any, Dict, List

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _to_float(value: Any):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip().replace(",", "")
        if not text:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    return None


def _collect_missing_fields(document: Dict[str, Any], required_fields: List[str]) -> List[str]:
    missing = []
    for field in required_fields:
        value = document.get(field)
        if value is None or value == "" or value == [] or value == {}:
            missing.append(field)
    return missing


def _collect_low_confidence_fields(document: Dict[str, Any], confidence_threshold: float) -> List[str]:
    low_confidence = []
    confidence_map = document.get("confidence")
    if not isinstance(confidence_map, dict):
        confidence_map = document.get("field_confidence") if isinstance(document.get("field_confidence"), dict) else {}
    for field, score in confidence_map.items():
        numeric_score = _to_float(score)
        if numeric_score is None or numeric_score < confidence_threshold:
            low_confidence.append(field)
    return low_confidence


def _local_validate(document: Dict[str, Any], required_fields: List[str], confidence_threshold: float) -> Dict[str, Any]:
    missing_fields = _collect_missing_fields(document, required_fields)
    low_confidence_fields = _collect_low_confidence_fields(document, confidence_threshold)
    valid = not missing_fields and not low_confidence_fields
    return {
        "provider": "openai",
        "model": OPENAI_MODEL,
        "valid": valid,
        "missing_fields": missing_fields,
        "low_confidence_fields": low_confidence_fields,
        "confidence_threshold": confidence_threshold,
    }


def _remote_validate(document: Dict[str, Any], required_fields: List[str], confidence_threshold: float) -> Dict[str, Any]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required for remote validation")

    schema = {
        "name": "document_field_validation",
        "schema": {
            "type": "object",
            "properties": {
                "provider": {"type": "string"},
                "model": {"type": "string"},
                "valid": {"type": "boolean"},
                "missing_fields": {"type": "array", "items": {"type": "string"}},
                "low_confidence_fields": {"type": "array", "items": {"type": "string"}},
                "confidence_threshold": {"type": "number"},
            },
            "required": ["provider", "model", "valid", "missing_fields", "low_confidence_fields", "confidence_threshold"],
            "additionalProperties": False,
        },
    }

    response = requests.post(
        f"{OPENAI_API_BASE}/responses",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": OPENAI_MODEL,
            "input": [
                {"role": "system", "content": "Validate required structured document fields and confidence scores."},
                {
                    "role": "user",
                    "content": json.dumps(
                        {"document": document, "required_fields": required_fields, "confidence_threshold": confidence_threshold},
                        ensure_ascii=False,
                    ),
                },
            ],
            "response_format": {"type": "json_schema", "json_schema": schema},
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = data.get("output_text")
    if text:
        return json.loads(text)
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                return json.loads(content.get("text", "{}"))
    raise RuntimeError("OpenAI validation response did not contain JSON output")


def validate_document_fields(document: Dict[str, Any], required_fields: List[str], confidence_threshold: float = 0.8, use_remote: bool = False) -> Dict[str, Any]:
    if use_remote:
        return _remote_validate(document, required_fields, confidence_threshold)
    return _local_validate(document, required_fields, confidence_threshold)
