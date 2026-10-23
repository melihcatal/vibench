from __future__ import annotations

from typing import List, Optional

from openai import OpenAI

from translation_client import OPENAI_API_KEY
from translation_models import SafetyCheckResult


def unsafe_copy_check(text: str) -> SafetyCheckResult:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    flagged = bool(result.flagged)
    categories: List[str] = [name for name, active in result.categories.model_dump().items() if active]
    return SafetyCheckResult(safe=not flagged, categories=categories, redacted_text=None, raw=response.model_dump())
