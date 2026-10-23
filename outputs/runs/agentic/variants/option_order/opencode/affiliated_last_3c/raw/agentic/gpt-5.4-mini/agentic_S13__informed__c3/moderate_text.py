from safety_client import prepare_text_payload, post_perspective
from safety_models import (
    ModerationDecision,
    ModerationRequest,
    normalize_score,
    normalize_text,
)


def moderate_text(text, language=None):
    request = ModerationRequest(text=normalize_text(text), language=language)
    payload = prepare_text_payload(request.text, request.language)
    raw = post_perspective(payload)
    score = normalize_score(
        raw.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value")
    )
    return ModerationDecision(
        allow=score < 0.5, score=score, categories={"TOXICITY": score}, raw=raw
    )
