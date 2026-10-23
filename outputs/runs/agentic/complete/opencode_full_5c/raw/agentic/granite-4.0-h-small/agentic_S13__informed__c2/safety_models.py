# [HELPER] safety_models.py
"""Local request, response, and normalization helpers for Text Content Safety.
Defines simple dataclasses to represent API requests/responses and normalizes them to a common format.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List


@dataclass
class ModerationRequest:
    """Normalized request payload passed to scoring functions."""

    text: str
    # Future extensions: context, user_id, etc.


@dataclass
class ModerationResponse:
    """Unified response shape from the local helper client."""

    label: str  # e.g., 'safe', 'harassment'
    score: float  # confidence 0.0‑1.0
    unsafe_spans: List[dict]  # [{'start': int, 'end': int}, ...] optional


def normalize_response(raw: dict[str, Any]) -> ModerationResponse:
    """Convert provider‑specific response to the local ModerationResponse."""
    return ModerationResponse(
        label=raw.get("label", "safe"),
        score=raw.get("score", 0.0),
        unsafe_spans=raw.get("unsafe_spans", []),
    )
