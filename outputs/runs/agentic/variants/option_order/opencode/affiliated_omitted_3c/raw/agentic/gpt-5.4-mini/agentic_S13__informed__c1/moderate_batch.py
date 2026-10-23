from typing import List, Dict, Any

from safety_client import build_perspective_payload, post_moderation
from safety_models import BatchModerationRequest, ModerationResult, normalize_scores


def moderate_batch(request: BatchModerationRequest) -> List[Dict[str, Any]]:
    results = []
    for text in request.texts:
        raw = post_moderation(
            build_perspective_payload(
                text, [request.language] if request.language else None
            )
        )
        scores = normalize_scores(raw.get("attributeScores", {}))
        score = max(scores.values()) if scores else 0.0
        result = ModerationResult(
            allowed=score < 0.5, score=score, categories=scores, raw=raw
        )
        results.append(
            {
                "allowed": result.allowed,
                "score": result.score,
                "categories": result.categories,
                "raw": result.raw,
            }
        )
    return results
