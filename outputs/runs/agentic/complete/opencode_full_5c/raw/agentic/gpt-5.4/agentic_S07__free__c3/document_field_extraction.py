from __future__ import annotations

import json
from typing import Iterable

from document_client import OPENAI_RESPONSES_URL, build_openai_headers, post_json
from document_models import FieldExtractionResult


def extract_document_fields(
    text: str, field_names: Iterable[str]
) -> FieldExtractionResult:
    fields = list(field_names)
    schema_hint = {name: "" for name in fields}
    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Extract the requested document fields from OCR text and return strict JSON only.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Fields: {fields}\nExpected JSON template: {json.dumps(schema_hint)}\nOCR text:\n{text}",
                    }
                ],
            },
        ],
    }
    response_json = post_json(
        OPENAI_RESPONSES_URL, payload, headers=build_openai_headers()
    )
    output_text = (
        response_json.get("output", [{}])[0].get("content", [{}])[0].get("text", "{}")
    )
    parsed = json.loads(output_text)
    return FieldExtractionResult(
        provider="openai", fields=parsed, raw_response=response_json
    )
