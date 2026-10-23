from __future__ import annotations

from openai import OpenAI

from messaging_models import normalize_text


MODEL = "gpt-4o-mini"


def check_message_safety(text: str) -> dict:
    client = OpenAI()
    normalized = normalize_text(text)
    response = client.moderations.create(model=MODEL, input=normalized)
    result = response.results[0]
    return {
        "provider": "openai",
        "model": MODEL,
        "safe": not result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
        "text": normalized,
    }
