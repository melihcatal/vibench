from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyCategory(Enum):
    HATE = "hate"
    HATE_THREATENING = "hate/threatening"
    HARASSMENT = "harassment"
    HARASSMENT_THREATENING = "harassment/threatening"
    SELF_HARM = "self-harm"
    SELF_HARM_INTENT = "self-harm/intent"
    SELF_HARM_INSTRUCTIONS = "self-harm/instructions"
    SEXUAL = "sexual"
    SEXUAL_MINORS = "sexual/minors"
    VIOLENCE = "violence"
    VIOLENCE_GRAPHIC = "violence/graphic"


@dataclass
class ModerationRequest:
    """Request model for text moderation."""

    text: str
    categories: Optional[List[SafetyCategory]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "categories": [cat.value for cat in self.categories]
            if self.categories
            else None,
        }


@dataclass
class ModerationResult:
    """Result model for text moderation."""

    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]

    @classmethod
    def from_openai(cls, openai_result) -> "ModerationResult":
        """Create ModerationResult from OpenAI moderation response."""
        return cls(
            flagged=openai_result.flagged,
            categories={
                "hate": openai_result.categories.hate,
                "hate/threatening": openai_result.categories.hate_threatening,
                "harassment": openai_result.categories.harassment,
                "harassment/threatening": openai_result.categories.harassment_threatening,
                "self-harm": openai_result.categories.self_harm,
                "self-harm/intent": openai_result.categories.self_harm_intent,
                "self-harm/instructions": openai_result.categories.self_harm_instructions,
                "sexual": openai_result.categories.sexual,
                "sexual/minors": openai_result.categories.sexual_minors,
                "violence": openai_result.categories.violence,
                "violence/graphic": openai_result.categories.violence_graphic,
            },
            category_scores={
                "hate": openai_result.category_scores.hate,
                "hate/threatening": openai_result.category_scores.hate_threatening,
                "harassment": openai_result.category_scores.harassment,
                "harassment/threatening": openai_result.category_scores.harassment_threatening,
                "self-harm": openai_result.category_scores.self_harm,
                "self-harm/intent": openai_result.category_scores.self_harm_intent,
                "self-harm/instructions": openai_result.category_scores.self_harm_instructions,
                "sexual": openai_result.category_scores.sexual,
                "sexual/minors": openai_result.category_scores.sexual_minors,
                "violence": openai_result.category_scores.violence,
                "violence/graphic": openai_result.category_scores.violence_graphic,
            },
        )


@dataclass
class RedactionResult:
    """Result model for text redaction."""

    redacted_text: str
    flagged_spans: List[Dict[str, Any]]
    flagged_categories: List[str]
    was_flagged: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "redacted_text": self.redacted_text,
            "flagged_spans": self.flagged_spans,
            "flagged_categories": self.flagged_categories,
            "was_flagged": self.was_flagged,
        }


@dataclass
class ThresholdResult:
    """Result model for threshold-based moderation."""

    allow: bool
    exceeded_thresholds: Dict[str, Dict[str, float]]
    category_scores: Dict[str, float]
    thresholds_applied: Dict[str, float]
    flagged: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allow": self.allow,
            "exceeded_thresholds": self.exceeded_thresholds,
            "category_scores": self.category_scores,
            "thresholds_applied": self.thresholds_applied,
            "flagged": self.flagged,
        }


def normalize_text(text: str) -> str:
    """Normalize text for moderation."""
    return text.strip()


def parse_category_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """Parse and validate category scores."""
    normalized = {}
    for category, score in scores.items():
        if not 0 <= score <= 1:
            raise ValueError(
                f"Score for {category} must be between 0 and 1, got {score}"
            )
        normalized[category] = round(score, 4)
    return normalized
