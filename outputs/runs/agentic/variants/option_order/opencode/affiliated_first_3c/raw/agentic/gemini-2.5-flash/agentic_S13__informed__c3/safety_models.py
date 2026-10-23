import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class ModerationResult:
    category: str
    severity: int
    detected: bool


@dataclasses.dataclass
class TextModerationResponse:
    text: str
    results: List[ModerationResult]


@dataclasses.dataclass
class RedactionResult:
    category: str
    severity: int
    detected: bool


@dataclasses.dataclass
class RedactionResponse:
    text: str
    redacted_text: str
    redaction_details: List[RedactionResult]


@dataclasses.dataclass
class ModerationDecision:
    text: str
    is_safe: bool
    reasons: List[str]
