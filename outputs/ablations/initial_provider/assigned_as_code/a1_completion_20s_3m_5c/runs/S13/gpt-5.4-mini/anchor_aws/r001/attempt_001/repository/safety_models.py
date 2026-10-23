from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_texts(payload: Any) -> List[str]:
    if payload is None:
        return []
    if isinstance(payload, list):
        return [normalize_text(item) for item in payload]
    if isinstance(payload, dict):
        if "texts" in payload and isinstance(payload["texts"], list):
            return [normalize_text(item) for item in payload["texts"]]
        if "messages" in payload and isinstance(payload["messages"], list):
            return [normalize_text(item) for item in payload["messages"]]
        if "text" in payload:
            return [normalize_text(payload["text"])]
    return [normalize_text(payload)]


def normalize_thresholds(value: Any) -> Dict[str, float]:
    if not isinstance(value, dict):
        return {}
    result: Dict[str, float] = {}
    for key, item in value.items():
        try:
            result[str(key)] = float(item)
        except (TypeError, ValueError):
            continue
    return result


@dataclass
class SafetyRequest:
    text: str
    region: Optional[str] = None


@dataclass
class BatchSafetyRequest:
    texts: List[str]
    region: Optional[str] = None


@dataclass
class SafetyDecision:
    allow: bool
    score: float
    category: Optional[str] = None
    rationale: Optional[str] = None


def decision_from_score(score: float, threshold: float, category: str = "toxicity") -> Dict[str, Any]:
    allow = score < threshold
    return {"allow": allow, "score": score, "category": category, "threshold": threshold}
