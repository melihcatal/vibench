from typing import TypedDict, List
from datetime import datetime


class MetricDatapoint(TypedDict):
    Timestamp: datetime
    SampleCount: float
    Average: float
    Sum: float
    Minimum: float
    Maximum: float


MetricDatapoints = List[MetricDatapoint]


class Dimension(TypedDict):
    Name: str
    Value: str
