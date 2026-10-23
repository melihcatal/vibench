# [HELPER] safety_models.py
# Define local request, response, and normalization helpers for Text Content Safety

from typing import TypedDict, List


class ModerationRequest(TypedDict):
    """Payload sent to the moderation endpoint."""

    input: str
    categories: List[str]


class ModerationResponse(TypedDict):
    """Normalized response from the moderation service."""

    categories: dict[str, float]  # category -> score
    flagged: bool


def normalize_moderation_response(raw: dict) -> ModerationResponse:
    """Convert provider-specific response to our canonical format."""
    # Example for OpenAI: raw['categories'] is dict[category: bool]
    categories = {cat: float(val) for cat, val in raw.get("categories", {}).items()}
    return ModerationResponse(categories=categories, flagged=raw.get("flagged", False))
