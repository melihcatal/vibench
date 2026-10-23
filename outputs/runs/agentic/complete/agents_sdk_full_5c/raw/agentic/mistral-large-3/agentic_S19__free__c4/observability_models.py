from pydantic import BaseModel
from typing import Optional, Dict, List


class MetricQueryRequest(BaseModel):
    metric_type: str
    hours: int = 1
    dimension_filters: Optional[Dict[str, str]] = None


class MetricDataPoint(BaseModel):
    timestamp: float
    value: float
    labels: Dict[str, str]


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