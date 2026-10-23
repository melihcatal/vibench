from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(text: Optional[str]) -> str:
    return "" if text is None else " ".join(str(text).split())


def normalize_texts(texts: Optional[List[str]]) -> List[str]:
    return [normalize_text(text) for text in (texts or [])]


@dataclass
class SafetyDecision:
    allow: bool
    score: float
    categories: Dict[str, float]
    raw: Dict[str, Any]


@dataclass
class SafetyBatchDecision:
    items: List[SafetyDecision]


@dataclass
class SafetyRedaction:
    text: str
    redacted_spans: List[Dict[str, Any]]
    allow: bool
