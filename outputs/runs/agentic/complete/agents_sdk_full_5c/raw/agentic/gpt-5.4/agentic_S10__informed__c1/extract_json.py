from __future__ import annotations

import json
from typing import Any, Dict

from model_client import HostedModelClient
from model_models import GenerationOptions, build_messages


EXTRACTION_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "document_extraction",
        "schema": {
            "type": "object",
            "properties": {
                "people": {"type": "array", "items": {"type": "string"}},
                "organizations": {"type": "array", "items": {"type": "string"}},
                "dates": {"type": "array", "items": {"type": "string"}},
                "summary": {"type": "string"}
            },
            "required": ["people", "organizations", "dates", "summary"],
            "additionalProperties": False,
        },
    },
}


def extract_json(text: str) -> Dict[str, Any]:
    client = HostedModelClient()
    model = client.select_model_family("json")
    messages = build_messages(
        system_prompt="Extract structured information from input text and return valid JSON matching the provided schema.",
        user_prompt=text,
    )
    result = client.chat(
        messages,
        GenerationOptions(
            model=model,
            temperature=0,
            max_tokens=300,
            response_format=EXTRACTION_SCHEMA,
        ),
    )
    return json.loads(result.text)
