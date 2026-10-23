from __future__ import annotations

import json

from openai import OpenAI

from model_client import DEFAULT_CHAT_MODEL, get_openai_client
from model_models import compact_json_schema


def extract_json(text: str) -> dict:
    client: OpenAI = get_openai_client()
    response = client.responses.create(
        model=DEFAULT_CHAT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Extract structured entities and return valid JSON matching the schema.",
            },
            {
                "role": "user",
                "content": f"Text to analyze:\n{text}",
            },
        ],
        text={"format": {"type": "json_schema", "name": compact_json_schema()["name"], "schema": compact_json_schema()["schema"], "strict": True}},
    )
    return json.loads(response.output_text)
