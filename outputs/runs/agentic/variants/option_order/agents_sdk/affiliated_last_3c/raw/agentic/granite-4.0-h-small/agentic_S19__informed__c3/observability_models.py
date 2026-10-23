from typing import TypedDict, List, Any

# Common model definitions usable by all integration files

class Dimension(TypedDict):
    Name: str
    Value: str

class MetricQueryRequest(TypedDict):
    metric_name: str
    start_time: str  # ISO8601
    end_time: str
    period: int
    statistics: List[str]
    dimensions: List[Dimension]

class MetricAggregateRequest(TypedDict):
    metric_name: str
    start_time: str
    end_time: str
    period: int
    statistics: List[str]

class MetricFilterRequest(TypedDict):
    metric_name: str
    start_time: str
    end_time: str
    dimensions: List[Dimension]

class MetricCompareRequest(TypedDict):
    metric_name: str
    start_time: str
    end_time: str
    period: int
    resources: List[str]

class DimensionFilter(TypedDict):
    Name: str
    Value: str
