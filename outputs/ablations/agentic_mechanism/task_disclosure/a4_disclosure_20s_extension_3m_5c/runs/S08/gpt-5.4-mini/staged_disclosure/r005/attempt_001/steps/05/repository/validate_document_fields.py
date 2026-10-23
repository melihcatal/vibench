import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODEL = "openai/gpt-5.4-mini"


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
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


def _normalize_fields(document: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(document, dict):
        raise ValueError("document must be a JSON object")
    fields = document.get("fields")
    if not isinstance(fields, dict):
        raise ValueError("document.fields must be a JSON object")
    return fields


def validate_document_fields(document: Dict[str, Any], required_fields: List[str], min_confidence: float = 0.8) -> Dict[str, Any]:
    fields = _normalize_fields(document)
    missing = []
    low_confidence = []
    present = {}

    for field_name in required_fields:
        entry = fields.get(field_name)
        if not isinstance(entry, dict):
            missing.append(field_name)
            continue
        value = entry.get("value")
        confidence = _to_float(entry.get("confidence"))
        if value in (None, ""):
            missing.append(field_name)
            continue
        if confidence is None or confidence < min_confidence:
            low_confidence.append({"field": field_name, "confidence": confidence})
        present[field_name] = {"value": value, "confidence": confidence}

    return {
        "valid": not missing and not low_confidence,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "present_fields": present,
    }


def validate_document_fields_with_openai(document: Dict[str, Any], required_fields: List[str], min_confidence: float = 0.8) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    validation = validate_document_fields(document, required_fields, min_confidence=min_confidence)
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Validate structured document fields and confidence scores.",
            },
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "document": document,
                        "required_fields": required_fields,
                        "min_confidence": min_confidence,
                        "local_validation": validation,
                    }
                ),
            },
        ],
    )
    return {
        "validation": validation,
        "provider": "openai",
        "model": OPENAI_MODEL,
        "response_id": response.id,
    }


def main() -> None:
    import sys

    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_document_fields.py <document_json>")
    document = json.loads(sys.argv[1])
    required_fields = document.get("required_fields", [])
    if not isinstance(required_fields, list):
        raise SystemExit("required_fields must be a list")
    print(json.dumps(validate_document_fields(document, required_fields), indent=2))


if __name__ == "__main__":
    main()
