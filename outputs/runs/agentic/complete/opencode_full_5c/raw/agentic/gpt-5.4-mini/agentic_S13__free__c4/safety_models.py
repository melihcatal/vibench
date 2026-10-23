from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(text: Optional[str]) -> str:
    return (text or "").strip()


def normalize_messages(messages: List[Any]) -> List[str]:
    result: List[str] = []
    for message in messages or []:
        if isinstance(message, str):
            result.append(normalize_text(message))
        elif isinstance(message, dict):
            result.append(normalize_text(message.get("text") or message.get("content")))
        else:
            result.append(
                normalize_text(
                    getattr(message, "text", None) or getattr(message, "content", None)
                )
            )
    return result


@dataclass
class ModerationDecision:
    flagged: bool
    categories: Dict[str, bool]
    scores: Dict[str, float]
    reason: Optional[str] = None


@dataclass
class ModerationBatchResult:
    decisions: List[ModerationDecision]


def decision_from_api(item: Any) -> ModerationDecision:
    categories = dict(getattr(item, "categories", {}) or {})
    scores = dict(getattr(item, "category_scores", {}) or {})
    return ModerationDecision(
        flagged=bool(getattr(item, "flagged", False)),
        categories=categories,
        scores=scores,
    )
