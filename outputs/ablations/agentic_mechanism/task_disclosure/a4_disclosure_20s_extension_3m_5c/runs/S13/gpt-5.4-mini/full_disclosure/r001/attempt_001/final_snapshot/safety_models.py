from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple


class ModerationCategory(str, Enum):
    HATE = "hate"
    SELF_HARM = "self_harm"
    SEXUAL = "sexual"
    VIOLENCE = "violence"
    HARASSMENT = "harassment"
    OTHER = "other"


@dataclass(frozen=True)
class Thresholds:
    hate: float = 0.5
    self_harm: float = 0.5
    sexual: float = 0.5
    violence: float = 0.5
    harassment: float = 0.5
    other: float = 0.5

    def get(self, category: str) -> float:
        key = _normalize_category_key(category)
        return {
            "hate": self.hate,
            "self_harm": self.self_harm,
            "sexual": self.sexual,
            "violence": self.violence,
            "harassment": self.harassment,
            "other": self.other,
        }.get(key, self.other)


@dataclass(frozen=True)
class ModerationRequest:
    text: str
    locale: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ModerationScore:
    category: str
    score: float
    flagged: bool = False


@dataclass(frozen=True)
class ModerationResponse:
    flagged: bool
    scores: Tuple[ModerationScore, ...] = ()
    rationale: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)


def _normalize_category_key(value: str) -> str:
    key = value.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "selfharm": "self_harm",
        "self_harm": "self_harm",
        "sexual": "sexual",
        "sex": "sexual",
        "violence": "violence",
        "violent": "violence",
        "hate": "hate",
        "harassment": "harassment",
        "harass": "harassment",
        "other": "other",
    }
    return aliases.get(key, key)


def normalize_category(value: str) -> str:
    return _normalize_category_key(value)


def normalize_score(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    if score != score:
        return 0.0
    if score < 0.0:
        return 0.0
    if score > 1.0:
        return 1.0
    return score


def normalize_flagged(value: Any, score: float = 0.0, threshold: float = 0.5) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return score >= threshold
    if isinstance(value, (int, float)):
        return normalize_score(value) >= threshold
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "1", "flagged", "unsafe"}:
            return True
        if lowered in {"false", "no", "0", "safe"}:
            return False
    return score >= threshold


def build_request(text: str, locale: Optional[str] = None, metadata: Optional[Mapping[str, Any]] = None) -> ModerationRequest:
    return ModerationRequest(text=text, locale=locale, metadata=dict(metadata or {}))


def response_from_mapping(data: Mapping[str, Any], thresholds: Optional[Thresholds] = None) -> ModerationResponse:
    thresholds = thresholds or Thresholds()
    flagged = bool(data.get("flagged", False))
    rationale = data.get("rationale")
    metadata = dict(data.get("metadata") or {})
    scores_data = data.get("scores") or data.get("categories") or []
    scores: List[ModerationScore] = []
    for item in scores_data:
        if not isinstance(item, Mapping):
            continue
        category = normalize_category(str(item.get("category") or item.get("name") or item.get("label") or "other"))
        score = normalize_score(item.get("score", item.get("value", item.get("probability"))))
        threshold = thresholds.get(category)
        item_flagged = normalize_flagged(item.get("flagged"), score=score, threshold=threshold)
        scores.append(ModerationScore(category=category, score=score, flagged=item_flagged))
        flagged = flagged or item_flagged
    return ModerationResponse(flagged=flagged, scores=tuple(scores), rationale=rationale, metadata=metadata)


def decision_from_scores(scores: Sequence[ModerationScore], thresholds: Optional[Thresholds] = None) -> bool:
    thresholds = thresholds or Thresholds()
    for score in scores:
        if score.flagged:
            return True
        if score.score >= thresholds.get(score.category):
            return True
    return False


def scores_to_mapping(scores: Iterable[ModerationScore]) -> Dict[str, Dict[str, Any]]:
    result: Dict[str, Dict[str, Any]] = {}
    for score in scores:
        result[score.category] = {"score": score.score, "flagged": score.flagged}
    return result
