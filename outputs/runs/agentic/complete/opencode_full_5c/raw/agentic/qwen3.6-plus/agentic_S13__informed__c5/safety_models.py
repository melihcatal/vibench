import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CategoryScore:
    category: str
    score: float
    threshold: float = 0.0

    @property
    def is_violating(self) -> bool:
        return self.score >= self.threshold


@dataclass
class ModerationRequest:
    text: str
    languages: list[str] = field(default_factory=lambda: ["en"])
    context: Optional[str] = None


@dataclass
class ModerationResponse:
    text: str
    scores: list[CategoryScore]
    overall_violation: bool
    provider: str = "perspective_api"
    raw_response: Optional[dict] = None

    @property
    def max_score(self) -> float:
        return max((s.score for s in self.scores), default=0.0)

    @property
    def max_category(self) -> Optional[str]:
        if not self.scores:
            return None
        return max(self.scores, key=lambda s: s.score).category

    @property
    def violating_categories(self) -> list[str]:
        return [s.category for s in self.scores if s.is_violating]


@dataclass
class BatchModerationRequest:
    messages: list[ModerationRequest]
    default_thresholds: Optional[dict[str, float]] = None


@dataclass
class BatchModerationResponse:
    results: list[ModerationResponse]
    provider: str = "perspective_api"

    @property
    def total_messages(self) -> int:
        return len(self.results)

    @property
    def flagged_count(self) -> int:
        return sum(1 for r in self.results if r.overall_violation)

    @property
    def clean_count(self) -> int:
        return self.total_messages - self.flagged_count


@dataclass
class UnsafeSpan:
    text: str
    start: int
    end: int
    category: str
    score: float


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    unsafe_spans: list[UnsafeSpan]
    provider: str = "perspective_api"


@dataclass
class ThresholdConfig:
    categories: dict[str, float] = field(default_factory=dict)
    default_threshold: float = 0.7
    action_on_violation: str = "block"

    def get_threshold(self, category: str) -> float:
        return self.categories.get(category, self.default_threshold)


@dataclass
class ThresholdResult:
    text: str
    allowed: bool
    category_decisions: list[CategoryScore]
    provider: str = "perspective_api"
