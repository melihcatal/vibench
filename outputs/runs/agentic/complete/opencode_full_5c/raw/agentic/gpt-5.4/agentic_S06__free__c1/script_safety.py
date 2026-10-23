from __future__ import annotations

from typing import Optional

from speech_client import get_openai_client, resolve_moderation_model
from speech_models import SafetyResult


def check_script_safety(
    script_text: str, model: Optional[str] = None, api_key: Optional[str] = None
) -> SafetyResult:
    resolved_model = resolve_moderation_model(model)
    client = get_openai_client(api_key)
    response = client.moderations.create(model=resolved_model, input=script_text)
    result = response.results[0]
    categories = (
        result.categories.model_dump()
        if hasattr(result.categories, "model_dump")
        else dict(result.categories)
    )
    return SafetyResult(
        flagged=result.flagged, categories=categories, model=resolved_model
    )
