from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ModerationRequest:
    text: str
    attributes: List[str]


@dataclass
class ModerationResponse:
    scores: Dict[str, float]


@dataclass
class BatchModerationRequest:
    texts: List[str]
    attributes: List[str]


@dataclass
class BatchModerationResponse:
    results: List[ModerationResponse]


@dataclass
class RedactionRequest:
    text: str
    attributes_to_redact: List[str]


@dataclass
class RedactionResponse:
    redacted_text: str
    flagged_spans: List[dict]


@dataclass
class ThresholdRequest:
    scores: Dict[str, float]
    thresholds: Dict[str, float]


@dataclass
class ThresholdResponse:
    is_safe: bool
    triggered_categories: List[str]
