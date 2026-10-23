from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ModerationCategory:
    name: str
    score: float


@dataclass
class ModerationResult:
    text: str
    scores: Dict[str, float]  # e.g., {"TOXICITY": 0.8, "SPAM": 0.1}
    categories: List[ModerationCategory]  # Detailed categories if available from API


@dataclass
class ModerationDecision:
    allow: bool
    reason: Optional[str] = None
