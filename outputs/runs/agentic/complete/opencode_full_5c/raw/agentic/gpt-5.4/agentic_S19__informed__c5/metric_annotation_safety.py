from __future__ import annotations

from observability_client import post_perspective
from observability_models import SafetyCheckResponse


def metric_annotation_safety(text: str, threshold: float = 0.7) -> SafetyCheckResponse:
    result = post_perspective(text)
    attribute_scores = result.get("attributeScores", {})
    scores = {
        name.lower(): float(details["summaryScore"]["value"])
        for name, details in attribute_scores.items()
        if "summaryScore" in details
    }
    flagged_categories = [name for name, score in scores.items() if score >= threshold]
    return SafetyCheckResponse(
        is_safe=not flagged_categories,
        flagged_categories=flagged_categories,
        scores=scores,
    )
