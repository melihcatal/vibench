from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any

@dataclass
class MetricQuery:
    namespace: str
    metric_name: str
    dimensions: Dict[str, str]
    start_time: datetime
    end_time: datetime
    period: int
    statistics: List[str]

@dataclass
class MetricDatapoint:
    timestamp: datetime
    value: float
    unit: str

@dataclass
class MetricQueryResult:
    label: str
    datapoints: List[MetricDatapoint]
    status_code: int
