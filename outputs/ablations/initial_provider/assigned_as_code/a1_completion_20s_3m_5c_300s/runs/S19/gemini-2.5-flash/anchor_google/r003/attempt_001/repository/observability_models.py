import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class MetricPoint:
    timestamp: float
    value: float

@dataclasses.dataclass
class MetricSeries:
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[MetricPoint]

@dataclasses.dataclass
class MetricQueryResponse:
    series: List[MetricSeries]

@dataclasses.dataclass
class MetricAggregate:
    timestamp: float
    mean: float
    min: float
    max: float
    sum: float
    count: int
