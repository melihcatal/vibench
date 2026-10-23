from typing import List, Dict, Any, Literal
from dataclasses import dataclass, field

@dataclass
class ModerationRequest:
    text: str
    language_code: str = "en"

@dataclass
class ModerationResult:
    sentiment: Literal['POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED']
    sentiment_score: Dict[str, float]
    is_unsafe_based_on_sentiment: bool
    provider: str

@dataclass
class BatchModerationRequest:
    texts: List[str]
    language_code: str = "en"

@dataclass
class BatchModerationResult:
    original_text: str
    sentiment: Literal['POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED']
    sentiment_score: Dict[str, float]
    is_unsafe_based_on_sentiment: bool
    provider: str

@dataclass
class RedactionRequest:
    text: str
    language_code: str = "en"

@dataclass
class ThresholdDecision:
    disallowed_by_threshold: bool
    negative_threshold_applied: float
