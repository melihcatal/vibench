from typing import TypedDict


class ModerationRequest(TypedDict):
    """Normalized request payload for safety checks."""
    text: str
    category: str | None = None  # optional category filter


class ModerationResponse(TypedDict):
    """Normalized response from a safety provider."""
    flagged: bool
    categories: dict[str, bool]  # e.g., {\"harassment\": True, \"self-harm\": False}


def normalize_response(raw: dict) -> ModerationResponse:
    """Convert provider-specific raw response to our standard ModerationResponse."""
    # Assume raw follows OpenAI Moderation result shape.
    result = raw["results"][0]
    return ModerationResponse(
        flagged=result["flagged"],
        categories={cat["category_name"]: cat["flagged"] for cat in result.get("categories", [])},
    )
