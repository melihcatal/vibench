from pydantic import BaseModel, Field
from typing import List, Dict, Any


class MetricQueryPayload(BaseModel):
    metric: str
    start_time: int
    end_time: int
    

class TimeSeriesPoint(BaseModel):
    timestamp: float
    value: float


class MetricQueryResponse(BaseModel):
    points: List[TimeSeriesPoint]


class MetricAggregationPayload(MetricQueryPayload):
    aggregator: str = "mean"
    period_seconds: int = 60


class MetricFilterPayload(MetricQueryPayload):
    filters: Dict[str, str]


class MetricComparisonPayload(BaseModel):
    metric: str
    start_time: int
    end_time: int
    filter_a: Dict[str, str]
    filter_b: Dict[str, str]


class MetricCompareResponse(BaseModel):
    series_a: List[TimeSeriesPoint]
    series_b: List[TimeSeriesPoint]
