from safety_client import AzureContentSafetyClient
from safety_models import (
    ModerationDecision,
    ModerationRequest,
    normalize_category_scores,
    normalize_text,
)


def moderate_text(request: ModerationRequest) -> ModerationDecision:
    client = AzureContentSafetyClient()
    payload = client.moderate_text(normalize_text(request.text))
    categories = normalize_category_scores(
        payload.get("categories") or payload.get("categoryScores")
    )
    score = max(categories.values(), default=float(payload.get("score", 0.0)))
    return ModerationDecision(
        allowed=not bool(payload.get("blocked", score >= 0.5)),
        score=score,
        categories=categories,
        raw=payload,
    )
