from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


@dataclass
class ModerationRequest:
    text: str
    user_id: Optional[str] = None

    def normalized(self) -> "ModerationRequest":
        return ModerationRequest(text=normalize_text(self.text), user_id=self.user_id)


@dataclass
class ModerationDecision:
    allowed: bool
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    model: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationItem:
    index: int
    text: str
    decision: Optional[ModerationDecision] = None


@dataclass
class BatchModerationResponse:
    items: List[BatchModerationItem]


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str


@dataclass
class RedactionResult:
    redacted_text: str
    spans: List[RedactionSpan] = field(default_factory=list)
    model: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)
