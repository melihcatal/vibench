from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class TimeSeriesPoint:
    timestamp: float
    value: float


@dataclass
class MetricData:
    metric_name: str
    points: List[TimeSeriesPoint]
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class AggregatedMetricData:
    metric_name: str
    aggregation: str
    value: float
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class TranslationRequest:
    text: str
    target_language: str


@dataclass
class TranslatedText:
    original_text: str
    translated_text: str
    target_language: str


@dataclass
class UnsafeTextCheckRequest:
    text: str


@dataclass
class UnsafeTextCheckResult:
    text: str
    is_unsafe: bool
    scores: Dict[str, float]


@dataclass
class MetricSummaryRequest:
    metric_data: List[MetricData]


@dataclass
class MetricSummary:
    summary: str
