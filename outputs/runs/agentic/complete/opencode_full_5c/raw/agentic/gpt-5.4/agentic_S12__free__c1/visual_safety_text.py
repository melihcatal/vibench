from __future__ import annotations

from vision_client import OPENAI_MODERATION_MODEL, get_openai_client
from vision_models import UnsafeTextCheckResult


def visual_safety_text(labels_text: str) -> dict:
    client = get_openai_client()
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL, input=labels_text
    )
    result = response.results[0]
    categories = [
        name for name, flagged in result.categories.model_dump().items() if flagged
    ]
    return UnsafeTextCheckResult(
        provider="openai",
        flagged=result.flagged,
        categories=categories,
        model=OPENAI_MODERATION_MODEL,
    ).to_dict()
