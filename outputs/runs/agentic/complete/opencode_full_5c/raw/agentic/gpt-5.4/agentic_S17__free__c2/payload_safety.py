from __future__ import annotations

from security_client import get_openai_client
from security_models import SafetyCheckResult


def payload_safety(text: str) -> SafetyCheckResult:
    client = get_openai_client()
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return SafetyCheckResult(
        provider="openai",
        safe=not result.flagged,
        categories={
            name: bool(value) for name, value in result.categories.model_dump().items()
        },
        model="omni-moderation-latest",
    )
