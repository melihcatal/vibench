from __future__ import annotations

from typing import Dict

from identity_client import get_openai_client
from identity_models import ModerationResult


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def profile_moderation(profile_text: str) -> Dict[str, object]:
    client = get_openai_client()
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL, input=profile_text
    )
    result = response.results[0]
    flagged = bool(result.flagged)
    approved = not flagged
    return ModerationResult(
        approved=approved,
        flagged=flagged,
        categories=result.categories.model_dump(),
        category_scores=result.category_scores.model_dump(),
        model=OPENAI_MODERATION_MODEL,
    ).to_dict()
