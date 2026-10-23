import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class ModerationCategory:
    category: str
    severity: int
    threshold: Optional[float] = None


@dataclasses.dataclass
class ModerationResult:
    text: str
    categories_analysis: List[ModerationCategory]
    overall_decision: str = "Accept"  # "Accept" or "Reject" or "Review"
