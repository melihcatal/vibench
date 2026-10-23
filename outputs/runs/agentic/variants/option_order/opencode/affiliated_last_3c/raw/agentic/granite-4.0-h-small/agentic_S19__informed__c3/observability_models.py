from typing import TypedDict, List


class MetricQueryResponse(TypedDict):
    MetricDataResults: List[dict]


class MetricDatapoint(TypedDict):
    Timestamp: int
    Value: float
    MetricName: str


class MetricStatResponse(TypedDict):
    MetricDataResults: List[dict]


class Dimension(TypedDict):
    Name: str
    Value: str


class MetricFilterQueryResponse(TypedDict):
    MetricDataResults: List[dict]
