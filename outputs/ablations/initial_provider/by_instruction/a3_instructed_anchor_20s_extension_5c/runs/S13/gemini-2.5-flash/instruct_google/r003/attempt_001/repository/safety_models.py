from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class SafetyRating:
    category: str
    probability: str
    blocked: bool

@dataclass
class ModerationResult:
    text: str
    safety_ratings: List[SafetyRating]
    is_allowed: bool = True
    reasons: List[str] = field(default_factory=list)

@dataclass
class ThresholdConfig:
    category: str
    block_probability: str  # e.g., "HARM_BLOCK_THRESHOLD_UNSPECIFIED", "BLOCK_LOW_AND_ABOVE"

