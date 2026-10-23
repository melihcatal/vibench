from __future__ import annotations

import json
from typing import Any, Dict

from model_client import choose_model, get_openai_client
from model_models import ChatMessage, messages_to_dicts, normalize_text


EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "people": {"type": "array", "items": {"type": "string"}},
        "organizations": {"type": "array", "items": {"type": "string"}},
        "dates": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
    },
    "required": ["people", "organizations", "dates", "summary"],
    "additionalProperties": False,
}


def extract_json(text: str) -> Dict[str, Any]:
    client = get_openai_client()
    response = client.chat.completions.create(
        model=choose_model("extract"),
        messages=messages_to_dicts(
            [
                ChatMessage(role="system", content="Extract structured entities and return only valid JSON."),
                ChatMessage(role="user", content=normalize_text(text)),
            ]
        ),
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "entity_extraction",
                "schema": EXTRACTION_SCHEMA,
                "strict": True,
            },
        },
    )
    content = response.choices[0].message.content or "{}"
    return json.loads(content)
