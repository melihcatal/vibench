from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyCategory(Enum):
    """Enumeration of safety categories."""

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
    return_scores: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        result = {"text": self.text}
        if self.categories:
            result["categories"] = [cat.value for cat in self.categories]
        return result


@dataclass
class ModerationResult:
    """Result model for text moderation."""

    text: str
    flagged: bool
    category_flags: Dict[SafetyCategory, bool]
    category_scores: Dict[SafetyCategory, float]

    @classmethod
    def from_openai_response(cls, text: str, openai_result: Any) -> "ModerationResult":
        """Create ModerationResult from OpenAI API response."""
        category_flags = {
            SafetyCategory.HATE: openai_result.categories.hate,
            SafetyCategory.HATE_THREATENING: openai_result.categories.hate_threatening,
            SafetyCategory.HARASSMENT: openai_result.categories.harassment,
            SafetyCategory.HARASSMENT_THREATENING: openai_result.categories.harassment_threatening,
            SafetyCategory.SELF_HARM: openai_result.categories.self_harm,
            SafetyCategory.SELF_HARM_INTENT: openai_result.categories.self_harm_intent,
            SafetyCategory.SELF_HARM_INSTRUCTIONS: openai_result.categories.self_harm_instructions,
            SafetyCategory.SEXUAL: openai_result.categories.sexual,
            SafetyCategory.SEXUAL_MINORS: openai_result.categories.sexual_minors,
            SafetyCategory.VIOLENCE: openai_result.categories.violence,
            SafetyCategory.VIOLENCE_GRAPHIC: openai_result.categories.violence_graphic,
        }

        category_scores = {
            SafetyCategory.HATE: openai_result.category_scores.hate,
            SafetyCategory.HATE_THREATENING: openai_result.category_scores.hate_threatening,
            SafetyCategory.HARASSMENT: openai_result.category_scores.harassment,
            SafetyCategory.HARASSMENT_THREATENING: openai_result.category_scores.harassment_threatening,
            SafetyCategory.SELF_HARM: openai_result.category_scores.self_harm,
            SafetyCategory.SELF_HARM_INTENT: openai_result.category_scores.self_harm_intent,
            SafetyCategory.SELF_HARM_INSTRUCTIONS: openai_result.category_scores.self_harm_instructions,
            SafetyCategory.SEXUAL: openai_result.category_scores.sexual,
            SafetyCategory.SEXUAL_MINORS: openai_result.category_scores.sexual_minors,
            SafetyCategory.VIOLENCE: openai_result.category_scores.violence,
            SafetyCategory.VIOLENCE_GRAPHIC: openai_result.category_scores.violence_graphic,
        }

        return cls(
            text=text,
            flagged=openai_result.flagged,
            category_flags=category_flags,
            category_scores=category_scores,
        )


@dataclass
class UnsafeSpan:
    """Model for unsafe text span."""

    text: str
    start_index: int
    end_index: int
    category: SafetyCategory
    score: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "text": self.text,
            "start_index": self.start_index,
            "end_index": self.end_index,
            "category": self.category.value,
            "score": self.score,
        }


@dataclass
class RedactionResult:
    """Result model for text redaction."""

    original_text: str
    redacted_text: str
    unsafe_spans: List[UnsafeSpan]
    moderation_result: ModerationResult

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "original_text": self.original_text,
            "redacted_text": self.redacted_text,
            "unsafe_spans": [span.to_dict() for span in self.unsafe_spans],
            "moderation_result": {
                "flagged": self.moderation_result.flagged,
                "category_flags": {
                    k.value: v for k, v in self.moderation_result.category_flags.items()
                },
                "category_scores": {
                    k.value: v
                    for k, v in self.moderation_result.category_scores.items()
                },
            },
        }


@dataclass
class ThresholdDecision:
    """Decision model based on safety thresholds."""

    allowed: bool
    text: str
    violations: Dict[SafetyCategory, Dict[str, Any]]
    category_scores: Dict[SafetyCategory, float]
    thresholds_applied: Dict[SafetyCategory, float]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "allowed": self.allowed,
            "text": self.text,
            "violations": {k.value: v for k, v in self.violations.items()},
            "category_scores": {k.value: v for k, v in self.category_scores.items()},
            "thresholds_applied": {
                k.value: v for k, v in self.thresholds_applied.items()
            },
        }


def normalize_category_name(category: str) -> SafetyCategory:
    """Normalize category name string to SafetyCategory enum."""
    category_map = {
        "hate": SafetyCategory.HATE,
        "hate/threatening": SafetyCategory.HATE_THREATENING,
        "harassment": SafetyCategory.HARASSMENT,
        "harassment/threatening": SafetyCategory.HARASSMENT_THREATENING,
        "self-harm": SafetyCategory.SELF_HARM,
        "self-harm/intent": SafetyCategory.SELF_HARM_INTENT,
        "self-harm/instructions": SafetyCategory.SELF_HARM_INSTRUCTIONS,
        "sexual": SafetyCategory.SEXUAL,
        "sexual/minors": SafetyCategory.SEXUAL_MINORS,
        "violence": SafetyCategory.VIOLENCE,
        "violence/graphic": SafetyCategory.VIOLENCE_GRAPHIC,
    }

    if category not in category_map:
        raise ValueError(f"Unknown category: {category}")

    return category_map[category]
