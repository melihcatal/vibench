from __future__ import annotations

from safety_client import DEFAULT_MODERATION_MODEL, get_openai_client
from safety_models import normalize_openai_result


def moderate_text(text: str) -> dict:
    client = get_openai_client()
    response = client.moderations.create(
        model=DEFAULT_MODERATION_MODEL,
        input=text,
    )
    decision = normalize_openai_result(response.results[0], model=DEFAULT_MODERATION_MODEL)
    return decision.to_dict()
