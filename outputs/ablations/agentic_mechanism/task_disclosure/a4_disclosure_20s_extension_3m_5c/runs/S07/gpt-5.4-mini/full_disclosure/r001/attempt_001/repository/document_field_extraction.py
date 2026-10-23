from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_HOST = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class FieldExtractionResult:
    fields: Dict[str, Any]
    raw_response: Dict[str, Any]


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _messages(document_text: str, field_names: Optional[List[str]] = None, schema_hint: Optional[Dict[str, Any]] = None) -> List[Dict[str, str]]:
    instructions = [
        "Extract structured fields from OCR-normalized document text.",
        "Return only valid JSON with a top-level object named fields.",
        "Use null for missing values.",
    ]
    if field_names:
        instructions.append(f"Target fields: {json.dumps(field_names)}")
    if schema_hint:
        instructions.append(f"Schema hint: {json.dumps(schema_hint)}")
    return [
        {"role": "system", "content": "\n".join(instructions)},
        {"role": "user", "content": document_text},
    ]


def extract_fields(document_text: str, field_names: Optional[List[str]] = None, schema_hint: Optional[Dict[str, Any]] = None, model: str = OPENAI_MODEL) -> FieldExtractionResult:
    payload: Dict[str, Any] = {
        "model": model,
        "input": _messages(document_text, field_names, schema_hint),
        "response_format": {"type": "json_object"},
    }
    response = requests.post(
        f"{OPENAI_API_HOST}/responses",
        headers=_headers(),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    text = ""
    if isinstance(data, dict):
        output = data.get("output", [])
        for item in output:
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"}:
                    text += content.get("text", "")
    parsed = json.loads(text) if text else {}
    fields = parsed.get("fields", parsed if isinstance(parsed, dict) else {})
    return FieldExtractionResult(fields=fields, raw_response=data)
