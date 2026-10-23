from __future__ import annotations

import json
from typing import Any, Dict

from model_client import get_openai_client, messages_to_dicts, resolve_chat_config
from model_models import normalize_messages


def extract_json(source_text: str, schema_description: str) -> Dict[str, Any]:
    client = get_openai_client()
    config = resolve_chat_config(
        model="gpt-4.1-mini", temperature=0.0, max_output_tokens=700
    )
    messages = normalize_messages(
        system_prompt="Extract structured data and return valid JSON only.",
        user_prompt=(
            f"Schema requirements:\n{schema_description}\n\n"
            f"Source text:\n{source_text}\n\n"
            "Return a single JSON object with no markdown."
        ),
    )
    response = client.responses.create(
        model=config.model,
        input=messages_to_dicts(messages),
        temperature=config.temperature,
        max_output_tokens=config.max_output_tokens,
        text={"format": {"type": "json_object"}},
    )
    return json.loads(response.output_text)
