from __future__ import annotations

from typing import Any, Dict

from safety_client import SafetyClient
from safety_models import ModerationDecision, ModerationRequest, best_category, extract_category_scores, normalize_severity


def moderate_text(request: ModerationRequest) -> ModerationDecision:
    client = SafetyClient()
    payload: Dict[str, Any] = client.analyze_text(request.text)
    scores = extract_category_scores(payload)
    category = best_category(scores)
    severity = scores.get(category, normalize_severity(payload.get("severity")))
    allow = severity < 0.5 and not bool(payload.get("blocked", False))
    return ModerationDecision(
        allow=allow,
        category=category,
        severity=severity,
        rationale=payload.get("rationale") or payload.get("reason"),
        raw=payload,
    )
