from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class MetricQueryRequest:
    metric_type: str
    window_hours: int = 1


@dataclass
class MetricDataPoint:
    timestamp: float
    value: float
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]


@dataclass
class MetricStatsRequest:
    metric_type: str
    window_hours: int = 1
    filter_dimensions: Optional[Dict[str, str]] = None


@dataclass
class MetricStatsResponse:
    metric_type: str
    window_hours: int
    count: int
    mean: float
    min: float
    max: float
    sum: float


@dataclass
class DimensionFilterRequest:
    metric_type: str
    dimensions: Dict[str, str]
    window_hours: int = 1


@dataclass
class MetricComparisonRequest:
    metric_type: str
    filter_a: Dict[str, str]
    filter_b: Dict[str, str]
    window_hours: int = 1


@dataclass
class MetricComparisonResponse:
    metric_type: str
    window_hours: int
    series_a_stats: Dict[str, float]
    series_b_stats: Dict[str, float]