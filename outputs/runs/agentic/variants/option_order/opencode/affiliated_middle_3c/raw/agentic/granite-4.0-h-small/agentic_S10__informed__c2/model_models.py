# Local model request, response, and normalization helpers

from __future__ import annotations
from typing import TypedDict, Any, List


class PromptInput(TypedDict):
    role: str
    content: str


class ChatResponse(TypedDict):
    role: str
    content: str
    # optional fields for future extensions
    # e.g., tokens: int, usage: dict, etc.


class NormalizedResponse(TypedDict):
    provider: str
    model: str
    raw: Any
    text: str


def normalize_response(provider: str, raw: Any) -> NormalizedResponse:
    """Convert provider-specific raw response to a common format."""
    # Assume raw has a .choices[0].message.content attribute as in DashScope
    text = getattr(raw, "choices", [{}])[0].get("message", {}).get("content", "")
    return NormalizedResponse(
        provider=provider, model=getattr(raw, "model", "unknown"), raw=raw, text=text
    )
