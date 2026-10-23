from __future__ import annotations

from typing import Any, Dict

from openai import OpenAI

from speech_client import require_openai_api_key
from speech_models import ModerationResult


def moderate_transcript(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=require_openai_api_key())
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    normalized = ModerationResult(
        flagged=result.flagged,
        categories=result.categories.model_dump(),
        provider="openai",
    )
    return {
        "provider": normalized.provider,
        "flagged": normalized.flagged,
        "categories": normalized.categories,
    }
