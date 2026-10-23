from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MetricQuery:
    project_id: str
    metric_type: str
    end_time: str
    start_time: str
    interval_seconds: int = 60
    filter: str = None
    group_by_fields: List[str] = None
    view: str = "FULL"  # "FULL" or "HEADERS"


@dataclass
class MetricDataPoint:
    value: Any
    timestamp: str


@dataclass
class MetricSeries:
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[MetricDataPoint]


@dataclass
class MetricResponse:
    metric_series: List[MetricSeries]
