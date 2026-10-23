from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ModerationRequest:
    text: str
    language_code: Optional[str] = "en"


@dataclass
class ModerationResultCategory:
    category: str
    severity: int


@dataclass
class ModerationResult:
    blocked: bool
    categories: List[ModerationResultCategory] = field(default_factory=list)
    raw_response: Optional[dict] = None


@dataclass
class RedactionResult:
    redacted_text: str
    blocked: bool
    categories: List[ModerationResultCategory] = field(default_factory=list)
    raw_response: Optional[dict] = None


@dataclass
class BatchModerationRequest:
    texts: List[str]
    language_code: Optional[str] = "en"


@dataclass
class BatchModerationResultItem:
    original_text: str
    moderation_result: ModerationResult


@dataclass
class BatchModerationResult:
    results: List[BatchModerationResultItem] = field(default_factory=list)
