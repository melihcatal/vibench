from __future__ import annotations

import os

from openai import OpenAI

from identity_models import ModerationResult


OPENAI_MODERATION_MODEL_ENV = "OPENAI_MODERATION_MODEL"
DEFAULT_MODERATION_MODEL = "omni-moderation-latest"


def moderate_claim_text(text: str) -> ModerationResult:
    model = os.getenv(OPENAI_MODERATION_MODEL_ENV, DEFAULT_MODERATION_MODEL)
    client = OpenAI()
    response = client.moderations.create(model=model, input=text)
    result = response.results[0]
    categories = result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories)
    return ModerationResult(
        provider="OpenAI",
        model=model,
        flagged=result.flagged,
        categories=categories,
        raw=response.model_dump() if hasattr(response, "model_dump") else {},
    )
