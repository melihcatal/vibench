from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MetricDataPoint:
    timestamp: float
    value: float
    labels: Dict[str, str]


@dataclass
class MetricStats:
    count: int = 0
    sum: float = 0.0
    avg: float = 0.0
    min: float = float('inf')
    max: float = float('-inf')


@dataclass
class MetricQueryRequest:
    metric_type: str
    hours: int = 1
    dimension_filters: Dict[str, str] = None


@dataclass
class MetricComparisonResult:
    series_a_avg: float
    series_b_avg: float
    difference: float
    series_a_count: int
    series_b_count: int