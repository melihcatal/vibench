# HELPER: Request/response and normalization helpers for Text Content Safety

import typing


class ModerationRequest(typing.TypedDict):
    input: str | list[str]
    unsafe_content_only: bool | None


class ModerationResult(typing.TypedDict):
    flagged: bool
    categories: dict[str, float]
    unsafe: list[dict] | None


def normalize_response(raw: dict) -> ModerationResult:
    """Convert OpenAI moderation response to a standard shape."""
    result = raw["results"][0]
    return ModerationResult(
        flagged=result.get("flagged", False),
        categories=result.get("categories", {}),
        unsafe=result.get("unsafe"),
    )
