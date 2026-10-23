from __future__ import annotations

import os

from openai import OpenAI

from identity_models import ModerationResult


OPENAI_MODERATION_MODEL = os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_claim_text(text: str) -> ModerationResult:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    categories = result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories)
    raw = response.model_dump() if hasattr(response, "model_dump") else {"results": response.results}
    return ModerationResult(
        provider="OpenAI",
        model=OPENAI_MODERATION_MODEL,
        flagged=bool(result.flagged),
        categories=categories,
        raw=raw,
    )
