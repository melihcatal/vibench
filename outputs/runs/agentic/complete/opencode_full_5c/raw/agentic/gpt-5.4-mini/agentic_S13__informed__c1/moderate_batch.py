from typing import List

from safety_client import AzureContentSafetyClient
from safety_models import (
    BatchModerationRequest,
    ModerationDecision,
    normalize_category_scores,
    normalize_text,
)


def moderate_batch(request: BatchModerationRequest) -> List[ModerationDecision]:
    client = AzureContentSafetyClient()
    payload = client.moderate_batch([normalize_text(text) for text in request.texts])
    results = []
    for item in payload.get("results", payload.get("value", [])):
        categories = normalize_category_scores(
            item.get("categories") or item.get("categoryScores")
        )
        score = max(categories.values(), default=float(item.get("score", 0.0)))
        results.append(
            ModerationDecision(
                allowed=not bool(item.get("blocked", score >= 0.5)),
                score=score,
                categories=categories,
                raw=item,
            )
        )
    return results
