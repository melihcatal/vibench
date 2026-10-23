from pydantic import BaseModel
from typing import Dict, List, Optional


class MetricDataPoint(BaseModel):
    timestamp: float
    value: float
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]


class MetricStats(BaseModel):
    min: float
    max: float
    avg: float
    count: int


class MetricComparisonResult(BaseModel):
    series_a_avg: float
    series_b_avg: float
    difference: float
    series_a_count: int
    series_b_count: int


class MetricSummaryRequest(BaseModel):
    metric_name: str
    hours: int = 1
    threshold: Optional[float] = None