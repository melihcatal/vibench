"""
safety_models.py - Local request, response, and normalization helpers for Text Content Safety.

Provides data models and normalization utilities for working with
OpenAI Moderation API responses.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional
from datetime import datetime


SAFETY_CATEGORIES = [
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]

HIGH_SEVERITY_CATEGORIES = {
    "hate/threatening",
    "harassment/threatening",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual/minors",
    "violence/graphic",
}


@dataclass
class ModerationRequest:
    """Request model for text moderation."""
    text: str
    model: str = "text-moderation-latest"
    threshold: float = 0.5
    categories: Optional[list] = None
    strict_mode: bool = False
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_api_payload(self) -> dict:
        """Convert to OpenAI API request payload."""
        return {
            "input": self.text,
            "model": self.model,
        }


@dataclass
class CategoryScore:
    """Individual category score with threshold comparison."""
    category: str
    score: float
    threshold: float
    exceeded: bool = field(init=False)

    def __post_init__(self):
        self.exceeded = self.score >= self.threshold


@dataclass
class ModerationResponse:
    """Normalized response from moderation API."""
    flagged: bool
    category_scores: dict[str, float]
    flagged_categories: list[str]
    model: str
    provider: str = "openai"
    provider_endpoint: str = "api.openai.com/v1/moderations"
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    request_id: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert response to dictionary."""
        return asdict(self)


@dataclass
class BatchModerationResponse:
    """Normalized response for batch moderation."""
    results: list[ModerationResponse]
    total_count: int
    flagged_count: int
    safe_count: int
    provider: str = "openai"

    def to_dict(self) -> dict:
        """Convert batch response to dictionary."""
        return {
            "results": [r.to_dict() for r in self.results],
            "total_count": self.total_count,
            "flagged_count": self.flagged_count,
            "safe_count": self.safe_count,
            "provider": self.provider,
        }


@dataclass
class RedactionResult:
    """Result from text redaction operation."""
    original_text: str
    redacted_text: str
    flagged_spans: list[dict]
    redaction_count: int
    model: str
    provider: str = "openai"

    def to_dict(self) -> dict:
        """Convert redaction result to dictionary."""
        return asdict(self)


@dataclass
class ThresholdDecision:
    """Decision result from threshold-based evaluation."""
    allowed: bool
    decision: str
    category_scores: dict[str, float]
    exceeded_thresholds: list[str]
    high_severity_exceeded: list[str]
    strict_mode: bool
    model: str
    provider: str = "openai"

    def to_dict(self) -> dict:
        """Convert decision to dictionary."""
        return asdict(self)


def normalize_openai_response(raw_response, model: str = "text-moderation-latest") -> ModerationResponse:
    """
    Normalize raw OpenAI moderation API response to internal format.

    Args:
        raw_response: Raw response from client.moderations.create()
        model: Model identifier used in the request.

    Returns:
        Normalized ModerationResponse instance.
    """
    result = raw_response.results[0]

    category_scores = {}
    flagged_categories = []

    for category in SAFETY_CATEGORIES:
        score = getattr(result.category_scores, category, 0.0)
        category_scores[category] = score
        if score >= 0.5:
            flagged_categories.append(category)

    return ModerationResponse(
        flagged=result.flagged,
        category_scores=category_scores,
        flagged_categories=flagged_categories,
        model=model,
        provider="openai",
        provider_endpoint="api.openai.com/v1/moderations",
        request_id=getattr(raw_response, "id", None),
    )


def normalize_batch_response(raw_response, model: str = "text-moderation-latest") -> BatchModerationResponse:
    """
    Normalize raw OpenAI batch moderation response to internal format.

    Args:
        raw_response: Raw response from client.moderations.create() with multiple inputs.
        model: Model identifier used in the request.

    Returns:
        Normalized BatchModerationResponse instance.
    """
    results = []
    flagged_count = 0

    for mod_result in raw_response.results:
        category_scores = {}
        flagged_categories = []

        for category in SAFETY_CATEGORIES:
            score = getattr(mod_result.category_scores, category, 0.0)
            category_scores[category] = score
            if score >= 0.5:
                flagged_categories.append(category)

        normalized = ModerationResponse(
            flagged=mod_result.flagged,
            category_scores=category_scores,
            flagged_categories=flagged_categories,
            model=model,
            provider="openai",
        )
        results.append(normalized)
        if mod_result.flagged:
            flagged_count += 1

    return BatchModerationResponse(
        results=results,
        total_count=len(results),
        flagged_count=flagged_count,
        safe_count=len(results) - flagged_count,
        provider="openai",
    )


def get_category_severity_level(category: str) -> str:
    """
    Get the severity level for a moderation category.

    Args:
        category: The moderation category name.

    Returns:
        'high', 'medium', or 'low' severity level.
    """
    if category in HIGH_SEVERITY_CATEGORIES:
        return "high"

    base_category = category.split("/")[0]
    if base_category in ("self-harm", "sexual", "hate", "violence"):
        return "medium"

    return "low"


def filter_categories_by_severity(
    category_scores: dict[str, float],
    min_severity: str = "medium",
) -> dict[str, float]:
    """
    Filter category scores by minimum severity level.

    Args:
        category_scores: Dict of category -> score.
        min_severity: Minimum severity level to include ('low', 'medium', 'high').

    Returns:
        Filtered category scores dict.
    """
    severity_order = {"low": 0, "medium": 1, "high": 2}
    min_level = severity_order.get(min_severity, 0)

    return {
        cat: score
        for cat, score in category_scores.items()
        if severity_order.get(get_category_severity_level(cat), 0) >= min_level
    }
