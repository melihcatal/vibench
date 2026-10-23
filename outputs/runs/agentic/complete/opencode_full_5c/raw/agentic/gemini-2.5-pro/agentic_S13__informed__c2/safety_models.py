from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class ModerationRequest:
    text: str


@dataclass
class BatchModerationRequest:
    texts: List[str]


@dataclass
class RedactionRequest:
    text: str
    categories: List[str]


@dataclass
class ThresholdRequest:
    text: str
    thresholds: Dict[str, float]


@dataclass
class ModerationResult:
    is_safe: bool
    violated_categories: List[str]
    scores: Dict[str, float]


@dataclass
class BatchModerationResult:
    results: List[ModerationResult]


@dataclass
class RedactionResult:
    redacted_text: str
    flagged_spans: List[Dict]


@dataclass
class ThresholdResult:
    is_safe: bool
    violated_categories: List[str]
