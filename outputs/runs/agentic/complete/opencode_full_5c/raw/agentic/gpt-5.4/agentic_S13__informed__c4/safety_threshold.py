from __future__ import annotations

from typing import Any

from safety_client import analyze_text
from safety_models import SafetyRequest


DEFAULT_THRESHOLDS = {
    "hate": 2.0,
    "self_harm": 1.0,
    "sexual": 2.0,
    "violence": 2.0,
}


def apply_safety_threshold(
    text: str, thresholds: dict[str, float] | None = None
) -> dict[str, Any]:
    result = analyze_text(SafetyRequest(text=text))
    active_thresholds = {**DEFAULT_THRESHOLDS, **(thresholds or {})}
    blocked_categories = {
        category: score
        for category, score in result.categories.items()
        if score >= active_thresholds.get(category, 999.0)
    }
    return {
        "provider": "azure-ai-content-safety",
        "allow": not blocked_categories,
        "blocked_categories": blocked_categories,
        "thresholds": active_thresholds,
        "categories": result.categories,
    }
