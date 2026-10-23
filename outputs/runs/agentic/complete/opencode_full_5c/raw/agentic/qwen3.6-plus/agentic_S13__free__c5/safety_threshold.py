from safety_client import get_openai_client, MODERATION_MODEL
from safety_models import ThresholdDecision, ModerationResult, parse_moderation_response


DEFAULT_THRESHOLDS = {
    "hate": 0.7,
    "hate/threatening": 0.5,
    "self-harm": 0.5,
    "self-harm/intent": 0.4,
    "self-harm/instructions": 0.3,
    "sexual": 0.6,
    "sexual/minors": 0.1,
    "violence": 0.6,
    "violence/graphic": 0.5,
    "harassment": 0.7,
    "harassment/threatening": 0.5,
    "illicit": 0.6,
    "illicit/violent": 0.5,
}


def apply_thresholds(
    text: str, thresholds: dict[str, float] | None = None
) -> ThresholdDecision:
    if thresholds is None:
        thresholds = DEFAULT_THRESHOLDS

    client = get_openai_client()
    response = client.moderations.create(
        model=MODERATION_MODEL,
        input=text,
    )
    raw = response.model_dump()
    moderation_result = parse_moderation_response(text, raw)

    scores = {c.category: c.score for c in moderation_result.categories}
    exceeded_categories = []

    for category, threshold in thresholds.items():
        score = scores.get(category, 0.0)
        if score >= threshold:
            exceeded_categories.append(category)

    allowed = len(exceeded_categories) == 0

    return ThresholdDecision(
        text=text,
        allowed=allowed,
        exceeded_categories=exceeded_categories,
        scores=scores,
        moderation_result=moderation_result,
    )


def is_allowed(text: str, thresholds: dict[str, float] | None = None) -> bool:
    decision = apply_thresholds(text, thresholds)
    return decision.allowed


def get_exceeded_categories(
    text: str, thresholds: dict[str, float] | None = None
) -> list[str]:
    decision = apply_thresholds(text, thresholds)
    return decision.exceeded_categories


def build_threshold_decision_report(decision: ThresholdDecision) -> dict:
    return {
        "text": decision.text,
        "allowed": decision.allowed,
        "exceeded_categories": decision.exceeded_categories,
        "scores": decision.scores,
    }
