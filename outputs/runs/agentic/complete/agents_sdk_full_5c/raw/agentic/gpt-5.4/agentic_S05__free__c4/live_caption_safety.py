from __future__ import annotations

import os

from openai import OpenAI

from speech_models import SafetyResult, normalize_whitespace


def check_live_caption_safety(text: str, api_key: str | None = None) -> SafetyResult:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=normalize_whitespace(text),
    )
    result = response.results[0]
    categories = [name for name, flagged in result.categories.model_dump().items() if flagged]
    return SafetyResult(flagged=result.flagged, categories=categories, raw=response.model_dump())
