from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class TimeSeriesDataPoint:
    timestamp: str
    value: float


@dataclass
class MetricTimeSeries:
    metric_name: str
    resource_labels: Dict[str, str]
    points: List[TimeSeriesDataPoint]


@dataclass
class AggregatedMetricStats:
    metric_name: str
    aggregation: str
    value: float
    time_window: Dict[str, Any]
