from __future__ import annotations

from security_client import get_openai_client
from security_models import SafetyCheckResult


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def payload_safety(text: str) -> SafetyCheckResult:
    client = get_openai_client()
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )
    result = response.results[0]
    categories = [name for name, flagged in result.categories.model_dump().items() if flagged]
    return SafetyCheckResult(
        is_safe=not result.flagged,
        categories=categories,
        provider="OpenAI",
    )
