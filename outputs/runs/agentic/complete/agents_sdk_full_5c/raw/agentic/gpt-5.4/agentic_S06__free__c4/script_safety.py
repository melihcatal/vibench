from __future__ import annotations

from openai import OpenAI

from speech_models import SafetyCheckResult


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_script_safety(text: str) -> SafetyCheckResult:
    client = OpenAI()
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )
    result = response.results[0]
    categories = {
        key: float(value)
        for key, value in result.category_scores.model_dump().items()
    }
    return SafetyCheckResult(
        blocked=bool(result.flagged),
        categories=categories,
    )
