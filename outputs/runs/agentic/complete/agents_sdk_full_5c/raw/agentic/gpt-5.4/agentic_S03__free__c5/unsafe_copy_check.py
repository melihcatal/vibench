from __future__ import annotations

from translation_client import perspective_analyze
from translation_models import SafetyCheckResult


def check_localized_copy_safety(
    text: str,
    threshold: float = 0.7,
) -> SafetyCheckResult:
    raw = perspective_analyze(text)
    scores: dict[str, float] = {}
    for name, payload in raw.get("attributeScores", {}).items():
        value = payload.get("summaryScore", {}).get("value", 0.0)
        scores[name] = float(value)
    triggered = [name for name, value in scores.items() if value >= threshold]
    rationale = ", ".join(f"{name}={scores[name]:.3f}" for name in sorted(scores))
    return SafetyCheckResult(
        is_safe=not triggered,
        categories=triggered,
        rationale=rationale,
        provider="google_perspective_api",
        raw=raw,
    )
