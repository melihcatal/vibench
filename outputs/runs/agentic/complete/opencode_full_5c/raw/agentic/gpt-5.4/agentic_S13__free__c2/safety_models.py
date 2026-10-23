from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyRequest:
    text: str
    categories: List[str] = field(default_factory=list)
    language: str = "en"


@dataclass
class CategoryScore:
    name: str
    score: float
    flagged: bool


@dataclass
class SafetyDecision:
    text: str
    flagged: bool
    action: str
    provider: str
    model: Optional[str] = None
    redacted_text: Optional[str] = None
    categories: List[CategoryScore] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_openai_moderation_result(
    text: str, result: Dict[str, Any]
) -> SafetyDecision:
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    normalized = [
        CategoryScore(
            name=name,
            score=float(category_scores.get(name, 0.0)),
            flagged=bool(flagged),
        )
        for name, flagged in categories.items()
    ]
    flagged = any(item.flagged for item in normalized)
    return SafetyDecision(
        text=text,
        flagged=flagged,
        action="block" if flagged else "allow",
        provider="openai",
        model=result.get("model") or "omni-moderation-latest",
        categories=normalized,
        raw=result,
    )


def category_score_map(decision: SafetyDecision) -> Dict[str, float]:
    return {item.name: item.score for item in decision.categories}


def flagged_categories(decision: SafetyDecision) -> List[str]:
    return [item.name for item in decision.categories if item.flagged]
