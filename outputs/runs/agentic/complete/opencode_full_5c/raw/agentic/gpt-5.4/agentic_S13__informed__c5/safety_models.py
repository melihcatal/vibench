from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyScore:
    category: str
    severity: float
    blocked: bool = False


@dataclass
class ModerationRequest:
    text: str
    language: str = "en"
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationResult:
    text: str
    action: str
    flagged: bool
    provider: str
    scores: List[SafetyScore] = field(default_factory=list)
    redacted_text: Optional[str] = None
    reasons: List[str] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: str) -> str:
    return " ".join((value or "").strip().split())


def build_score(category: str, severity: float, blocked: bool = False) -> SafetyScore:
    return SafetyScore(
        category=category, severity=float(severity), blocked=bool(blocked)
    )


def result_to_dict(result: ModerationResult) -> Dict[str, Any]:
    return {
        "text": result.text,
        "action": result.action,
        "flagged": result.flagged,
        "provider": result.provider,
        "scores": [
            {
                "category": score.category,
                "severity": score.severity,
                "blocked": score.blocked,
            }
            for score in result.scores
        ],
        "redacted_text": result.redacted_text,
        "reasons": list(result.reasons),
        "raw_response": dict(result.raw_response),
    }


def coerce_results(results: List[ModerationResult]) -> List[Dict[str, Any]]:
    return [result_to_dict(result) for result in results]
