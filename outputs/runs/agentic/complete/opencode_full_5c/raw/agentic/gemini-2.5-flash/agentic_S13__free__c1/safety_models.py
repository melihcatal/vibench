import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class ModerationCategory:
    category: str
    score: float
    threshold: Optional[float] = None
    allowed: Optional[bool] = None


@dataclasses.dataclass
class TextModerationRequest:
    text_content: str
    context: Optional[str] = None


@dataclasses.dataclass
class TextModerationResponse:
    filtered_text: Optional[str] = None
    categories: List[ModerationCategory] = dataclasses.field(default_factory=list)
    is_safe: bool = True
    decision_reason: Optional[str] = None
