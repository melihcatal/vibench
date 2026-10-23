from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from speech_models import ModerationResult


def moderate_transcript(text: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    categories = {name: bool(value) for name, value in result.categories.model_dump().items()}
    scores = {name: float(value) for name, value in result.category_scores.model_dump().items()}
    moderation = ModerationResult(
        flagged=bool(result.flagged),
        categories=categories,
        category_scores=scores,
    )
    return moderation.__dict__
