from pydantic import BaseModel
from typing import Dict, Any, List


class TimeWindow(BaseModel):
    start_time: str
    end_time: str


class MetricQuery(BaseModel):
    metric_type: str
    project_id: str
    interval: TimeWindow


class MetricDataPoint(BaseModel):
    timestamp: str
    value: float


class MetricSeries(BaseModel):
    metric_labels: Dict[str, str]
    resource_labels: Dict[str, str]
    points: List[MetricDataPoint]


class MetricAggregate(BaseModel):
    metric_type: str
    project_id: str
    interval: TimeWindow
    aggregation_function: str


class MetricFilter(BaseModel):
    metric_type: str
    project_id: str
    interval: TimeWindow
    filters: Dict[str, str]


class MetricComparison(BaseModel):
    metric_type: str
    project_id: str
    interval: TimeWindow
    filter1: Dict[str, str]
    filter2: Dict[str, str]
