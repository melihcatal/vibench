from __future__ import annotations

from security_client import OPENAI_MODERATION_MODEL, OPENAI_PROVIDER, get_openai_client
from security_models import SafetyCheckResponse


def payload_safety(text: str) -> SafetyCheckResponse:
    client = get_openai_client()
    result = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    moderation = result.results[0]
    categories = []
    for name, flagged in moderation.categories.model_dump().items():
        if flagged:
            categories.append(name)
    return SafetyCheckResponse(
        provider=OPENAI_PROVIDER,
        safe=not moderation.flagged,
        flagged_categories=categories,
        raw_result=moderation.model_dump(),
    )
