import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class FieldExtractionResult:
    fields: Dict[str, Any]
    raw_response: Dict[str, Any]


def _build_prompt(document_text: str, field_spec: Optional[List[str]], schema_hint: Optional[Dict[str, Any]]) -> str:
    parts = [
        "Extract structured fields from the following OCR-normalized document text.",
        "Return only valid JSON with a top-level object named fields.",
    ]
    if field_spec:
        parts.append(f"Target fields: {', '.join(field_spec)}")
    if schema_hint:
        parts.append(f"Schema hint: {schema_hint}")
    parts.append("Document text:")
    parts.append(document_text)
    return "\n".join(parts)


def extract_structured_fields(
    document_text: str,
    field_spec: Optional[List[str]] = None,
    schema_hint: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    timeout: int = 60,
) -> FieldExtractionResult:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "input": _build_prompt(document_text, field_spec, schema_hint),
    }
    if schema_hint:
        payload["text"] = {"format": {"type": "json_schema", "name": "field_extraction", "schema": {"type": "object", "properties": {"fields": schema_hint}, "required": ["fields"], "additionalProperties": False}}}

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()

    extracted: Dict[str, Any] = {}
    output = data.get("output", [])
    for item in output:
        content = item.get("content", [])
        for block in content:
            if isinstance(block, dict) and block.get("type") in {"output_text", "text"}:
                text = block.get("text", "")
                if text:
                    import json

                    parsed = json.loads(text)
                    if isinstance(parsed, dict) and "fields" in parsed:
                        extracted = parsed["fields"]
                        break
        if extracted:
            break

    if not extracted and isinstance(data.get("output_text"), str):
        import json

        parsed = json.loads(data["output_text"])
        if isinstance(parsed, dict) and "fields" in parsed:
            extracted = parsed["fields"]

    return FieldExtractionResult(fields=extracted, raw_response=data)
