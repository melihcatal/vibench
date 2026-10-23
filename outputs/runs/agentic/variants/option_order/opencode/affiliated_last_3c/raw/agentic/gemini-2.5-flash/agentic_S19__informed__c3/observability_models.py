import datetime
from typing import List, Dict, Any, Optional


class MetricQuery:
    def __init__(
        self,
        project_id: str,
        metric_type: str,
        end_time: datetime.datetime,
        start_time: datetime.datetime,
        interval_seconds: int,
    ):
        self.project_id = project_id
        self.metric_type = metric_type
        self.end_time = end_time
        self.start_time = start_time
        self.interval_seconds = interval_seconds


class MetricDataPoint:
    def __init__(
        self,
        timestamp: datetime.datetime,
        value: float,
        labels: Optional[Dict[str, str]] = None,
    ):
        self.timestamp = timestamp
        self.value = value
        self.labels = labels if labels is not None else {}


class MetricStatistics:
    def __init__(
        self,
        metric_type: str,
        start_time: datetime.datetime,
        end_time: datetime.datetime,
        mean: Optional[float] = None,
        max: Optional[float] = None,
        min: Optional[float] = None,
        sum: Optional[float] = None,
        count: Optional[int] = None,
    ):
        self.metric_type = metric_type
        self.start_time = start_time
        self.end_time = end_time
        self.mean = mean
        self.max = max
        self.min = min
        self.sum = sum
        self.count = count


class MetricFilter:
    def __init__(
        self,
        project_id: str,
        metric_type: str,
        end_time: datetime.datetime,
        start_time: datetime.datetime,
        interval_seconds: int,
        resource_labels: Optional[Dict[str, str]] = None,
    ):
        self.project_id = project_id
        self.metric_type = metric_type
        self.end_time = end_time
        self.start_time = start_time
        self.interval_seconds = interval_seconds
        self.resource_labels = resource_labels if resource_labels is not None else {}


class MetricSeries:
    def __init__(
        self,
        metric_type: str,
        data_points: List[MetricDataPoint],
        resource_labels: Optional[Dict[str, str]] = None,
    ):
        self.metric_type = metric_type
        self.data_points = data_points
        self.resource_labels = resource_labels if resource_labels is not None else {}
