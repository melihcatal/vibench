from __future__ import annotations

from vision_client import get_openai_client


def visual_safety_text(labels_text: str) -> dict:
    client = get_openai_client()
    response = client.moderations.create(
        model="omni-moderation-latest", input=labels_text
    )
    result = response.results[0]
    return {
        "provider": "openai",
        "flagged": result.flagged,
        "categories": result.categories.model_dump()
        if hasattr(result.categories, "model_dump")
        else dict(result.categories),
    }
