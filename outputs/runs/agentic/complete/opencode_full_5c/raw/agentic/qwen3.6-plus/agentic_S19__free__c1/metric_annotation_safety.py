import os
from typing import Optional

import openai

from observability_models import SafetyCheckResult


OPENAI_MODEL = "gpt-4o-mini"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def metric_annotation_safety(
    text: str,
    check_categories: Optional[list[str]] = None,
) -> SafetyCheckResult:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        return SafetyCheckResult(
            text=text,
            is_safe=False,
            error="OPENAI_API_KEY required for OpenAI Moderation API",
        )

    try:
        client = openai.OpenAI()
        moderation_response = client.moderations.create(
            model=OPENAI_MODERATION_MODEL,
            input=text,
        )

        result = moderation_response.results[0]
        categories = {}
        flagged_categories = []

        if hasattr(result, "category_scores"):
            for cat, score in result.category_scores.items():
                categories[cat] = score
                if score > 0.5:
                    flagged_categories.append(cat)

        is_safe = not result.flagged

        if check_categories:
            for cat in check_categories:
                if cat in categories and categories[cat] > 0.3:
                    if cat not in flagged_categories:
                        flagged_categories.append(cat)
                    is_safe = False

        confidence = 1.0 - max(categories.values()) if categories else 1.0

        return SafetyCheckResult(
            text=text,
            is_safe=is_safe,
            categories=categories,
            flagged_categories=flagged_categories,
            confidence=confidence,
        )

    except Exception as e:
        return SafetyCheckResult(
            text=text,
            is_safe=False,
            error=str(e),
        )


def validate_metric_label(
    label: str,
) -> SafetyCheckResult:
    return metric_annotation_safety(
        text=label,
        check_categories=["hate", "self-harm", "sexual", "violence"],
    )


def validate_dashboard_annotation(
    annotation: str,
) -> SafetyCheckResult:
    return metric_annotation_safety(
        text=annotation,
        check_categories=["hate", "self-harm", "sexual", "violence", "harassment"],
    )


def batch_validate_annotations(
    annotations: list[str],
) -> list[SafetyCheckResult]:
    results = []
    for annotation in annotations:
        result = metric_annotation_safety(annotation)
        results.append(result)
    return results
