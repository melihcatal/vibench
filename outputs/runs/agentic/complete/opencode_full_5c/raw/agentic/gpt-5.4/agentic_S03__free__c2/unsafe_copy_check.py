from __future__ import annotations

from openai import OpenAI

from translation_client import openai_api_key
from translation_models import SafetyCheckResult


def unsafe_copy_check(text: str, language: str) -> SafetyCheckResult:
    client = OpenAI(api_key=openai_api_key())
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=f"Language: {language}\nLocalized copy: {text}",
    )
    result = response.results[0]
    flagged_categories = [
        name for name, flagged in result.categories.model_dump().items() if flagged
    ]
    return SafetyCheckResult(
        safe=not result.flagged,
        categories=flagged_categories,
        rationale="Flagged by OpenAI moderation categories"
        if result.flagged
        else "No unsafe categories flagged",
        provider="openai-omni-moderation-latest",
        raw=response.model_dump(),
    )
