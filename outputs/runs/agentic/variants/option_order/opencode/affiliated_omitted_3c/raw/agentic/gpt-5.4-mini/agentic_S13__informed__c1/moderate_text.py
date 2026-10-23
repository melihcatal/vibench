from safety_client import build_perspective_payload, post_moderation
from safety_models import ModerationRequest, ModerationResult, normalize_scores


def moderate_text(request: ModerationRequest) -> ModerationResult:
    payload = build_perspective_payload(
        request.text, [request.language] if request.language else None
    )
    raw = post_moderation(payload)
    scores = normalize_scores(raw.get("attributeScores", {}))
    score = max(scores.values()) if scores else 0.0
    return ModerationResult(
        allowed=score < 0.5, score=score, categories=scores, raw=raw
    )
