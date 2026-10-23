from __future__ import annotations

from typing import Iterable, List

from safety_client import OPENAI_MODERATION_MODEL, get_openai_client
from safety_models import BatchModerationResult, decision_from_openai_result


def moderate_batch(messages: Iterable[str]) -> BatchModerationResult:
    items: List[str] = list(messages)
    client = get_openai_client()
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=items,
    )
    results = [decision_from_openai_result(item.model_dump(), provider="openai") for item in response.results]
    return BatchModerationResult(results=results)
