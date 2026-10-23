from safety_client import prepare_text_payload, post_perspective
from safety_models import (
    BatchModerationRequest,
    ModerationDecision,
    normalize_score,
    normalize_text,
)


def moderate_batch(texts, language=None):
    request = BatchModerationRequest(
        texts=[normalize_text(t) for t in texts], language=language
    )
    decisions = []
    for text in request.texts:
        raw = post_perspective(prepare_text_payload(text, request.language))
        score = normalize_score(
            raw.get("attributeScores", {})
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value")
        )
        decisions.append(
            {"text": text, "allow": score < 0.5, "score": score, "raw": raw}
        )
    return decisions
