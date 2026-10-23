from __future__ import annotations

from typing import Dict

from safety_client import SafetyClient
from safety_models import ModerationDecision, ModerationRequest, ThresholdConfig, extract_category_scores, normalize_severity


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "hate": 0.4,
    "self_harm": 0.3,
    "sexual": 0.4,
    "violence": 0.5,
}


def safety_threshold(request: ModerationRequest, config: ThresholdConfig | None = None) -> ModerationDecision:
    client = SafetyClient()
    payload = client.analyze_text(request.text)
    scores = extract_category_scores(payload)
    thresholds = (config.thresholds if config else DEFAULT_THRESHOLDS)
    default_threshold = config.default_threshold if config else 0.5
    category = max(scores, key=scores.get) if scores else "unknown"
    severity = scores.get(category, normalize_severity(payload.get("severity")))
    threshold = thresholds.get(category, default_threshold)
    allow = severity < threshold
    return ModerationDecision(
        allow=allow,
        category=category,
        severity=severity,
        rationale=f"threshold={threshold}",
        raw=payload,
    )
