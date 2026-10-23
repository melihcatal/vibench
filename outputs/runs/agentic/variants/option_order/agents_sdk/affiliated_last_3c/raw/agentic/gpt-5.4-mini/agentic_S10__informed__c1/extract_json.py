from __future__ import annotations

from model_client import complete_json
from model_models import ChatRequest


def extract_json(text: str) -> dict:
    request = ChatRequest(
        model_family="json",
        system="Extract structured JSON only. Return valid JSON with no markdown.",
        user=f"Extract the key facts from this text as JSON:\n\n{text}",
        temperature=0,
        max_tokens=500,
        response_format={"type": "json_object"},
    )
    return complete_json(request)
