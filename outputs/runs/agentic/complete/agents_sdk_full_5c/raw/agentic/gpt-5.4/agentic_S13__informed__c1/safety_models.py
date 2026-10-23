from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyCategoryScore:
    name: str
    score: float


@dataclass
class SafetyDecision:
    text: str
    flagged: bool
    categories: Dict[str, float] = field(default_factory=dict)
    block_reason: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class BatchSafetyDecision:
    decisions: List[SafetyDecision]


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    flagged_spans: List[Dict[str, Any]] = field(default_factory=list)
    categories: Dict[str, float] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None


DEFAULT_CATEGORY_MAP = {
    "TOXICITY": "toxicity",
    "SEVERE_TOXICITY": "severe_toxicity",
    "INSULT": "insult",
    "PROFANITY": "profanity",
    "THREAT": "threat",
    "IDENTITY_ATTACK": "identity_attack",
    "SEXUALLY_EXPLICIT": "sexually_explicit",
}


def normalize_perspective_scores(attribute_scores: Dict[str, Any]) -> Dict[str, float]:
    normalized: Dict[str, float] = {}
    for provider_name, payload in attribute_scores.items():
        summary = payload.get("summaryScore") or {}
        value = summary.get("value")
        if value is None:
            continue
        normalized[DEFAULT_CATEGORY_MAP.get(provider_name, provider_name.lower())] = float(value)
    return normalized


def top_category(categories: Dict[str, float]) -> Optional[str]:
    if not categories:
        return None
    return max(categories, key=categories.get)


def clamp_score(score: float) -> float:
    return max(0.0, min(1.0, float(score)))
