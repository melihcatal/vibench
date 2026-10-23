from safety_client import analyze_text
from safety_models import (
    AZURE_CONTENT_SAFETY_CATEGORIES,
    CategoryScore,
    ThresholdConfig,
    ThresholdDecision,
)


def apply_thresholds(
    text: str,
    thresholds: ThresholdConfig | None = None,
) -> ThresholdDecision:
    if thresholds is None:
        thresholds = ThresholdConfig()

    result = analyze_text(text, AZURE_CONTENT_SAFETY_CATEGORIES)

    thresholds_applied = {}
    exceeded_categories = []

    for cat_score in result.category_scores:
        threshold = thresholds.get_threshold(cat_score.category)
        thresholds_applied[cat_score.category] = threshold
        if cat_score.score >= threshold:
            exceeded_categories.append(cat_score.category)

    allowed = len(exceeded_categories) == 0

    if allowed:
        reason = "All category scores are below configured thresholds."
    else:
        reason = (
            f"Text blocked due to exceeding thresholds in: "
            f"{', '.join(exceeded_categories)}."
        )

    return ThresholdDecision(
        text=text,
        allowed=allowed,
        reason=reason,
        scores=result.category_scores,
        thresholds_applied=thresholds_applied,
    )
