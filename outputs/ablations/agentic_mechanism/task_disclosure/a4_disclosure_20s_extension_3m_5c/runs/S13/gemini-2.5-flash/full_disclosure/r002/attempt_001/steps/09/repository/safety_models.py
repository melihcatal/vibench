
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class CategoryScore:
    category: str
    score: float

@dataclass
class OverallDecision:
    decision: str
    reason: Optional[str] = None

@dataclass
class ModerationResponse:
    scores: List[CategoryScore]
    overall_decision: OverallDecision
    id: Optional[str] = None

@dataclass
class ModerationRequest:
    text_content: str
    id: Optional[str] = None
