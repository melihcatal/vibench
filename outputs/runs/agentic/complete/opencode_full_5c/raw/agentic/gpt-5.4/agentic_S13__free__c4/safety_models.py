from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SafetyCategoryScore:
    category: str
    score: float


@dataclass(slots=True)
class ModerationDecision:
    text: str
    provider: str
    flagged: bool
    action: str
    categories: dict[str, float] = field(default_factory=dict)
    redacted_text: str | None = None
    reason: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "provider": self.provider,
            "flagged": self.flagged,
            "action": self.action,
            "categories": dict(self.categories),
            "redacted_text": self.redacted_text,
            "reason": self.reason,
            "raw": self.raw,
        }


@dataclass(slots=True)
class BatchModerationResult:
    decisions: list[ModerationDecision]

    def to_dict(self) -> dict[str, Any]:
        return {"decisions": [decision.to_dict() for decision in self.decisions]}


@dataclass(slots=True)
class ThresholdDecision:
    allow: bool
    triggered_categories: list[str]
    scores: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return {
            "allow": self.allow,
            "triggered_categories": list(self.triggered_categories),
            "scores": dict(self.scores),
        }


def normalize_openai_categories(category_scores: dict[str, Any]) -> dict[str, float]:
    normalized: dict[str, float] = {}
    for key, value in category_scores.items():
        if isinstance(value, (int, float)):
            normalized[key] = float(value)
        elif hasattr(value, "score"):
            normalized[key] = float(value.score)
        else:
            try:
                normalized[key] = float(value)
            except (TypeError, ValueError):
                continue
    return normalized


def summarize_triggered_categories(
    scores: dict[str, float], thresholds: dict[str, float]
) -> list[str]:
    return [
        category
        for category, score in scores.items()
        if score >= thresholds.get(category, 1.0)
    ]
