from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


def normalize_text(text: Optional[str]) -> str:
    return (text or "").strip()


def normalize_texts(texts: Optional[List[str]]) -> List[str]:
    return [normalize_text(t) for t in (texts or [])]


@dataclass
class SafetyRequest:
    text: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BatchSafetyRequest:
    texts: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SafetyDecision:
    allowed: bool
    categories: Dict[str, float]
    flagged_spans: List[Dict[str, Any]]
    raw: Dict[str, Any]


@dataclass
class BatchSafetyDecision:
    decisions: List[SafetyDecision]


@dataclass
class SafetyThresholdConfig:
    thresholds: Dict[str, float]
