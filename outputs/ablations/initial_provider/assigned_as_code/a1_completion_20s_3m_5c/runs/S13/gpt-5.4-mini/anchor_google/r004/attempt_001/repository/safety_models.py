from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_thresholds(thresholds: Optional[Dict[str, Any]]) -> Dict[str, float]:
    thresholds = thresholds or {}
    return {str(k): float(v) for k, v in thresholds.items()}


def normalize_messages(messages: Any) -> List[Dict[str, str]]:
    if not messages:
        return []
    normalized = []
    for item in messages:
        if isinstance(item, dict):
            normalized.append({"id": normalize_text(item.get("id")), "text": normalize_text(item.get("text"))})
        else:
            normalized.append({"id": "", "text": normalize_text(item)})
    return normalized


@dataclass
class SafetyDecision:
    allow: bool
    score: float
    category: str = "TOXICITY"
