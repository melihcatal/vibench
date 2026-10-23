import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class MetricPoint:
    timestamp: float
    value: float

@dataclasses.dataclass
class MetricTimeSeries:
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[MetricPoint]

@dataclasses.dataclass
class MetricData:
    time_series: List[MetricTimeSeries]
