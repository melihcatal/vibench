import os
from typing import TypedDict, List

class MetricWindowPoint(TypedDict):
    timestamp: str
    value: float

class MetricWindowRequest(TypedDict):
    metric: str
    start: str  # ISO 8601
    end: str

class MetricWindowResponse(TypedDict):
    points: List[MetricWindowPoint]

class MetricStatsPoint(TypedDict):
    timestamp: str
    sum: float
    avg: float
    min: float
    max: float
    count: int

class MetricStatsRequest(TypedDict):
    metric: str
    start: str
    end: str
    aggregation: str

class MetricStatsResponse(TypedDict):
    statistics: List[MetricStatsPoint]

class FilterDimension(TypedDict):
    name: str
    value: str

class FilteredMetricRequest(TypedDict):
    metric: str
    start: str
    end: str
    dimensions: List[FilterDimension]

class FilteredMetricResponse(TypedDict):
    points: List[MetricWindowPoint]

class CompareResource(TypedDict):
    name: str
    points: List[MetricWindowPoint]

class CompareMetricRequest(TypedDict):
    metric: str
    start: str
    end: str
    resource_a: str
    resource_b: str

class CompareMetricResponse(TypedDict):
    resource_a: CompareResource
    resource_b: CompareResource
