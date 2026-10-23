import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


REQUIRED_FIELDS = ["document_type", "document_id", "date", "total_amount", "confidence"]


def _auth_headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _coerce_float(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
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


def _extract_output_text(payload: Dict[str, Any]) -> str:
    for item in payload.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    return text
    raise ValueError("No structured response content returned by OpenAI API")


def validate_document_fields(document: Dict[str, Any]) -> Dict[str, Any]:
    missing_fields: List[str] = [field for field in REQUIRED_FIELDS if document.get(field) in (None, "")]
    confidence = _coerce_float(document.get("confidence"))
    confidence_valid = confidence is not None and 0.0 <= confidence <= 1.0
    field_checks = {field: document.get(field) not in (None, "") for field in REQUIRED_FIELDS if field != "confidence"}
    field_checks["confidence"] = confidence_valid
    return {
        "valid": not missing_fields and confidence_valid,
        "missing_fields": missing_fields,
        "confidence": confidence,
        "confidence_valid": confidence_valid,
        "field_checks": field_checks,
        "document": document,
    }


def validate_document_fields_with_openai(document: Dict[str, Any]) -> Dict[str, Any]:
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": "Validate document records for required structured fields and confidence scores. Return strict JSON only.",
            },
            {
                "role": "user",
                "content": json.dumps({"document": document, "required_fields": REQUIRED_FIELDS}),
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "document_validation",
                "schema": {
                    "type": "object",
                    "properties": {
                        "valid": {"type": "boolean"},
                        "missing_fields": {"type": "array", "items": {"type": "string"}},
                        "confidence": {"type": ["number", "null"]},
                        "confidence_valid": {"type": "boolean"},
                        "field_checks": {
                            "type": "object",
                            "properties": {
                                "document_type": {"type": "boolean"},
                                "document_id": {"type": "boolean"},
                                "date": {"type": "boolean"},
                                "total_amount": {"type": "boolean"},
                                "confidence": {"type": "boolean"},
                            },
                            "required": ["document_type", "document_id", "date", "total_amount", "confidence"],
                            "additionalProperties": False,
                        },
                        "document": {"type": "object"},
                    },
                    "required": ["valid", "missing_fields", "confidence", "confidence_valid", "field_checks", "document"],
                    "additionalProperties": False,
                },
                "strict": True,
            }
        },
    }
    response = requests.post(OPENAI_API_URL, headers=_auth_headers(), data=json.dumps(payload), timeout=60)
    response.raise_for_status()
    return json.loads(_extract_output_text(response.json()))


def main() -> None:
    payload = json.loads(sys.stdin.read() or "{}")
    if os.environ.get("OPENAI_API_KEY"):
        result = validate_document_fields_with_openai(payload)
    else:
        result = validate_document_fields(payload)
    sys.stdout.write(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
