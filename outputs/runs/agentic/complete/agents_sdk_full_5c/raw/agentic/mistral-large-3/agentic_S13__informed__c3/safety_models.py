from typing import List, Dict, Optional, TypedDict
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "hate"
    SEXUAL = "sexual"
    VIOLENCE = "violence"
    HARASSMENT = "harassment"
    SELF_HARM = "self_harm"
    DANGEROUS = "dangerous"


class SafetyScore(TypedDict):
    category: SafetyCategory
    score: float
    flagged: bool


class TextModerationResponse:
    """Normalized response for text moderation."""

    def __init__(
        self,
        raw_response: dict,
        scores: List[SafetyScore],
        flagged: bool,
        flagged_categories: List[SafetyCategory]
    ):
        self.raw_response = raw_response
        self.scores = scores
        self.flagged = flagged
        self.flagged_categories = flagged_categories

    @classmethod
    def from_watsonx(cls, raw_response: dict) -> "TextModerationResponse":
        """Normalize WatsonX guardrails response."""
        # Example normalization logic (adjust based on actual response structure)
        scores = []
        flagged_categories = []
        flagged = False

        if "results" in raw_response:
            for category in SafetyCategory:
                score = raw_response["results"].get(category.value, 0.0)
                is_flagged = score > 0.5
                scores.append({
                    "category": category,
                    "score": score,
                    "flagged": is_flagged
                })
                if is_flagged:
                    flagged_categories.append(category)
                    flagged = True

        return cls(
            raw_response=raw_response,
            scores=scores,
            flagged=flagged,
            flagged_categories=flagged_categories
        )


class RedactionSpan(TypedDict):
    start: int
    end: int
    category: SafetyCategory
    replacement: Optional[str]


class TextRedactionResponse:
    """Normalized response for text redaction."""

    def __init__(
        self,
        raw_response: dict,
        redacted_text: str,
        spans: List[RedactionSpan]
    ):
        self.raw_response = raw_response
        self.redacted_text = redacted_text
        self.spans = spans