import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class TextContent:
    text: str
    content_type: str = "text/plain"


@dataclasses.dataclass
class CategoryDetection:
    category: str
    severity: int


@dataclasses.dataclass
class ModerationResult:
    text: str
    categories_detection: List[CategoryDetection]
    is_unsafe: bool = False


@dataclasses.dataclass
class BatchModerationRequest:
    texts: List[TextContent]


@dataclasses.dataclass
class BatchModerationResult:
    results: List[ModerationResult]


@dataclasses.dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    unsafe_spans: List[
        dict
    ]  # Example: [{"offset": 0, "length": 5, "category": "Hate"}]


@dataclasses.dataclass
class ModerationDecision:
    text: str
    decision: str  # "allow" or "deny"
    reasons: List[str]
