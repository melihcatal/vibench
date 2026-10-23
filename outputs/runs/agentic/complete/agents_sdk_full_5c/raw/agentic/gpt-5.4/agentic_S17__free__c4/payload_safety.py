from __future__ import annotations

from security_client import openai_client
from security_models import SafetyResult


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def payload_safety(text: str) -> SafetyResult:
    client = openai_client()
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    return SafetyResult(
        model=OPENAI_MODERATION_MODEL,
        safe=not result.flagged,
        categories=result.categories.model_dump(),
        provider="openai",
    )
