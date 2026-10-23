import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class MetricQueryRequest:
    project_id: str
    metric_type: str
    interval_start_time: str
    interval_end_time: str
    filter_string: Optional[str] = None
    group_by_fields: Optional[List[str]] = None
    aggregator: Optional[str] = None


@dataclasses.dataclass
class MetricPoint:
    time: str
    value: Any
    labels: Dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class MetricSeries:
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[MetricPoint]
