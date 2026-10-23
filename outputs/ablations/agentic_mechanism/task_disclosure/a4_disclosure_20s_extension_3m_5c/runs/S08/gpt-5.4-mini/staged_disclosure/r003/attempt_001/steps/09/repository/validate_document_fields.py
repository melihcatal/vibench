import json
import os
from typing import Any, Dict, List, Tuple

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _load_json(source: str) -> Dict[str, Any]:
    if os.path.exists(source):
        with open(source, "r", encoding="utf-8") as f:
            return json.load(f)
    return json.loads(source)


def _validate_field(name: str, payload: Dict[str, Any], errors: List[str]) -> None:
    value = payload.get(name)
    if value is None or value == "":
        errors.append(f"missing required field: {name}")


def _validate_confidence(name: str, payload: Dict[str, Any], errors: List[str]) -> None:
    confidence_key = f"{name}_confidence"
    value = payload.get(confidence_key)
    if value is None:
        errors.append(f"missing confidence score: {confidence_key}")
        return
    try:
        score = float(value)
    except (TypeError, ValueError):
        errors.append(f"invalid confidence score: {confidence_key}")
        return
    if not 0.0 <= score <= 1.0:
        errors.append(f"confidence score out of range: {confidence_key}")


def validate_document_fields(document_source: str) -> Dict[str, Any]:
    document = _load_json(document_source)
    required_fields = ["document_type", "document_id", "date", "total"]
    errors: List[str] = []

    for field in required_fields:
        _validate_field(field, document, errors)
        _validate_confidence(field, document, errors)

    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        response = requests.post(
            OPENAI_RESPONSES_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": OPENAI_MODEL,
                "input": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": (
                                    "Validate this document JSON for required structured fields and confidence scores. "
                                    "Return strict JSON with keys valid, errors, and missing_fields.\n\n"
                                    f"Document:\n{json.dumps(document, ensure_ascii=False)}"
                                ),
                            }
                        ],
                    }
                ],
                "text": {"format": {"type": "json_object"}},
            },
            timeout=120,
        )
        response.raise_for_status()
        content = ""
        for item in response.json().get("output", []):
            for block in item.get("content", []):
                if block.get("type") in {"output_text", "text"}:
                    content += block.get("text", "")
        if content:
            remote_result = json.loads(content)
            if isinstance(remote_result, dict) and remote_result.get("errors"):
                errors.extend(str(err) for err in remote_result.get("errors", []))

    return {"valid": not errors, "errors": errors, "document": document}


if __name__ == "__main__":
    import sys

    source = sys.argv[1] if len(sys.argv) > 1 else "{}"
    print(json.dumps(validate_document_fields(source), ensure_ascii=False))
