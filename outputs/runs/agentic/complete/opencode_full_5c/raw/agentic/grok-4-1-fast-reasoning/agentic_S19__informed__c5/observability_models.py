from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class TimeWindow:
    start: str  # e.g. "2024-04-21T00:00:00Z"
    end: str


@dataclass
class Dimension:
    name: str
    value: str


@dataclass
class MetricQuery:
    namespace: str
    metric_name: str
    dimensions: Optional[List[Dimension]] = None


@dataclass
class MetricDatapoint:
    timestamp: str
    value: float


@dataclass
class MetricResponse:
    query: MetricQuery
    datapoints: List[MetricDatapoint]
