from __future__ import annotations

import os

from openai import OpenAI

from identity_models import ModerationResult


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_claim_text(text: str) -> ModerationResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    scores = {name: float(value) for name, value in result.category_scores.model_dump().items()}
    categories = {name: bool(value) for name, value in result.categories.model_dump().items()}
    return ModerationResult(
        provider="openai",
        model=OPENAI_MODERATION_MODEL,
        flagged=bool(result.flagged),
        categories=categories,
        category_scores=scores,
    )
