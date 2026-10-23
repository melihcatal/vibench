from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json

def normalize_categories(raw_scores: Dict[str, float], thresholds: Optional[Dict[str, float]] = None) -> List['CategoryScore']:
    scores = []
    for category, prob in raw_scores.items():
        blocked = bool(thresholds and thresholds.get(category, 0.5) &lt; prob)
        scores.append(CategoryScore(category=category, probability=prob, blocked=blocked))
    return scores

@dataclass
class Span:
    start: int
    end: int
    category: str
    text: str
    probability: Optional[float] = None

@dataclass
class CategoryScore:
    category: str
    probability: float
    blocked: bool = False

@dataclass
class ModerationResult:
    input_text: str
    scores: List[CategoryScore] = field(default_factory=list)
    flagged: bool = False
    spans: List[Span] = field(default_factory=list)
    redacted_text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_text": self.input_text,
            "scores": [{"category": s.category, "probability": s.probability, "blocked": s.blocked} for s in self.scores],
            "flagged": self.flagged,
            "spans": [{"start": sp.start, "end": sp.end, "category": sp.category, "text": sp.text, "probability": sp.probability} for sp in self.spans],
            "redacted_text": self.redacted_text
        }
