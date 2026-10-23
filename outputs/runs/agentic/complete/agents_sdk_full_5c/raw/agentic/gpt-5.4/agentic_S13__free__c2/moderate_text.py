from __future__ import annotations

from safety_client import get_openai_client, moderation_model
from safety_models import ModerationResult, normalize_openai_moderation_result


def moderate_text(text: str, api_key: str | None = None, model: str | None = None) -> ModerationResult:
    client = get_openai_client(api_key)
    resolved_model = moderation_model(model)
    response = client.moderations.create(
        model=resolved_model,
        input=text,
    )
    return normalize_openai_moderation_result(response.results[0], model=resolved_model)
