from __future__ import annotations

from security_client import PERSPECTIVE_PROVIDER, perspective_analyze
from security_models import PayloadSafetyRequest, PayloadSafetyResponse


def payload_safety(request: PayloadSafetyRequest) -> PayloadSafetyResponse:
    result = perspective_analyze(request.text)
    scores = {
        key.lower(): value["summaryScore"]["value"]
        for key, value in result.get("attributeScores", {}).items()
    }
    blocked = any(score >= 0.8 for score in scores.values())
    return PayloadSafetyResponse(
        provider=PERSPECTIVE_PROVIDER,
        blocked=blocked,
        scores=scores,
        raw_result=result,
    )
