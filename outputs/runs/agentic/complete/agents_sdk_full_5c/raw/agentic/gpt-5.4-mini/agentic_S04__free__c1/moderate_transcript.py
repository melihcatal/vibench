from __future__ import annotations

from openai import OpenAI

from speech_client import OPENAI_MODERATION_MODEL, get_client, normalize_text
from speech_models import ModerationRequest


def moderate_transcript(transcript: str, categories: list[str] | None = None) -> dict:
    client: OpenAI = get_client()
    request = ModerationRequest(transcript=normalize_text(transcript), categories=categories)
    moderation = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=request.transcript,
    )
    result = moderation.results[0]
    flagged_categories = []
    if hasattr(result, "categories"):
        flagged_categories = [name for name, flagged in result.categories.model_dump().items() if flagged]
    if request.categories:
        flagged_categories = [category for category in flagged_categories if category in request.categories]
    return {"flagged": result.flagged, "categories": flagged_categories, "raw": moderation.model_dump()}
