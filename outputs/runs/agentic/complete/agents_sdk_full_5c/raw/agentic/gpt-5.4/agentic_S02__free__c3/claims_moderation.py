from __future__ import annotations

import os

from openai import OpenAI

from identity_models import ModerationResult


OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_claim_text(text: str) -> ModerationResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    return ModerationResult(
        provider="openai",
        model=OPENAI_MODERATION_MODEL,
        flagged=result.flagged,
        categories={k: bool(v) for k, v in result.categories.model_dump().items()},
        category_scores={k: float(v) for k, v in result.category_scores.model_dump().items()},
        original_text=text,
    )
