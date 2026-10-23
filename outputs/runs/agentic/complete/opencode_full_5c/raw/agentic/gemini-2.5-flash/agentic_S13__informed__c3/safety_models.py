import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class TextModerationRequest:
    text: str


@dataclasses.dataclass
class TextModerationResult:
    category: str
    severity: int


@dataclasses.dataclass
class TextModerationResponse:
    is_safe: bool
    results: List[TextModerationResult]
    original_text: str


@dataclasses.dataclass
class BatchModerationRequest:
    texts: List[str]


@dataclasses.dataclass
class BatchModerationResponse:
    per_message_decisions: List[TextModerationResponse]


@dataclasses.dataclass
class RedactionRequest:
    text: str
    thresholds: Optional[dict] = None  # Category-severity pairs for redaction


@dataclasses.dataclass
class RedactionResponse:
    redacted_text: str
    flagged_spans: List[dict]  # { "category": "hate", "offset": 0, "length": 4 }


@dataclasses.dataclass
class ThresholdDecisionRequest:
    text_moderation_response: TextModerationResponse
    thresholds: dict  # { "Hate": 2, "Sexual": 2, ... }


@dataclasses.dataclass
class ThresholdDecisionResponse:
    allow_text: bool
    reasons: List[str]
