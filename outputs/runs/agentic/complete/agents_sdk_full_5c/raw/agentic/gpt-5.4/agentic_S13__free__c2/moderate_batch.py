from __future__ import annotations

from typing import Iterable, List

from safety_client import get_openai_client, moderation_model
from safety_models import BatchModerationResult, normalize_openai_moderation_response


def moderate_batch(messages: Iterable[str], api_key: str | None = None, model: str | None = None) -> BatchModerationResult:
    client = get_openai_client(api_key)
    resolved_model = moderation_model(model)
    payload: List[str] = list(messages)
    response = client.moderations.create(
        model=resolved_model,
        input=payload,
    )
    return normalize_openai_moderation_response(response, model=resolved_model)
