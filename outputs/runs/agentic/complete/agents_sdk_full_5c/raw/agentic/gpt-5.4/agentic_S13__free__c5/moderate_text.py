from __future__ import annotations

from safety_client import OPENAI_MODERATION_MODEL, get_openai_client
from safety_models import ModerationDecision, decision_from_openai_result


def moderate_text(text: str) -> ModerationDecision:
    client = get_openai_client()
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )
    result = response.results[0].model_dump()
    return decision_from_openai_result(result, provider="openai")
