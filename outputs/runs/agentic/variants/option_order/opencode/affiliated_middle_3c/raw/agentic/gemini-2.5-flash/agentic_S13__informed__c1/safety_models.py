import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class TextModerationRequest:
    text: str


@dataclasses.dataclass
class TextModerationResponse:
    categories: dict
    category_scores: dict
    suggested_action: str
    analyze_result: dict


@dataclasses.dataclass
class TextRedactionResponse:
    redacted_text: str
    analyze_result: dict


@dataclasses.dataclass
class BatchModerationRequest:
    texts: List[str]


@dataclasses.dataclass
class BatchModerationResponse:
    results: List[TextModerationResponse]


@dataclasses.dataclass
class ModerationDecision:
    text: str
    is_safe: bool
    reasons: List[str]
    category_scores: dict
