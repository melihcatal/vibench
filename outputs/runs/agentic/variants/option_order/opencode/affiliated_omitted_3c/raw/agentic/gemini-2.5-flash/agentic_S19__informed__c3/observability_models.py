from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class MetricDimension:
    Name: str
    Value: str


@dataclass
class MetricDataQuery:
    Id: str
    MetricStat: Dict[str, Any] = field(default_factory=dict)
    Expression: str = ""
    Label: str = ""
    ReturnData: bool = True
    Period: int = 300  # Default to 5 minutes


@dataclass
class GetMetricDataRequest:
    MetricDataQueries: List[MetricDataQuery]
    StartTime: str
    EndTime: str
    NextToken: str = ""
    ScanBy: str = "TimestampAscending"
    MaxDatapoints: int = 100
