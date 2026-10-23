from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI



def moderate_vendor_text(text: str) -> Dict[str, Any]:
    client = OpenAI()
    moderation = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = moderation.results[0]
    return {
        "provider": "openai",
        "model": "omni-moderation-latest",
        "flagged": result.flagged,
        "categories": result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories),
        "category_scores": result.category_scores.model_dump() if hasattr(result.category_scores, "model_dump") else dict(result.category_scores),
    }
