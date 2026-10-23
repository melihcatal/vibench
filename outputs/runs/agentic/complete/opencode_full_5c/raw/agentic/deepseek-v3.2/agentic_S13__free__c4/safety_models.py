from typing import Dict, Any, List, Optional, TypedDict
from dataclasses import dataclass
from enum import Enum


class SafetyCategory(str, Enum):
    """Safety categories for content moderation."""

    HATE = "hate"
    HATE_THREATENING = "hate_threatening"
    HARASSMENT = "harassment"
    HARASSMENT_THREATENING = "harassment_threatening"
    SELF_HARM = "self_harm"
    SELF_HARM_INTENT = "self_harm_intent"
    SELF_HARM_INSTRUCTIONS = "self_harm_instructions"
    SEXUAL = "sexual"
    SEXUAL_MINORS = "sexual_minors"
    VIOLENCE = "violence"
    VIOLENCE_GRAPHIC = "violence_graphic"


@dataclass
class ModerationRequest:
    """Request model for text moderation."""

    text: str
    model: str = "text-moderation-latest"
    categories: Optional[List[SafetyCategory]] = None

    def to_openai_dict(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        return {"input": self.text, "model": self.model}


@dataclass
class ModerationResult:
    """Result model for text moderation."""

    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    text: str

    @classmethod
    def from_openai_response(cls, response: Any, text: str) -> "ModerationResult":
        """Create from OpenAI moderation response."""
        result = response.results[0]

        categories = {
            "hate": result.categories.hate,
            "hate_threatening": result.categories.hate_threatening,
            "harassment": result.categories.harassment,
            "harassment_threatening": result.categories.harassment_threatening,
            "self_harm": result.categories.self_harm,
            "self_harm_intent": result.categories.self_harm_intent,
            "self_harm_instructions": result.categories.self_harm_instructions,
            "sexual": result.categories.sexual,
            "sexual_minors": result.categories.sexual_minors,
            "violence": result.categories.violence,
            "violence_graphic": result.categories.violence_graphic,
        }

        category_scores = {
            "hate": result.category_scores.hate,
            "hate_threatening": result.category_scores.hate_threatening,
            "harassment": result.category_scores.harassment,
            "harassment_threatening": result.category_scores.harassment_threatening,
            "self_harm": result.category_scores.self_harm,
            "self_harm_intent": result.category_scores.self_harm_intent,
            "self_harm_instructions": result.category_scores.self_harm_instructions,
            "sexual": result.category_scores.sexual,
            "sexual_minors": result.category_scores.sexual_minors,
            "violence": result.category_scores.violence,
            "violence_graphic": result.category_scores.violence_graphic,
        }

        return cls(
            flagged=result.flagged,
            categories=categories,
            category_scores=category_scores,
            text=text,
        )


@dataclass
class RedactionSpan:
    """Span of text to be redacted."""

    text: str
    start: int
    end: int
    category: str
    confidence: float = 1.0


@dataclass
class RedactionResult:
    """Result model for text redaction."""

    original_text: str
    redacted_text: str
    flagged: bool
    flagged_spans: List[RedactionSpan]
    category_flags: Dict[str, bool]


@dataclass
class ThresholdDecision:
    """Decision based on category thresholds."""

    category: str
    score: float
    threshold: float
    allowed: bool


@dataclass
class ThresholdResult:
    """Result model for threshold-based decisions."""

    text: str
    overall_decision: str
    allow: bool
    decisions: Dict[str, ThresholdDecision]
    violating_categories: List[str]
    max_violation_score: float


class BatchModerationRequest(TypedDict):
    """Batch moderation request type."""

    texts: List[str]
    model: str


class BatchModerationResult(TypedDict):
    """Batch moderation result type."""

    results: List[ModerationResult]
    batch_id: Optional[str]


def normalize_category_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """Normalize category scores to 0-1 range."""
    normalized = {}
    for category, score in scores.items():
        normalized[category] = min(max(score, 0.0), 1.0)
    return normalized


def get_primary_violation(categories: Dict[str, bool]) -> Optional[str]:
    """Get the primary violation category from flagged categories."""
    priority_order = [
        "violence_graphic",
        "violence",
        "sexual_minors",
        "sexual",
        "hate_threatening",
        "hate",
        "harassment_threatening",
        "harassment",
        "self_harm_instructions",
        "self_harm_intent",
        "self_harm",
    ]

    for category in priority_order:
        if categories.get(category):
            return category
    return None
