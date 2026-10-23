from __future__ import annotations

import json
from typing import Any, Dict

from model_client import create_chat_completion
from model_models import ChatRequest, normalize_json_text, truncate_text


def extract_json(
    text: str, schema_hint: str, model: str | None = None
) -> Dict[str, Any]:
    request = ChatRequest(
        system_prompt="You are an OpenAI information extraction assistant. Return only valid JSON matching the requested structure.",
        user_prompt=(
            f"Extract structured data from the text below.\n"
            f"Schema hint: {schema_hint}\n"
            f"Return JSON only.\n\n"
            f"Text:\n{truncate_text(text)}"
        ),
        model=model,
        temperature=0.0,
        max_tokens=500,
    )
    raw = create_chat_completion(request).text
    return json.loads(normalize_json_text(raw))
