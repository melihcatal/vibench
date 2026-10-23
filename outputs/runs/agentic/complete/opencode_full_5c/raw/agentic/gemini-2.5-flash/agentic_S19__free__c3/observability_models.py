from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class TimeSeriesData:
    metric_type: str
    resource_labels: Dict[str, str]
    points: List[Dict[str, Any]]  # Each point contains 'interval' and 'value'


@dataclass
class MetricAggregate:
    metric_type: str
    resource_labels: Dict[str, str]
    reducer: str
    value: Any


@dataclass
class MetricComparison:
    metric_type: str
    series_a: TimeSeriesData
    series_b: TimeSeriesData


@dataclass
class Annotation:
    text: str
    severity: str = "UNKNOWN"  # e.g., UNKNOWN, VERY_UNLIKELY, UNLIKELY, NEUTRAL, LIKELY, VERY_LIKELY


@dataclass
class Translation:
    original_text: str
    translated_text: str
    target_language: str


@dataclass
class MetricSnapshot:
    metric_type: str
    data: List[TimeSeriesData]
    timestamp: str
