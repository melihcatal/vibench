from __future__ import annotations

from openai import OpenAI

from identity_models import ModerationResult


OPENAI_MODERATION_MODEL = "omni-moderation-latest"



def profile_moderation(profile_text: str) -> ModerationResult:
    client = OpenAI()
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=profile_text)
    result = response.results[0]
    flagged_categories = [name for name, enabled in result.categories.model_dump().items() if enabled]
    score_map = {name: float(score) for name, score in result.category_scores.model_dump().items()}
    return ModerationResult(
        allowed=not result.flagged,
        flagged_categories=flagged_categories,
        score_map=score_map,
    )
