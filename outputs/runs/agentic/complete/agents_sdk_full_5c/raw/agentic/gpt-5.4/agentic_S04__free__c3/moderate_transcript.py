from __future__ import annotations

from typing import Dict, List

from openai import OpenAI


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_transcript(segments: List[Dict[str, str]]) -> Dict[str, object]:
    client = OpenAI()
    text = "\n".join(segment.get("text", "") for segment in segments)
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    moderation = result.results[0]
    return {
        "provider": "OpenAI",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": moderation.flagged,
        "categories": moderation.categories.model_dump(),
        "category_scores": moderation.category_scores.model_dump(),
    }
