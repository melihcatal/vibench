import dataclasses
from typing import Dict, Any, List, Optional


@dataclasses.dataclass
class TimeWindow:
    start_time: str
    end_time: str


@dataclasses.dataclass
class MetricQuery:
    project_id: str
    metric_type: str
    interval: TimeWindow
    filter_string: Optional[str] = None
    aggregation_reducer: Optional[str] = None
    aggregation_aligner: Optional[str] = None
    group_by_fields: Optional[List[str]] = None


@dataclasses.dataclass
class MetricDataPoint:
    timestamp: str
    value: float
    labels: Dict[str, str]


@dataclasses.dataclass
class MetricTimeSeries:
    metric_type: str
    resource_labels: Dict[str, str]
    points: List[MetricDataPoint]


@dataclasses.dataclass
class MetricAnnotation:
    text: str
    language_code: Optional[str] = None


@dataclasses.dataclass
class ArchivedMetricSnapshot:
    bucket_name: str
    blob_name: str
    content: str
