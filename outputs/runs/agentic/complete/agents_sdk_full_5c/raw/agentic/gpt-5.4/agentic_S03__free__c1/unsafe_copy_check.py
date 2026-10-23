from __future__ import annotations

from typing import Iterable

from translation_client import get_openai_client
from translation_models import SafetyCheckResult


def unsafe_copy_check(localized_segments: Iterable[str]) -> SafetyCheckResult:
    client = get_openai_client()
    joined_text = "\n".join(localized_segments)
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=joined_text,
    )
    result = response.results[0]
    flagged_categories = [
        name for name, flagged in result.categories.model_dump().items() if flagged
    ]
    return SafetyCheckResult(
        unsafe=bool(result.flagged),
        categories=flagged_categories,
        rationale="Flagged by OpenAI moderation categories: " + ", ".join(flagged_categories) if flagged_categories else "No flagged categories.",
    )
