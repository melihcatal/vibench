from __future__ import annotations

import os
from typing import Dict, Optional

from openai import OpenAI

from speech_models import NormalizedModerationResult


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_transcript(text: str, *, api_key: Optional[str] = None) -> Dict[str, object]:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    normalized = NormalizedModerationResult(
        flagged=result.flagged,
        categories=result.categories.model_dump(),
        scores=result.category_scores.model_dump(),
    )
    return {
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
        "flagged": normalized.flagged,
        "categories": normalized.categories,
        "scores": normalized.scores,
    }
