"""
Local request, response, and normalization helpers for Text Content Safety.

Provides dataclasses and utilities for modeling moderation requests,
category scores, and OpenAI moderation API responses.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from openai.types import Moderation, ModerationCreateParams


class SeverityLevel(str, Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ModerationRequest:
    """Normalized request payload for a single moderation call."""

    text: str
    categories: Optional[List[str]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CategoryScore:
    """Normalized score for a single moderation category."""

    category: str
    score: float
    flagged: bool


@dataclass
class ModerationResult:
    """Normalized result from a moderation call."""

    text: str
    flagged: bool
    category_scores: List[CategoryScore] = field(default_factory=list)
    severity: SeverityLevel = SeverityLevel.SAFE
    raw_response: Optional[Moderation] = None

    @property
    def max_score(self) -> float:
        if not self.category_scores:
            return 0.0
        return max(cs.score for cs in self.category_scores)

    @property
    def highest_category(self) -> Optional[str]:
        if not self.category_scores:
            return None
        return max(self.category_scores, key=lambda cs: cs.score).category


@dataclass
class BatchModerationRequest:
    """Normalized request for batch moderation."""

    texts: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationResult:
    """Normalized result from batch moderation."""

    results: List[ModerationResult] = field(default_factory=list)
    overall_flagged_count: int = 0
    total_texts: int = 0


def normalize_openai_moderation(
    raw: Moderation, text: str
) -> ModerationResult:
    """Convert an OpenAI Moderation response to a normalized ModerationResult."""
    cats = raw.categories
    cat_scores = raw.category_scores

    category_scores: List[CategoryScore] = []
    for cat_name in cats.model_fields_set if hasattr(cats, "model_fields_set") else dir(cats):
        if cat_name.startswith("_") or cat_name in ("model_config",):
            continue
        try:
            flagged_val = getattr(cats, cat_name, None)
            score_val = getattr(cat_scores, cat_name, None)
            if flagged_val is not None and score_val is not None:
                category_scores.append(
                    CategoryScore(
                        category=cat_name,
                        score=float(score_val),
                        flagged=bool(flagged_val),
                    )
                )
        except AttributeError:
            continue

    overall_flagged = any(cs.flagged for cs in category_scores)
    max_score = max((cs.score for cs in category_scores), default=0.0)

    if max_score > 0.8:
        severity = SeverityLevel.CRITICAL
    elif max_score > 0.6:
        severity = SeverityLevel.HIGH
    elif max_score > 0.4:
        severity = SeverityLevel.MEDIUM
    elif max_score > 0.15:
        severity = SeverityLevel.LOW
    else:
        severity = SeverityLevel.SAFE

    return ModerationResult(
        text=text,
        flagged=overall_flagged,
        category_scores=category_scores,
        severity=severity,
        raw_response=raw,
    )


def build_openai_moderation_params(
    text: str,
) -> ModerationCreateParams:
    """Build the OpenAI ModerationCreateParams for the omni-moderation-latest model."""
    return ModerationCreateParams(
        input=text,
        model="omni-moderation-latest",
    )


def get_openai_api_key() -> str:
    """Retrieve the OpenAI API key from environment."""
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable must be set for moderation."
        )
    return key
