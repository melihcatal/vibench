from __future__ import annotations

import os

from openai import OpenAI

from speech_models import SafetyResult


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_script_safety(text: str) -> SafetyResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    categories = [name for name, flagged in result.categories.model_dump().items() if flagged]
    return SafetyResult(
        blocked=result.flagged,
        categories=categories,
        raw_response=response.model_dump(),
    )
