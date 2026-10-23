from __future__ import annotations

from typing import Any


def normalize_moderation_result(result: Any) -> dict:
    categories = getattr(result, "categories", {}) or {}
    category_scores = getattr(result, "category_scores", {}) or {}
    return {
        "flagged": bool(getattr(result, "flagged", False)),
        "categories": dict(categories),
        "category_scores": dict(category_scores),
    }


def redact_text_with_categories(text: str, categories: dict) -> str:
    if not categories:
        return text
    redacted = text
    for name, enabled in categories.items():
        if enabled:
            redacted = redacted.replace(name, "[REDACTED]")
    return redacted


def should_allow_by_thresholds(category_scores: dict, thresholds: dict) -> bool:
    for category, threshold in thresholds.items():
        if float(category_scores.get(category, 0.0)) >= float(threshold):
            return False
    return True
