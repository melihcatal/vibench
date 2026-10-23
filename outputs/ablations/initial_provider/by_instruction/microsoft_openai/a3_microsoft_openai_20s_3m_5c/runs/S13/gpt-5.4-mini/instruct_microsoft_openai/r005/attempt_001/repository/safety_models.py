from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


@dataclass
class ModerationRequest:
    text: str


@dataclass
class BatchModerationRequest:
    texts: List[str]


@dataclass
class ModerationDecision:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    provider: str = "openai"
    raw: Optional[Dict[str, Any]] = None


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str


@dataclass
class RedactionResult:
    text: str
    spans: List[RedactionSpan]
