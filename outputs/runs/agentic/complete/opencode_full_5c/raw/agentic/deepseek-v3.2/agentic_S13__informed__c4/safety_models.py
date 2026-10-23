from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "Hate"
    SELF_HARM = "SelfHarm"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"


@dataclass
class SafetyRequest:
    text: str
    categories: List[str] = field(
        default_factory=lambda: ["Hate", "SelfHarm", "Sexual", "Violence"]
    )
    blocklist_names: Optional[List[str]] = None
    halt_on_blocklist_hit: bool = False


@dataclass
class CategoryScore:
    severity: int
    score: float


@dataclass
class SafetyResponse:
    text: str
    categories: Dict[str, CategoryScore]
    blocklist_matches: Optional[List[Dict[str, Any]]] = None
    text_analysis: Optional[List[Dict[str, Any]]] = None


@dataclass
class BatchSafetyRequest:
    texts: List[str]
    categories: List[str] = field(
        default_factory=lambda: ["Hate", "SelfHarm", "Sexual", "Violence"]
    )


@dataclass
class BatchSafetyResponse:
    results: List[SafetyResponse]


@dataclass
class FlaggedSpan:
    text: str
    offset: int
    length: int
    category: Optional[str] = None
    severity: Optional[int] = None


@dataclass
class RedactionResult:
    redacted_text: str
    flagged_spans: List[FlaggedSpan]


@dataclass
class ThresholdConfig:
    hate: float = 0.7
    self_harm: float = 0.6
    sexual: float = 0.8
    violence: float = 0.7

    def to_dict(self) -> Dict[str, float]:
        return {
            "Hate": self.hate,
            "SelfHarm": self.self_harm,
            "Sexual": self.sexual,
            "Violence": self.violence,
        }


@dataclass
class ThresholdResult:
    text: str
    decision: str
    violations: List[Dict[str, Any]]
    category_scores: Dict[str, float]
    thresholds: Dict[str, float]
