from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class TimeSeriesPoint:
    timestamp: float
    value: float


@dataclass
class MetricTimeSeries:
    metric_name: str
    points: List[TimeSeriesPoint]
    dimensions: Dict[str, str]


@dataclass
class AggregatedMetricStats:
    metric_name: str
    aggregation: str
    value: float
    interval_seconds: int
    dimensions: Dict[str, str]


@dataclass
class MetricQuery:
    metric_name: str
    minutes_ago: int
    filter_dimensions: Dict[str, str] = None


@dataclass
class TranslationRequest:
    text: str
    target_locale: str


@dataclass
class SafetyCheckRequest:
    text: str


@dataclass
class ArchiveRequest:
    bucket_name: str
    object_name: str
    data: Any
