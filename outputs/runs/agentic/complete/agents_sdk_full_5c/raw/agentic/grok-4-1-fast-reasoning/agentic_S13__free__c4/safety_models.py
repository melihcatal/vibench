from typing import TypedDict, Dict, List
from dataclasses import dataclass

@dataclass
class SafetyResult:
    input_text: str
    categories: Dict[str, float]
    flagged: bool
    severity: float

class ModerationDecision(TypedDict):
    allowed: bool
    reason: str
    scores: Dict[str, float]