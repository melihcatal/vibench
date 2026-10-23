from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Union

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
DEFAULT_MODEL = "gpt-5.4-mini"


@dataclass
class FieldExtractionRequest:
    text: str
    fields: Sequence[str]
    instructions: str = "Extract the requested structured fields from the provided OCR-normalized document text."
    model: str = DEFAULT_MODEL
    temperature: float = 0.0
    max_output_tokens: int = 1024


@dataclass
class FieldExtractionResponse:
    fields: Dict[str, Any]
    raw_output: str
    model: str


def _auth_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }


def _build_prompt(request: FieldExtractionRequest) -> str:
    fields = "\n".join(f"- {field}" for field in request.fields)
    schema = {
        field: "string | number | boolean | null | object | array"
        for field in request.fields
    }
    return (
        f"{request.instructions}\n\n"
        f"Requested fields:\n{fields}\n\n"
        f"Return JSON with exactly these top-level keys:\n{json.dumps(schema, ensure_ascii=False)}\n\n"
        f"Document text:\n{request.text}"
    )


def _extract_text_from_response(payload: Mapping[str, Any]) -> str:
    if "output_text" in payload and isinstance(payload["output_text"], str):
        return payload["output_text"]
    output = payload.get("output", [])
    chunks: List[str] = []
    for item in output:
        if not isinstance(item, Mapping):
            continue
        for content in item.get("content", []):
            if isinstance(content, Mapping):
                text = content.get("text")
                if isinstance(text, str):
                    chunks.append(text)
    return "\n".join(chunks).strip()


def _coerce_field_payload(text: str, fields: Sequence[str]) -> Dict[str, Any]:
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("Model response was not a JSON object")
    return {field: parsed.get(field) for field in fields}


def extract_fields(
    text: str,
    fields: Sequence[str],
    *,
    api_key: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.0,
    max_output_tokens: int = 1024,
    instructions: str = "Extract the requested structured fields from the provided OCR-normalized document text.",
) -> FieldExtractionResponse:
    request = FieldExtractionRequest(
        text=text,
        fields=list(fields),
        instructions=instructions,
        model=model,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
    )
    payload: Dict[str, Any] = {
        "model": request.model,
        "input": _build_prompt(request),
        "temperature": request.temperature,
        "max_output_tokens": request.max_output_tokens,
    }
    response = requests.post(
        OPENAI_RESPONSES_URL,
        headers=_auth_headers(api_key),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    raw_text = _extract_text_from_response(data)
    if not raw_text:
        raise ValueError("Empty response from OpenAI Responses API")
    return FieldExtractionResponse(
        fields=_coerce_field_payload(raw_text, request.fields),
        raw_output=raw_text,
        model=request.model,
    )


def extract_fields_from_document(
    document_text: str,
    field_names: Iterable[str],
    **kwargs: Any,
) -> Dict[str, Any]:
    return extract_fields(document_text, list(field_names), **kwargs).fields
