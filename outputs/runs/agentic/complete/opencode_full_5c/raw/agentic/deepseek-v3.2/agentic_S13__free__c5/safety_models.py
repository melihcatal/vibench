from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class SafetyCategory(str, Enum):
    """Enumeration of safety categories."""

    HARASSMENT = "harassment"
    HATE = "hate"
    SELF_HARM = "self-harm"
    SEXUAL = "sexual"
    VIOLENCE = "violence"
    HARASSMENT_THREATENING = "harassment/threatening"
    HATE_THREATENING = "hate/threatening"
    SELF_HARM_INTENT = "self-harm/intent"
    SELF_HARM_INSTRUCTIONS = "self-harm/instructions"
    SEXUAL_MINORS = "sexual/minors"
    VIOLENCE_GRAPHIC = "violence/graphic"


@dataclass
class ModerationRequest:
    """Request model for moderation operations."""

    text: str
    model: str = "text-moderation-latest"
    categories: Optional[List[SafetyCategory]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        result = {"input": self.text, "model": self.model}
        return result


@dataclass
class ModerationResult:
    """Result model for moderation operations."""

    text: str
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]

    @classmethod
    def from_openai_response(cls, text: str, response) -> "ModerationResult":
        """Create from OpenAI moderation response."""
        result = response.results[0]
        return cls(
            text=text,
            flagged=result.flagged,
            categories=result.categories.model_dump(),
            category_scores=result.category_scores.model_dump(),
        )

    def get_flagged_categories(self) -> List[str]:
        """Get list of flagged category names."""
        return [cat for cat, flagged in self.categories.items() if flagged]


@dataclass
class BatchModerationRequest:
    """Request model for batch moderation operations."""

    texts: List[str]
    model: str = "text-moderation-latest"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        return {"input": self.texts, "model": self.model}


@dataclass
class BatchModerationResult:
    """Result model for batch moderation operations."""

    results: List[ModerationResult]

    @classmethod
    def from_openai_response(
        cls, texts: List[str], response
    ) -> "BatchModerationResult":
        """Create from OpenAI batch moderation response."""
        results = []
        for i, result in enumerate(response.results):
            results.append(
                ModerationResult(
                    text=texts[i],
                    flagged=result.flagged,
                    categories=result.categories.model_dump(),
                    category_scores=result.category_scores.model_dump(),
                )
            )
        return cls(results=results)


@dataclass
class RedactionResult:
    """Result model for text redaction operations."""

    original_text: str
    redacted_text: str
    flagged: bool
    flagged_categories: List[str]
    redacted_spans: List[Dict[str, Any]]
    category_scores: Dict[str, float]


@dataclass
class ThresholdDecision:
    """Decision model for threshold-based moderation."""

    category: str
    score: float
    threshold: float
    flagged: bool


@dataclass
class ThresholdResult:
    """Result model for threshold-based moderation."""

    text: str
    allow: bool
    decisions: Dict[str, ThresholdDecision]
    overall_flagged: bool
