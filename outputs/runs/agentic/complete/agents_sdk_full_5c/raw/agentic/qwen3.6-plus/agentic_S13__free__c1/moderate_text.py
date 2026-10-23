"""
[SAME-SCENARIO] moderate_text.py
Scores user text for unsafe or policy-violating content.
Uses the OpenAI Moderation API via the openai SDK (text-moderation-latest model).
"""

from typing import Optional

from safety_client import get_openai_client, call_moderation_api
from safety_models import (
    SafetyRequest,
    ModerationResponse,
    normalize_moderation_result,
    OPENAI_CATEGORIES,
)


def moderate_text(
    text: str,
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> ModerationResponse:
    """
    Score a single user text for unsafe or policy-violating content
    using the OpenAI Moderation API.

    Args:
        text: The user text to moderate.
        api_key: Optional OpenAI API key. Falls back to OPENAI_API_KEY env var.
        model: OpenAI moderation model identifier (default: text-moderation-latest).

    Returns:
        ModerationResponse with per-category flags and scores.
    """
    request = SafetyRequest(text=text, model=model)
    client = get_openai_client(api_key=api_key)

    raw_result = call_moderation_api(client, request.text, model=request.model)
    return normalize_moderation_result(raw_result)


def get_top_violations(
    response: ModerationResponse,
    limit: int = 3,
) -> list[tuple[str, float]]:
    """
    Return the top N categories by score from a moderation response.

    Args:
        response: ModerationResponse from moderate_text.
        limit: Maximum number of categories to return.

    Returns:
        List of (category, score) tuples sorted by descending score.
    """
    scored = [
        (c.category, c.score)
        for c in response.categories
        if c.flagged or c.score > 0.0
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]


def is_safe(
    text: str,
    api_key: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> bool:
    """
    Quick check whether text is considered safe (not flagged).

    Args:
        text: The user text to check.
        api_key: Optional OpenAI API key.
        model: OpenAI moderation model identifier.

    Returns:
        True if the text is not flagged by OpenAI moderation.
    """
    result = moderate_text(text, api_key=api_key, model=model)
    return not result.flagged
