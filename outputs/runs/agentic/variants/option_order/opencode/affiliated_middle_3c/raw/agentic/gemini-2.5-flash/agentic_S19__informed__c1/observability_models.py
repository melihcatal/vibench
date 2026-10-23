from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MetricDatapoint:
    timestamp: str
    value: float


@dataclass
class MetricSeries:
    metric: Dict[str, str]
    resource: Dict[str, str]
    points: List[MetricDatapoint]


@dataclass
class AggregatedMetric:
    interval_start: str
    interval_end: str
    value: float
    reducer: str
