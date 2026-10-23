"""Apply category thresholds to decide whether to allow text using OpenAI Moderation API."""

import os
from typing import Dict

from openai import OpenAI

from safety_client import get_safety_config
from safety_models import ModerationRequest, ModerationResponse, normalize_openai_categories


# Default thresholds for category scores; scores above threshold trigger action.
DEFAULT_CATEGORY_THRESHOLDS: Dict[str, float] = {
    "hate": 0.5,
    "hate/threatening": 0.5,
    "self-harm": 0.5,
    "self-harm/intent": 0.5,
    "self-harm/instructions": 0.5,
    "sexual": 0.5,
    "sexual/minors": 0.3,
    "violence": 0.5,
    "violence/graphic": 0.5,
}


def apply_safety_threshold(
    text: str,
    custom_thresholds: Dict[str, float] | None = None,
) -> ModerationResponse:
    """Apply category thresholds to decide whether to allow text.

    Uses OpenAI's text-moderation-latest model via api.openai.com. Each category score
    is compared against configurable thresholds. If any score exceeds its threshold,
    the text is flagged as blocked.

    Args:
        text: The input text to evaluate.
        custom_thresholds: Optional dict mapping category names to float thresholds.
            Falls back to DEFAULT_CATEGORY_THRESHOLDS if not provided.

    Returns:
        ModerationResponse with threshold-based decision and per-category details.
    """
    config = get_safety_config()
    client = OpenAI(api_key=config.get("openai_api_key", os.environ.get("OPENAI_API_KEY", "")))

    request = ModerationRequest(
        model="text-moderation-latest",
        input=text,
    )

    response = client.moderations.create(
        model=request.model,
        input=request.input,
    )

    result = response.results[0]
    categories = normalize_openai_categories(result.categories)
    category_scores = normalize_openai_categories(result.category_scores, as_float=True)

    thresholds = custom_thresholds if custom_thresholds is not None else DEFAULT_CATEGORY_THRESHOLDS

    threshold_exceeded = False
    exceeded_categories = []
    for cat, score in category_scores.items():
        if cat in thresholds and score > thresholds[cat]:
            threshold_exceeded = True
            exceeded_categories.append(cat)

    return ModerationResponse(
        flagged=threshold_exceeded,
        categories=categories,
        category_scores=category_scores,
        model="text-moderation-latest",
        provider="openai",
        provider_endpoint="api.openai.com",
        thresholds_applied=thresholds,
        exceeded_categories=exceeded_categories,
    )


if __name__ == "__main__":
    import sys
    sample = sys.argv[1] if len(sys.argv) > 1 else "Evaluate this message."
    result = apply_safety_threshold(sample)
    print(result.to_dict())
