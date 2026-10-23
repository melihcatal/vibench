from __future__ import annotations

import os

from openai import OpenAI

from speech_models import SafetyResult, ensure_text


def check_script_safety(text: str) -> SafetyResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    client = OpenAI(api_key=api_key)
    result = client.moderations.create(
        model="omni-moderation-latest", input=ensure_text(text)
    )
    output = result.results[0]
    categories = {
        key: bool(value) for key, value in output.categories.model_dump().items()
    }
    scores = {
        key: float(value) for key, value in output.category_scores.model_dump().items()
    }
    return SafetyResult(
        flagged=bool(output.flagged), categories=categories, category_scores=scores
    )
