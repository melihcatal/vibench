from safety_client import AzureContentSafetyClient, get_default_thresholds
from safety_models import (
    ThresholdDecision,
    ThresholdRule,
    normalize_category_scores,
    normalize_text,
)


def safety_threshold(
    text: str, rules: list[ThresholdRule] | None = None
) -> ThresholdDecision:
    client = AzureContentSafetyClient()
    payload = client.moderate_text(normalize_text(text))
    categories = normalize_category_scores(
        payload.get("categories") or payload.get("categoryScores")
    )
    thresholds = {
        rule.category: rule.threshold
        for rule in (
            rules
            or [
                ThresholdRule(category=k, threshold=v)
                for k, v in get_default_thresholds().items()
            ]
        )
    }
    triggered = [
        category
        for category, score in categories.items()
        if score >= thresholds.get(category, 1.0)
    ]
    return ThresholdDecision(
        allowed=not triggered, triggered=triggered, categories=categories, raw=payload
    )
