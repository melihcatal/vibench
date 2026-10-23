"""
Local helper: safety_models.py
Define local request, response, and normalization helpers for Text Content Safety.
Works with OpenAI Moderation API category schemas.
"""

from dataclasses import dataclass, field
from typing import Optional


OPENAI_CATEGORIES = [
    "sexual",
    "hate",
    "harassment",
    "self-harm",
    "sexual/minors",
    "hate/threatening",
    "violence/graphic",
    "self-harm/intent",
    "self-harm/instructions",
    "harassment/threatening",
    "violence",
]


@dataclass
class SafetyRequest:
    """Normalized request payload for a single text moderation call."""
    text: str
    model: str = "text-moderation-latest"


@dataclass
class CategoryScore:
    """Represents a single category score from OpenAI moderation."""
    category: str
    flagged: bool
    score: float


@dataclass
class ModerationResponse:
    """Normalized response from a moderation API call."""
    flagged: bool
    categories: list[CategoryScore] = field(default_factory=list)
    raw: Optional[dict] = None

    @property
    def category_flags(self) -> dict[str, bool]:
        return {c.category: c.flagged for c in self.categories}

    @property
    def category_scores(self) -> dict[str, float]:
        return {c.category: c.score for c in self.categories}


@dataclass
class BatchModerationResponse:
    """Normalized response for batch moderation."""
    results: list[ModerationResponse] = field(default_factory=list)

    @property
    def all_flagged(self) -> list[int]:
        return [i for i, r in enumerate(self.results) if r.flagged]

    @property
    def safe_count(self) -> int:
        return sum(1 for r in self.results if not r.flagged)


def normalize_moderation_result(raw_result: dict) -> ModerationResponse:
    """
    Normalize a raw OpenAI moderation result dict into a ModerationResponse.

    Args:
        raw_result: Dict from OpenAI moderation API (categories + category_scores).

    Returns:
        Normalized ModerationResponse.
    """
    categories = raw_result.get("categories", {})
    scores = raw_result.get("category_scores", {})
    category_scores = []

    for cat in OPENAI_CATEGORIES:
        if cat in categories:
            category_scores.append(
                CategoryScore(
                    category=cat,
                    flagged=categories.get(cat, False),
                    score=float(scores.get(cat, 0.0)),
                )
            )

    return ModerationResponse(
        flagged=raw_result.get("flagged", False),
        categories=category_scores,
        raw=raw_result,
    )


def normalize_batch_results(raw_results: list[dict]) -> BatchModerationResponse:
    """
    Normalize a list of raw OpenAI moderation results into a BatchModerationResponse.

    Args:
        raw_results: List of raw moderation result dicts.

    Returns:
        Normalized BatchModerationResponse.
    """
    return BatchModerationResponse(
        results=[normalize_moderation_result(r) for r in raw_results]
    )
