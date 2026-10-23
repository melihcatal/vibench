from __future__ import annotations

import os

from openai import OpenAI

from document_models import SafetyCheckResult


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_ocr_text_safety(text: str) -> SafetyCheckResult:
    client = OpenAI(api_key=os.environ[OPENAI_API_KEY_ENV])
    response = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = response.results[0]
    categories = (
        result.categories.model_dump()
        if hasattr(result.categories, "model_dump")
        else dict(result.categories)
    )
    scores = (
        result.category_scores.model_dump()
        if hasattr(result.category_scores, "model_dump")
        else dict(result.category_scores)
    )
    return SafetyCheckResult(
        provider="openai",
        flagged=result.flagged,
        categories=categories,
        category_scores=scores,
        raw_response=response.model_dump() if hasattr(response, "model_dump") else {},
    )
