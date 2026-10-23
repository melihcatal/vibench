from typing import List, Dict, Optional, TypedDict
from dataclasses import dataclass


class TextModerationRequest(TypedDict):
    text: str
    categories: Optional[List[str]]
    language: Optional[str]


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]
    redacted_text: Optional[str] = None


@dataclass
class BatchModerationResult:
    results: List[ModerationResult]


@dataclass
class SafetyThresholdConfig:
    category_thresholds: Dict[str, float]
    default_threshold: float = 0.5