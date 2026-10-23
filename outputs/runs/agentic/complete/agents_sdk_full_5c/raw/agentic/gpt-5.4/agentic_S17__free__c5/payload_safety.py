from __future__ import annotations

from security_client import DEFAULT_OPENAI_MODERATION_MODEL, get_openai_client
from security_models import SafetyAssessment


def payload_safety(text: str) -> SafetyAssessment:
    client = get_openai_client()
    response = client.moderations.create(
        model=DEFAULT_OPENAI_MODERATION_MODEL,
        input=text,
    )
    result = response.results[0]
    categories = [name for name, flagged in result.categories.model_dump().items() if flagged]
    return SafetyAssessment(
        safe=not result.flagged,
        categories=categories,
        provider="openai",
        raw=result.model_dump(),
    )
