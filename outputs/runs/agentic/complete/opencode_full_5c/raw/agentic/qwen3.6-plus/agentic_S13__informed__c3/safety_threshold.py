from safety_models import (
    SafetyCategory,
    SeverityLevel,
    SafetyRequest,
    SafetyResponse,
    ThresholdConfig,
    ThresholdDecision,
    CategoryScore,
)
from safety_client import call_azure_content_safety


def apply_safety_threshold(
    text: str,
    threshold_config: ThresholdConfig | None = None,
    categories: list[SafetyCategory] | None = None,
) -> ThresholdDecision:
    if threshold_config is None:
        threshold_config = ThresholdConfig()
    if categories is None:
        categories = list(SafetyCategory)

    request = SafetyRequest(text=text, categories=categories)
    response = call_azure_content_safety(request)

    return evaluate_threshold(response, threshold_config)


def evaluate_threshold(
    response: SafetyResponse,
    threshold_config: ThresholdConfig,
) -> ThresholdDecision:
    violated = []
    exceeded = {}

    for score in response.category_scores:
        threshold = threshold_config.thresholds.get(score.category)
        if threshold is None:
            continue

        if score.severity.value >= threshold.value:
            violated.append(score.category)
            exceeded[score.category] = score.severity

    allowed = len(violated) == 0

    if threshold_config.action == "block":
        allowed = len(violated) == 0
    elif threshold_config.action == "warn":
        allowed = True

    return ThresholdDecision(
        allowed=allowed,
        text=response.text,
        violated_categories=violated,
        exceeded_thresholds=exceeded,
        raw_scores=response.category_scores,
    )


def apply_thresholds_batch(
    texts: list[str],
    threshold_config: ThresholdConfig | None = None,
    categories: list[SafetyCategory] | None = None,
) -> list[ThresholdDecision]:
    decisions = []
    for text in texts:
        decision = apply_safety_threshold(text, threshold_config, categories)
        decisions.append(decision)
    return decisions


def threshold_decision_summary(decision: ThresholdDecision) -> dict:
    return {
        "allowed": decision.allowed,
        "text": decision.text,
        "violated_categories": [c.value for c in decision.violated_categories],
        "exceeded_thresholds": {
            k.value: v.name for k, v in decision.exceeded_thresholds.items()
        },
        "scores": [
            {
                "category": s.category.value,
                "severity": s.severity.name,
                "score": s.raw_score,
            }
            for s in decision.raw_scores
        ],
    }
