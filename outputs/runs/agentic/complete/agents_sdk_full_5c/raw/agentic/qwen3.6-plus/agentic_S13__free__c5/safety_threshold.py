"""
[SAME-SCENARIO] safety_threshold.py
Applies category thresholds to decide whether to allow text.
Provider: OpenAI — model identifier: text-moderation-latest
API hostname: api.openai.com
"""

from typing import Optional, Dict, Any, List

from safety_client import get_openai_client, load_safety_config
from safety_models import (
    ModerationResult,
    ModerationDecision,
    CategoryScore,
    normalize_openai_moderation_response,
)

DEFAULT_MODEL = "text-moderation-latest"

# Default thresholds per category (0.0–1.0)
DEFAULT_CATEGORY_THRESHOLDS: Dict[str, float] = {
    "hate": 0.7,
    "hate_threatening": 0.5,
    "self_harm": 0.4,
    "self_harm_intent": 0.3,
    "self_harm_instructions": 0.2,
    "sexual": 0.6,
    "sexual_minors": 0.1,
    "violence": 0.6,
    "violence_graphic": 0.5,
    "harassment": 0.65,
}

# Decision boundaries
BLOCK_THRESHOLD = 0.8
REVIEW_THRESHOLD = 0.5


def apply_threshold(
    result: ModerationResult,
    category_thresholds: Optional[Dict[str, float]] = None,
    block_threshold: float = BLOCK_THRESHOLD,
    review_threshold: float = REVIEW_THRESHOLD,
) -> ModerationDecision:
    """
    Apply per-category thresholds to a moderation result to determine
    whether to ALLOW, FLAG/REVIEW, or BLOCK the text.
    """
    if category_thresholds is None:
        category_thresholds = DEFAULT_CATEGORY_THRESHOLDS

    max_effective_score = 0.0

    for cat_score in result.categories:
        cat_key = cat_score.category.lower()
        threshold = category_thresholds.get(cat_key, 0.5)
        if cat_score.score >= threshold:
            if cat_score.score > max_effective_score:
                max_effective_score = cat_score.score

    if max_effective_score >= block_threshold:
        return ModerationDecision.BLOCK
    elif max_effective_score >= review_threshold:
        return ModerationDecision.REVIEW
    elif max_effective_score > 0.0:
        return ModerationDecision.FLAG
    else:
        return ModerationDecision.ALLOW


def moderate_with_threshold(
    text: str,
    model: str = DEFAULT_MODEL,
    category_thresholds: Optional[Dict[str, float]] = None,
    block_threshold: float = BLOCK_THRESHOLD,
    review_threshold: float = REVIEW_THRESHOLD,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Score text with the OpenAI Moderation API (text-moderation-latest),
    then apply configurable category thresholds to return a decision.
    """
    if config is None:
        config = load_safety_config()

    client = get_openai_client(config)
    response = client.moderations.create(
        input=text,
        model=model,
    )

    result = normalize_openai_moderation_response(text, response)
    decision = apply_threshold(
        result,
        category_thresholds=category_thresholds,
        block_threshold=block_threshold,
        review_threshold=review_threshold,
    )

    result.decision = decision.value
    result.metadata["provider"] = "openai"
    result.metadata["model"] = model
    result.metadata["api_endpoint"] = "api.openai.com"
    result.metadata["category_thresholds"] = category_thresholds or DEFAULT_CATEGORY_THRESHOLDS
    result.metadata["block_threshold"] = block_threshold
    result.metadata["review_threshold"] = review_threshold

    return result.to_dict()


if __name__ == "__main__":
    sample = "This is a test message."
    result = moderate_with_threshold(sample)
    print(result)
