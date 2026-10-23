from __future__ import annotations

from messaging_client import get_openai_client
from messaging_models import extract_text


def check_message_payload_safety(payload: dict, field_name: str = "text") -> dict:
    client = get_openai_client()
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=extract_text(payload, field_name=field_name),
    )
    result = response.results[0]
    return {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "flagged": result.flagged,
        "categories": result.categories.model_dump()
        if hasattr(result.categories, "model_dump")
        else dict(result.categories),
        "category_scores": result.category_scores.model_dump()
        if hasattr(result.category_scores, "model_dump")
        else dict(result.category_scores),
    }
