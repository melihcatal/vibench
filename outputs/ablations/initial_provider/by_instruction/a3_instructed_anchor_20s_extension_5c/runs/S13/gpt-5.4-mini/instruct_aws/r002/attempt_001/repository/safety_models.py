from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_messages(messages: Any) -> List[str]:
    if messages is None:
        return []
    if isinstance(messages, str):
        return [normalize_text(messages)]
    return [normalize_text(item) for item in messages if normalize_text(item)]


@dataclass
class SafetyDecision:
    allow: bool
    categories: Dict[str, float] = field(default_factory=dict)
    flagged_spans: List[Dict[str, Any]] = field(default_factory=list)
    provider: str = "aws"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyBatchResult:
    decisions: List[SafetyDecision]
