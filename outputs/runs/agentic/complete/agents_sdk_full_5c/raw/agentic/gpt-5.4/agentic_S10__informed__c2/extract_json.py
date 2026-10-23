from __future__ import annotations

import json
from typing import Any, Dict

from model_client import OpenAIModelClient, build_text_request
from model_models import strip_code_fences


_JSON_SCHEMA_PROMPT = (
    "Extract structured information from the user text and return only valid JSON. "
    "Do not include markdown fences or extra commentary."
)


def extract_json(text: str, *, instructions: str = "Return an object with the key facts.", model: str = "gpt-4o-mini") -> Dict[str, Any]:
    client = OpenAIModelClient(model=model)
    request = build_text_request(
        system_prompt=_JSON_SCHEMA_PROMPT,
        user_prompt=f"Instructions: {instructions}\n\nText:\n{text}",
        model=model,
        temperature=0,
        max_tokens=500,
    )
    raw_text = client.complete(request).content
    return json.loads(strip_code_fences(raw_text))
