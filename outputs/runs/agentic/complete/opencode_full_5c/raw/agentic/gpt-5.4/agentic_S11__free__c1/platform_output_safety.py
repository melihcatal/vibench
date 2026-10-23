from __future__ import annotations

from model_client import get_openai_client
from model_models import SafetyResult


def platform_output_safety(text: str) -> SafetyResult:
    client = get_openai_client()
    result = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    moderation = result.results[0]
    return SafetyResult(
        flagged=moderation.flagged,
        categories=dict(moderation.categories),
        provider_result=result,
    )
