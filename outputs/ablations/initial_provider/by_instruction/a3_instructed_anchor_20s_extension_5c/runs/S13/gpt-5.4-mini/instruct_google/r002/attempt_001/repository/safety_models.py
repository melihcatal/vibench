from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


@dataclass
class SafetyRequest:
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyDecision:
    label: str
    score: float
    categories: Dict[str, float] = field(default_factory=dict)
    redacted_text: Optional[str] = None
    spans: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def build_request(text: Any, metadata: Optional[Dict[str, Any]] = None) -> SafetyRequest:
    return SafetyRequest(text=normalize_text(text), metadata=metadata or {})


def decision_from_payload(payload: Dict[str, Any], redacted_text: Optional[str] = None) -> SafetyDecision:
    categories = payload.get("category_scores") or payload.get("categories") or {}
    spans = payload.get("spans") or []
    return SafetyDecision(
        label=payload.get("label") or payload.get("decision") or "unknown",
        score=float(payload.get("score") or payload.get("severity") or 0.0),
        categories={k: float(v) for k, v in categories.items()},
        redacted_text=redacted_text,
        spans=spans,
        raw=payload,
    )
