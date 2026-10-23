from typing import List

from openai import OpenAI

from safety_client import get_client, load_config
from safety_models import BatchModerationResult, ModerationDecision, normalize_messages


def moderate_batch(messages: List[str]) -> BatchModerationResult:
    cfg = load_config()
    client: OpenAI = get_client(cfg)
    normalized = normalize_messages(messages)
    result = client.moderations.create(model="omni-moderation-latest", input=normalized)
    decisions = []
    for item in result.results:
        decisions.append(
            ModerationDecision(
                allowed=not item.flagged,
                categories=dict(item.categories),
                scores=dict(item.category_scores),
                model="omni-moderation-latest",
                raw=result.model_dump() if hasattr(result, "model_dump") else None,
            )
        )
    return BatchModerationResult(decisions=decisions)
