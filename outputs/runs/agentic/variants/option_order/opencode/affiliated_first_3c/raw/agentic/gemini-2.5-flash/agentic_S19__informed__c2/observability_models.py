from datetime import datetime
from typing import Dict, Any, List, Optional


class MetricQueryRequest:
    def __init__(
        self,
        project_id: str,
        metric_type: str,
        end_time: datetime,
        start_time: datetime,
        interval_minutes: int = 5,
        filter_str: Optional[str] = None,
    ):
        self.project_id = project_id
        self.metric_type = metric_type
        self.end_time = end_time
        self.start_time = start_time
        self.interval_minutes = interval_minutes
        self.filter_str = filter_str


class MetricPoint:
    def __init__(self, time: datetime, value: float):
        self.time = time
        self.value = value


class MetricSeries:
    def __init__(self, points: List[MetricPoint], labels: Dict[str, str] = None):
        self.points = points
        self.labels = labels if labels is not None else {}


class MetricAggregationResult:
    def __init__(
        self,
        metric_type: str,
        mean: Optional[float] = None,
        max: Optional[float] = None,
        min: Optional[float] = None,
        sum: Optional[float] = None,
        count: Optional[int] = None,
        labels: Dict[str, str] = None,
    ):
        self.metric_type = metric_type
        self.mean = mean
        self.max = max
        self.min = min
        self.sum = sum
        self.count = count
        self.labels = labels if labels is not None else {}
