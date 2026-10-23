from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class TimeSeriesPoint(BaseModel):
    timestamp: datetime
    value: float


class TimeSeries(BaseModel):
    metric_name: str
    resource_labels: Dict[str, str] = Field(default_factory=dict)
    points: List[TimeSeriesPoint] = Field(default_factory=list)


class MetricFilter(BaseModel):
    metric_type: str
    resource_labels: Dict[str, str] = Field(default_factory=dict)
    filter_conditions: Optional[str] = None


class AggregationOptions(BaseModel):
    per_series_aligner: str
    cross_series_reducer: str
    group_by_fields: List[str] = Field(default_factory=list)


class QueryResult(BaseModel):
    series: List[TimeSeries] = Field(default_factory=list)
    raw_response: Optional[Any] = None
