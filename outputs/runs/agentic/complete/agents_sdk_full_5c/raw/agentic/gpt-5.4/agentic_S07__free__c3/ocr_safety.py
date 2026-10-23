from __future__ import annotations

import os

from openai import OpenAI

from document_models import SafetyResult


def check_ocr_text_safety(text: str) -> SafetyResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    return SafetyResult(
        provider="openai",
        flagged=result.flagged,
        categories=result.categories.model_dump(),
        raw=response.model_dump(),
    )
