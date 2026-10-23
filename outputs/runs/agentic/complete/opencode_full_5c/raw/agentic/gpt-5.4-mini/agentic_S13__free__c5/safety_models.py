from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def _lower_text(value: Optional[str]) -> str:
    return (value or "").strip().lower()


def normalize_messages(messages: Iterable[Any]) -> List[str]:
    normalized: List[str] = []
    for message in messages:
        if isinstance(message, str):
            normalized.append(message)
        elif isinstance(message, dict):
            normalized.append(str(message.get("text") or message.get("content") or ""))
        else:
            normalized.append(str(message))
    return normalized


def to_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    return _lower_text(str(value)) in {"1", "true", "yes", "allow", "safe", "pass"}


def clamp_score(value: Any) -> float:
    try:
        score = float(value)
    except Exception:
        score = 0.0
    if score < 0.0:
        return 0.0
    if score > 1.0:
        return 1.0
    return score


def normalize_category_scores(raw: Any) -> Dict[str, float]:
    if not isinstance(raw, dict):
        return {}
    return {str(k): clamp_score(v) for k, v in raw.items()}


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    redacted_text: Optional[str] = None
    decision: Optional[str] = None
    rationale: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ModerationResult":
        return cls(
            flagged=to_bool(data.get("flagged")),
            categories={
                str(k): to_bool(v) for k, v in (data.get("categories") or {}).items()
            },
            category_scores=normalize_category_scores(
                data.get("category_scores") or data.get("scores") or {}
            ),
            redacted_text=data.get("redacted_text") or data.get("text_redacted"),
            decision=data.get("decision"),
            rationale=data.get("rationale") or data.get("reason"),
        )


@dataclass
class BatchModerationResult:
    results: List[ModerationResult]


@dataclass
class SafetyThreshold:
    category: str
    threshold: float
