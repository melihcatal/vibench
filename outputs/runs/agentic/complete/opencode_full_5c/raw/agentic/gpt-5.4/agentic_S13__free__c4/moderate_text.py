from __future__ import annotations

from safety_client import get_openai_client, moderation_model_name
from safety_models import ModerationDecision, normalize_openai_categories


def moderate_text(text: str) -> ModerationDecision:
    client = get_openai_client()
    response = client.moderations.create(model=moderation_model_name(), input=text)
    result = response.results[0]
    scores = normalize_openai_categories(result.category_scores)
    flagged = bool(result.flagged)
    categories = {name: score for name, score in scores.items() if score > 0}
    reason = None
    if flagged:
        top_category = max(
            categories.items(), key=lambda item: item[1], default=(None, 0.0)
        )[0]
        reason = (
            f"Flagged by OpenAI moderation category: {top_category}"
            if top_category
            else "Flagged by OpenAI moderation"
        )
    return ModerationDecision(
        text=text,
        provider="openai",
        flagged=flagged,
        action="block" if flagged else "allow",
        categories=categories,
        reason=reason,
        raw=response.model_dump(),
    )
