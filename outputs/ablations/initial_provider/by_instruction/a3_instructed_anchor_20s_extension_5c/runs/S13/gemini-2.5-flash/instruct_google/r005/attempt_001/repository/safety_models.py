from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class SafetyRating:
    category: str
    probability: str
    probability_score: float
    severity: Optional[float] = None

@dataclass
class SafetyAttribute:
    text_content: str
    categories: List[SafetyRating]
    blocked: bool

@dataclass
class ModerationResponse:
    id: str
    model: str
    results: List[SafetyAttribute]

@dataclass
class ModerationRequest:
    text_content: str
