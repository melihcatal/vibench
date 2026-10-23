from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_categories(value: Any) -> Dict[str, float]:
    if not isinstance(value, dict):
        return {}
    output: Dict[str, float] = {}
    for key, score in value.items():
        try:
            output[str(key)] = float(score)
        except (TypeError, ValueError):
            continue
    return output


@dataclass
class SafetyRequest:
    text: str
    categories: List[str] = field(default_factory=list)


@dataclass
class SafetyDecision:
    allow: bool
    scores: Dict[str, float] = field(default_factory=dict)
    reason: Optional[str] = None


@dataclass
class BatchSafetyDecision:
    results: List[SafetyDecision] = field(default_factory=list)


@dataclass
class RedactionResult:
    text: str
    spans: List[Dict[str, Any]] = field(default_factory=list)
