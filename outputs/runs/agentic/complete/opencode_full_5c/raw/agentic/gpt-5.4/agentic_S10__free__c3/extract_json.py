from __future__ import annotations

import json

from model_client import DEFAULT_REASONING_MODEL, build_chat_request, get_openai_client
from model_models import normalize_generation_response


def extract_json(text: str, schema_hint: str) -> dict:
    client = get_openai_client()
    prompt = f"Schema hint:\n{schema_hint}\n\nSource text:\n{text}"
    request = build_chat_request(
        "Extract the requested fields from the source text and return only valid JSON.",
        prompt,
        model=DEFAULT_REASONING_MODEL,
        temperature=0,
        max_output_tokens=500,
    )
    response = client.chat.completions.create(
        **request.to_openai(),
        response_format={"type": "json_object"},
    )
    result = normalize_generation_response(response)
    return {
        "data": json.loads(result.text),
        "model": result.model,
        "usage": result.usage,
    }
