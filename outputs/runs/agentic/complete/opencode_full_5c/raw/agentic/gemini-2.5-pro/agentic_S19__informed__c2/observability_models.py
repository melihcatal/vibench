from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any


class TimeSeriesPoint(BaseModel):
    timestamp: str
    value: float


class MetricTimeSeries(BaseModel):
    metric_name: str
    dimensions: Dict[str, str]
    points: List[TimeSeriesPoint]


class QueryWindowRequest(BaseModel):
    project_id: str
    metric_name: str
    minutes_ago: int


class AggregationRequest(BaseModel):
    project_id: str
    metric_name: str
    minutes_ago: int
    alignment_period_seconds: int
    per_series_aligner: str
    cross_series_reducer: str


class FilteredQueryRequest(BaseModel):
    project_id: str
    metric_name: str
    minutes_ago: int
    filter_dimensions: Dict[str, str]


class ComparisonRequest(BaseModel):
    project_id: str
    metric_name: str
    minutes_ago: int
    filter1: Dict[str, str]
    filter2: Dict[str, str]


class SummaryRequest(BaseModel):
    metric_data: List[MetricTimeSeries]
    model: Optional[str] = "gpt-4o"


class SafetyCheckRequest(BaseModel):
    text_content: str


class TranslationRequest(BaseModel):
    text: str
    target_language: str = "DE"  # Default to German


class ArchiveRequest(BaseModel):
    bucket_name: str
    object_name: str
    data: Any
