"""
[SAME-SCENARIO] safety_threshold.py
Applies category thresholds to decide whether to allow text.
Uses the OpenAI Moderation API via the openai SDK (text-moderation-latest model).
"""

from typing import Optional

from safety_client import get_openai_client, call_moderation_api
from safety_models import (
    ModerationResponse,
    normalize_moderation_result,
    OPENAI_CATEGORIES,
)


DEFAULT_THRESHOLDS: dict[str, float] = {
    "sexual": 0.5,
    "hate": 0.4,
    "harassment": 0.4,
    "self-harm": 0.3,
    "sexual/minors": 0.2,
    "hate/threatening": 0.3,
    "violence/graphic": 0.4,
    "self-harm/intent": 0.2,
    "self-harm/instructions": 0.2,
    "harassment/threatening": 0.3,
    "violence": 0.5,
}

STRICT_THRESHOLDS: dict[str, float] = {
    "sexual": 0.2,
    "hate": 0.15,
    "harassment": 0.15,
    "self-harm": 0.1,
    "sexual/minors": 0.05,
    "hate/threatening": 0.1,
    "violence/graphic": 0.15,
    "self-harm/intent": 0.05,
    "self-harm/instructions": 0.05,
    "harassment/threatening": 0.1,
    "violence": 0.2,
}


def apply_thresholds(
    text: str,
    thresholds: Optional[dict[str, float]] = None,
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> tuple[bool, ModerationResponse, dict[str, bool]]:
    """
    Apply per-category score thresholds to decide whether to allow text.

    Args:
        text: The text to evaluate.
        thresholds: Dict mapping category names to score thresholds.
            Uses DEFAULT_THRESHOLDS if not provided.
        api_key: Optional OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI moderation model identifier (default: text-moderation-latest).

    Returns:
        Tuple of (allowed, response, threshold_results) where:
            - allowed: True if text passes all thresholds
            - response: Full ModerationResponse from OpenAI
            - threshold_results: Dict of category -> whether it exceeds threshold
    """
    client = get_openai_client(api_key=api_key)
    raw_result = call_moderation_api(client, text, model=model)
    response = normalize_moderation_result(raw_result)

    active_thresholds = thresholds if thresholds is not None else DEFAULT_THRESHOLDS

    threshold_results = {}
    allowed = True

    for category_score in response.categories:
        threshold = active_thresholds.get(category_score.category, 0.5)
        exceeds = category_score.score >= threshold
        threshold_results[category_score.category] = exceeds
        if exceeds:
            allowed = False

    return allowed, response, threshold_results


def check_allow_text(
    text: str,
    strict: bool = False,
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> bool:
    """
    Quick boolean check: should this text be allowed?

    Args:
        text: The text to check.
        strict: If True, use STRICT_THRESHOLDS; otherwise use DEFAULT_THRESHOLDS.
        api_key: Optional OpenAI API key.
        model: OpenAI moderation model identifier.

    Returns:
        True if the text should be allowed, False otherwise.
    """
    thresholds = STRICT_THRESHOLDS if strict else DEFAULT_THRESHOLDS
    allowed, _, _ = apply_thresholds(text, thresholds, api_key=api_key, model=model)
    return allowed


def get_blocked_categories(
    text: str,
    thresholds: Optional[dict[str, float]] = None,
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> list[str]:
    """
    Return the list of categories that exceed their thresholds.

    Args:
        text: The text to evaluate.
        thresholds: Custom threshold dict.
        api_key: Optional OpenAI API key.
        model: OpenAI moderation model identifier.

    Returns:
        List of category names that exceed their thresholds.
    """
    _, _, threshold_results = apply_thresholds(
        text, thresholds, api_key=api_key, model=model
    )
    return [cat for cat, exceeded in threshold_results.items() if exceeded]
