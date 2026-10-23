from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List

from openai import OpenAI


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_transcript(segments: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    normalized_segments: List[Dict[str, Any]] = list(segments)
    joined_text = "\n".join(segment.get("text", "") for segment in normalized_segments)
    result = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=joined_text,
    )
    moderation = result.results[0]
    return {
        "provider": "OpenAI",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": moderation.flagged,
        "categories": moderation.categories.model_dump(),
        "category_scores": moderation.category_scores.model_dump(),
    }
