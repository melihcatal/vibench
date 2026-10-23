from typing import Iterable, List

from openai import OpenAI

from safety_client import default_moderation_model, get_client, map_category_scores
from safety_models import BatchModerationResult, ModerationDecision, normalize_text


def moderate_batch(messages: Iterable[str]) -> BatchModerationResult:
    client: OpenAI = get_client()
    payload: List[str] = [normalize_text(message) for message in messages]
    response = client.moderations.create(model=default_moderation_model(), input=payload)
    results = []
    for item in response.results:
        results.append(
            ModerationDecision(
                flagged=bool(item.flagged),
                categories=dict(item.categories),
                category_scores=map_category_scores(getattr(item, "category_scores", None)),
                raw=item.model_dump() if hasattr(item, "model_dump") else {},
            )
        )
    return BatchModerationResult(results=results)
