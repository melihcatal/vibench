from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class MetricQueryRequest:
    project_id: str
    metric_type: str
    interval_start_time: str
    interval_end_time: str
    aggregation_alignment_period: str = "60s"
    aggregation_reducer: str = "REDUCE_MEAN"
    filter_string: str = ""


@dataclass
class MetricDataPoint:
    timestamp: str
    value: Any


@dataclass
class MetricSeries:
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[MetricDataPoint]


@dataclass
class MetricAggregate:
    statistic: str
    value: Any
    timestamp: str


@dataclass
class MetricComparisonResult:
    series_a: List[MetricDataPoint]
    series_b: List[MetricDataPoint]
    difference: List[MetricDataPoint]
