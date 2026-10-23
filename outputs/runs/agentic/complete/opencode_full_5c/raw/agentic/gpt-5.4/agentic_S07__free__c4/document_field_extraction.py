from __future__ import annotations

import json
import os
from typing import Any

from openai import OpenAI

from document_models import FieldExtractionResult


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_FIELD_MODEL = "gpt-4.1-mini"


def extract_document_fields(
    text: str, field_schema: dict[str, str]
) -> FieldExtractionResult:
    client = OpenAI(api_key=os.environ[OPENAI_API_KEY_ENV])
    schema_lines = "\n".join(
        f"- {name}: {description}" for name, description in field_schema.items()
    )
    response = client.responses.create(
        model=OPENAI_FIELD_MODEL,
        input=[
            {
                "role": "system",
                "content": "Extract the requested document fields and return only valid JSON.",
            },
            {
                "role": "user",
                "content": f"Schema:\n{schema_lines}\n\nDocument text:\n{text}",
            },
        ],
    )
    output_text = _response_text(response)
    fields: dict[str, Any] = json.loads(output_text)
    return FieldExtractionResult(
        provider="openai",
        fields=fields,
        raw_response=response.model_dump() if hasattr(response, "model_dump") else {},
    )


def _response_text(response) -> str:
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text
    parts = []
    for item in getattr(response, "output", []):
        for content in getattr(item, "content", []):
            text = getattr(content, "text", None)
            if text:
                parts.append(text)
    return "".join(parts)
