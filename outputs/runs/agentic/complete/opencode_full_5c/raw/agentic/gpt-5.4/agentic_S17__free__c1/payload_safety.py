from __future__ import annotations

from typing import Any, Dict

from security_client import get_openai_client
from security_models import SafetyCheckResult


def payload_safety(text: str) -> Dict[str, Any]:
    client = get_openai_client()
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    categories = [
        name for name, flagged in result.categories.model_dump().items() if flagged
    ]
    normalized = SafetyCheckResult(
        provider="openai",
        model="omni-moderation-latest",
        is_safe=not result.flagged,
        categories=categories,
        details={
            "flagged": result.flagged,
            "categories": result.categories.model_dump(),
            "category_scores": result.category_scores.model_dump(),
        },
    )
    return normalized.to_dict()
