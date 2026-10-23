from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MetricDataPoint:
    timestamp: str
    value: Any


@dataclass
class MetricTimeSeries:
    metric_kind: str
    value_type: str
    metric_labels: Dict[str, str]
    resource_labels: Dict[str, str]
    points: List[MetricDataPoint]
