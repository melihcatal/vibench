from safety_client import (
    get_openai_client,
    build_moderation_payload,
    parse_moderation_response,
    MODERATION_MODEL,
)
from safety_models import ThresholdDecision, CategoryScore, normalize_category_scores

DEFAULT_THRESHOLDS: dict[str, float] = {
    "hate": 0.5,
    "hate/threatening": 0.5,
    "harassment": 0.5,
    "harassment/threatening": 0.5,
    "self-harm": 0.3,
    "self-harm/intent": 0.3,
    "self-harm/instructions": 0.3,
    "sexual": 0.5,
    "sexual/minors": 0.1,
    "violence": 0.5,
    "violence/graphic": 0.5,
    "illicit": 0.4,
    "illicit/violent": 0.4,
}


def safety_threshold(
    text: str,
    thresholds: dict[str, float] | None = None,
    request_id: str | None = None,
    model: str = MODERATION_MODEL,
) -> ThresholdDecision:
    applied = thresholds if thresholds is not None else DEFAULT_THRESHOLDS
    client = get_openai_client()
    payload = build_moderation_payload(text, model=model)
    response = client.moderations.create(**payload)
    parsed = parse_moderation_response(response)
    category_scores = normalize_category_scores(
        parsed["categories"], parsed["category_scores"]
    )
    blocked = False
    for cs in category_scores:
        threshold = applied.get(cs.category, 1.0)
        if cs.score >= threshold:
            blocked = True
            break
    return ThresholdDecision(
        text=text,
        allowed=not blocked,
        category_scores=category_scores,
        applied_thresholds=applied,
        request_id=request_id,
    )
