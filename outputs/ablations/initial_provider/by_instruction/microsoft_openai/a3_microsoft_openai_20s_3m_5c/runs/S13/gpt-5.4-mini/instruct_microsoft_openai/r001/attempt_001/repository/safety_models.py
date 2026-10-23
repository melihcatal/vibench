from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_messages(messages: Any) -> List[Dict[str, str]]:
    if not messages:
        return []
    normalized = []
    for item in messages:
        if isinstance(item, dict):
            role = normalize_text(item.get("role", "user")) or "user"
            content = normalize_text(item.get("content", ""))
        else:
            role = "user"
            content = normalize_text(item)
        normalized.append({"role": role, "content": content})
    return normalized


@dataclass
class ModerationRequest:
    text: str
    model: Optional[str] = None


@dataclass
class BatchModerationRequest:
    messages: List[str] = field(default_factory=list)
    model: Optional[str] = None


@dataclass
class ModerationResult:
    allowed: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RedactionResult:
    redacted_text: str
    spans: List[Dict[str, Any]]
    allowed: bool
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThresholdResult:
    allowed: bool
    triggered: List[str]
    raw: Dict[str, Any] = field(default_factory=dict)
