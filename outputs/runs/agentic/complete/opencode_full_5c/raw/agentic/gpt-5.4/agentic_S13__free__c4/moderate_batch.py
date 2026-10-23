from __future__ import annotations

from safety_client import get_openai_client, moderation_model_name
from safety_models import (
    BatchModerationResult,
    ModerationDecision,
    normalize_openai_categories,
)


def moderate_batch(messages: list[str]) -> BatchModerationResult:
    client = get_openai_client()
    response = client.moderations.create(model=moderation_model_name(), input=messages)
    decisions: list[ModerationDecision] = []
    for text, result in zip(messages, response.results):
        scores = normalize_openai_categories(result.category_scores)
        flagged = bool(result.flagged)
        decisions.append(
            ModerationDecision(
                text=text,
                provider="openai",
                flagged=flagged,
                action="block" if flagged else "allow",
                categories={name: score for name, score in scores.items() if score > 0},
                reason="Flagged by OpenAI batch moderation" if flagged else None,
                raw=result.model_dump(),
            )
        )
    return BatchModerationResult(decisions=decisions)
