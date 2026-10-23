from dataclasses import dataclass
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
    if isinstance(messages, list):
        return [normalize_text(item) for item in messages if normalize_text(item)]
    single = normalize_text(messages)
    return [single] if single else []


@dataclass
class SafetyRequest:
    text: str
    categories: Optional[List[str]] = None
    threshold: float = 0.5


@dataclass
class SafetyDecision:
    allowed: bool
    scores: Dict[str, float]
    labels: List[str]
    redacted_text: Optional[str] = None


def build_result(
    allowed: bool,
    scores: Dict[str, float],
    labels: List[str],
    redacted_text: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "allowed": allowed,
        "scores": scores,
        "labels": labels,
        "redacted_text": redacted_text,
    }
