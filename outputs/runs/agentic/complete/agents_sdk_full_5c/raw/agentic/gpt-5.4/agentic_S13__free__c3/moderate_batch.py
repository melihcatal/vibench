from __future__ import annotations

from safety_client import DEFAULT_MODERATION_MODEL, ensure_messages, get_openai_client
from safety_models import normalize_openai_result


def moderate_batch(messages: list[str]) -> list[dict]:
    client = get_openai_client()
    payload = ensure_messages(messages)
    response = client.moderations.create(
        model=DEFAULT_MODERATION_MODEL,
        input=payload,
    )
    return [
        normalize_openai_result(item, model=DEFAULT_MODERATION_MODEL).to_dict()
        for item in response.results
    ]
