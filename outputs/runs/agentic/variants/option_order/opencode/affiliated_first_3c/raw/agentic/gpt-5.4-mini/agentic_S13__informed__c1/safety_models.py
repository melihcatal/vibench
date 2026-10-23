from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SafetyTextRequest:
    text: str
    language: Optional[str] = None
    categories: Optional[List[str]] = None


@dataclass
class SafetyBatchRequest:
    texts: List[str]
    language: Optional[str] = None


@dataclass
class SafetyDecision:
    allowed: bool
    score: float
    categories: Dict[str, float]
    raw: Dict[str, Any]


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def normalize_scores(payload: Any) -> Dict[str, float]:
    if isinstance(payload, dict):
        return {str(k): float(v) for k, v in payload.items() if v is not None}
    return {}
