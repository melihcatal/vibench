from typing import TypedDict, List


class SafetySpan(TypedDict):
    """Represent a single unsafe span detected by a moderation service. Start index is inclusive, end index is exclusive."""

    startIndex: int
    endIndex: int


class SafetyResponse(TypedDict):
    """Generic wrapper for moderation service responses. The concrete shape depends on the downstream model (e.g., Perspective, Granite)."""

    text: str
    scores: dict
    unsafeSpans: List[SafetySpan]


class SafetyModelConfig(TypedDict):
    """Configuration required to instantiate a safety model client. Implementations must supply these fields via environment variables."""

    API_KEY: str
    ENDPOINT: str


# ----------------------------------------------------------------------
# Helper for normalizing a generic moderation response into our internal format.
# ----------------------------------------------------------------------


def normalize_response(raw: dict) -> SafetyResponse:
    """Adapt an external service's output to the SafetyResponse schema. Currently assumes Perspective‑API style attributeScores."""
    # Placeholder – real normalization will parse the incoming raw dict.
    return {
        "text": raw.get("text"),
        "scores": raw.get("scores"),  # may contain TOXICITY, SEVERE_TOXICITY etc.
        "unsafeSpans": raw.get("unsafeSpans", []),
    }
