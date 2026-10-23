from __future__ import annotations

from typing import Any, Dict

from model_client import OPENAI_DEFAULT_MODERATION_MODEL, get_openai_client


def platform_output_safety(text: str) -> Dict[str, Any]:
    client = get_openai_client()
    result = client.moderations.create(
        model=OPENAI_DEFAULT_MODERATION_MODEL,
        input=text,
    )
    moderation = result.results[0]
    return {
        "provider": "openai",
        "model": OPENAI_DEFAULT_MODERATION_MODEL,
        "flagged": moderation.flagged,
        "categories": moderation.categories,
        "category_scores": moderation.category_scores,
        "raw_response": result,
    }
