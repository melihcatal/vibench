from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModerationCategoryScore:
    name: str
    score: float
    flagged: bool = False


@dataclass
class ModerationDecision:
    provider: str
    model: str
    allowed: bool
    flagged: bool
    categories: List[ModerationCategoryScore] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "allowed": self.allowed,
            "flagged": self.flagged,
            "categories": [
                {"name": c.name, "score": c.score, "flagged": c.flagged}
                for c in self.categories
            ],
            "raw": self.raw,
        }


@dataclass
class RedactionResult:
    provider: str
    original_text: str
    redacted_text: str
    flagged: bool
    categories: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "original_text": self.original_text,
            "redacted_text": self.redacted_text,
            "flagged": self.flagged,
            "categories": self.categories,
        }


def normalize_openai_result(result: Any, model: str = "omni-moderation-latest") -> ModerationDecision:
    category_scores = getattr(result, "category_scores", None)
    categories = getattr(result, "categories", None)

    normalized: List[ModerationCategoryScore] = []
    score_map = category_scores.model_dump() if hasattr(category_scores, "model_dump") else {}
    flag_map = categories.model_dump() if hasattr(categories, "model_dump") else {}

    seen = set(score_map) | set(flag_map)
    for name in sorted(seen):
        score = float(score_map.get(name, 0.0) or 0.0)
        flagged = bool(flag_map.get(name, False))
        normalized.append(ModerationCategoryScore(name=name, score=score, flagged=flagged))

    return ModerationDecision(
        provider="OpenAI",
        model=model,
        allowed=not bool(getattr(result, "flagged", False)),
        flagged=bool(getattr(result, "flagged", False)),
        categories=normalized,
        raw=result.model_dump() if hasattr(result, "model_dump") else {},
    )


def category_score_map(decision: ModerationDecision) -> Dict[str, float]:
    return {item.name: item.score for item in decision.categories}
