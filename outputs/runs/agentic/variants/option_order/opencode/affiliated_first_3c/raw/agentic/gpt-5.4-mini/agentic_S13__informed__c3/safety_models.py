from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class ModerationRequest:
    text: str


@dataclass
class ModerationDecision:
    flagged: bool
    categories: Dict[str, Any]
    raw: Dict[str, Any]


@dataclass
class BatchModerationRequest:
    messages: List[str]


@dataclass
class RedactionSpan:
    start: int
    end: int
    category: str


@dataclass
class ThresholdRule:
    category: str
    threshold: float


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_messages(messages: Iterable[str]) -> List[str]:
    return [normalize_text(m) for m in messages]


def parse_decision(payload: Mapping[str, Any]) -> ModerationDecision:
    return ModerationDecision(flagged=bool(payload.get("flagged", False)), categories=dict(payload.get("categories", {})), raw=dict(payload))
