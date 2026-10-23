from __future__ import annotations

import json

from model_client import chat_completion
from model_models import ChatMessage, LLMRequest


def extract_json(text: str) -> dict:
    request = LLMRequest(
        model_family="gpt-4o-mini",
        messages=[
            ChatMessage(role="system", content="Extract structured JSON from the user text. Return only valid JSON."),
            ChatMessage(role="user", content=text),
        ],
        temperature=0.0,
        max_tokens=500,
    )
    raw = chat_completion(request).text
    return json.loads(raw)
