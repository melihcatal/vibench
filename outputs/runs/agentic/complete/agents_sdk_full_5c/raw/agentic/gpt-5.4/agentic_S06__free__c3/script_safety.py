from __future__ import annotations

import os
from typing import List

from openai import OpenAI

from speech_models import SafetyResult

OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_script_safety(text: str) -> SafetyResult:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    categories: List[str] = [name for name, flagged in result.categories.model_dump().items() if flagged]
    return SafetyResult(
        provider="openai",
        flagged=result.flagged,
        categories=categories,
        raw=result.model_dump(),
    )
