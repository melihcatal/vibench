"""
Local helper: safety_models.py
Defines local request, response, and normalization helpers for Text Content Safety.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "hate"
    SELF_HARM = "self_harm"
    SEXUAL = "sexual"
    VIOLENCE = "violence"
    HARASSMENT = "harassment"
    SEXUAL_MINORS = "sexual_minors"
    HATE_THREATENING = "hate_threatening"
    SELF_HARM_INTENT = "self_harm_intent"
    SELF_HARM_INSTRUCTIONS = "self_harm_instructions"
    VIOLENCE_GRAPHIC = "violence_graphic"


class ModerationDecision(str, Enum):
    ALLOW = "allow"
    FLAG = "flag"
    BLOCK = "block"
    REVIEW = "review"


@dataclass
class CategoryScore:
    """Normalized per-category score with category name and float value."""
    category: str
    score: float

    def to_dict(self) -> Dict[str, Any]:
        return {"category": self.category, "score": self.score}


@dataclass
class ModerationResult:
    """Single-text moderation response."""
    text: str
    flagged: bool
    decision: str
    categories: List[CategoryScore]
    highest_category: Optional[str] = None
    highest_score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "flagged": self.flagged,
            "decision": self.decision,
            "categories": [c.to_dict() for c in self.categories],
            "highest_category": self.highest_category,
            "highest_score": self.highest_score,
            "metadata": self.metadata,
        }


@dataclass
class BatchModerationResult:
    """Batch moderation response containing per-message results."""
    results: List[ModerationResult]
    total_processed: int = 0
    total_flagged: int = 0
    total_blocked: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": [r.to_dict() for r in self.results],
            "total_processed": self.total_processed,
            "total_flagged": self.total_flagged,
            "total_blocked": self.total_blocked,
        }


@dataclass
class RedactedText:
    """Result of redacting unsafe spans."""
    original_text: str
    redacted_text: str
    flagged_spans: List[Dict[str, Any]]
    categories_redacted: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_text": self.original_text,
            "redacted_text": self.redacted_text,
            "flagged_spans": self.flagged_spans,
            "categories_redacted": self.categories_redacted,
        }


@dataclass
class ModerationSummary:
    """Summary of moderation decisions over a set of texts."""
    total_texts: int
    allowed: int
    flagged: int
    blocked: int
    under_review: int
    category_counts: Dict[str, int]
    average_scores: Dict[str, float]
    top_risk_text: Optional[str] = None
    top_risk_category: Optional[str] = None
    top_risk_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ModerationAppeal:
    """Translated appeal text for review."""
    appeal_id: str
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    translation_confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ModerationEmbedding:
    """Embedded moderation rationale."""
    rationale_text: str
    embedding: List[float]
    model: str
    dimension: int = 0

    def __post_init__(self):
        if not self.dimension and self.embedding:
            self.dimension = len(self.embedding)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReviewerAudioBrief:
    """Spoken brief for moderation reviewer."""
    case_summary: str
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    voice_id: str = ""
    duration_seconds: Optional[float] = None
    format: str = "mp3"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_openai_moderation_response(
    text: str, response: Any
) -> ModerationResult:
    """Normalize an OpenAI moderation API response to a ModerationResult."""
    results = response.results[0]
    categories = []
    highest_category = None
    highest_score = 0.0

    category_scores = results.category_scores
    for cat_name in dir(category_scores):
        if not cat_name.startswith("_"):
            score = getattr(category_scores, cat_name, 0.0)
            if score is not None:
                cat = CategoryScore(category=cat_name, score=float(score))
                categories.append(cat)
                if float(score) > highest_score:
                    highest_score = float(score)
                    highest_category = cat_name

    return ModerationResult(
        text=text,
        flagged=bool(results.flagged),
        decision=ModerationDecision.BLOCK if results.flagged else ModerationDecision.ALLOW,
        categories=categories,
        highest_category=highest_category,
        highest_score=highest_score,
    )


def normalize_perspective_category_scores(
    attribute_scores: Dict[str, float],
) -> List[CategoryScore]:
    """Normalize Google Perspective API attribute scores to CategoryScore list."""
    mapping = {
        "TOXICITY": SafetyCategory.HATE,
        "SEVERE_TOXICITY": SafetyCategory.HATE_THREATENING,
        "IDENTITY_ATTACK": SafetyCategory.HARASSMENT,
        "INSULT": SafetyCategory.HARASSMENT,
        "PROFANITY": SafetyCategory.HATE,
        "THREAT": SafetyCategory.VIOLENCE,
        "SEXUALLY_EXPLICIT": SafetyCategory.SEXUAL,
        "FLIRTATION": SafetyCategory.SEXUAL,
    }
    categories = []
    for attr_name, score in attribute_scores.items():
        mapped_cat = mapping.get(attr_name, attr_name.lower())
        categories.append(CategoryScore(category=str(mapped_cat), score=float(score)))
    return categories


def build_perspective_request_payload(
    text: str,
    languages: Optional[List[str]] = None,
    requested_attributes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a request payload for the Google Comment Analyzer / Perspective API."""
    if requested_attributes is None:
        requested_attributes = [
            "TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK",
            "INSULT", "PROFANITY", "THREAT", "SEXUALLY_EXPLICIT", "FLIRTATION",
        ]
    return {
        "comment": {"text": text},
        "languages": languages or ["en"],
        "requestedAttributes": {attr: {} for attr in requested_attributes},
    }
