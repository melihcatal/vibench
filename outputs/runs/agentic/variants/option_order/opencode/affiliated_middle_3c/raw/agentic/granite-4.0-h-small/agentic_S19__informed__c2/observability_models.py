from typing import List, Dict, Any
from pydantic import BaseModel


class MetricQueryRequest(BaseModel):
    resource_id: str
    metric_name: str
    start_time: str  # ISO 8601 string
    end_time: str  # ISO 8601 string
    interval: str = "PT1M"
    aggregation: str = "Average"
    filter: str = None  # optional dimension filter expression


class MetricAggregateRequest(BaseModel):
    resource_id: str
    metric_name: str
    start_time: str
    end_time: str
    granularity: str = "1h"
    aggregation: str = "Average,Total,Maximum,Minimum,Count"
    filter: str = None


class MetricFilterRequest(BaseModel):
    resource_id: str
    metric_name: str
    filter_expr: str  # dimension filter expression (e.g., ResourceId = 'i-1234')
    start_time: str
    end_time: str
    interval: str = "PT1M"
    aggregation: str = "Average"


class CompareRequest(BaseModel):
    series: List[
        Dict[str, Any]
    ]  # list of dicts with keys: resource_id, metric_name, filter, start_time, end_time


class MetricDataResult(BaseModel):
    ref_id: str
    datapoints: List[Dict[str, Any]]  # each point: {timestamp: str, value: float}


class MetricAggregateResult(BaseModel):
    ref_id: str
    statistics: Dict[
        str, Any
    ]  # keys: Average, Sum, Maximum, Minimum, SampleCount, etc.


class MetricFilterResult(BaseModel):
    ref_id: str
    datapoints: List[Dict[str, Any]]


class CompareResult(BaseModel):
    series: List[MetricDataResult]
