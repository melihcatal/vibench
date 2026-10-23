from __future__ import annotations

import json
from typing import Any, Dict

from model_client import create_chat_completion
from model_models import ChatMessage, GenerationRequest, coerce_text


def extract_json(text: str, schema_hint: str, model: str = "gpt-4o-mini") -> Dict[str, Any]:
    payload_text = coerce_text(text)
    request = GenerationRequest(
        model=model,
        temperature=0.0,
        max_tokens=400,
        messages=[
            ChatMessage(
                role="system",
                content="Extract structured data and return only valid JSON with no markdown fences or commentary.",
            ),
            ChatMessage(
                role="user",
                content=(
                    "Extract JSON from the text below. "
                    f"Follow this schema guidance: {schema_hint}\n\n"
                    f"Text:\n{payload_text}"
                ),
            ),
        ],
    )
    content = create_chat_completion(request).text
    return json.loads(content)
