from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class MetricPoint:
    value: Any
    timestamp: datetime


@dataclass
class MetricSeries:
    metric_type: str
    resource_labels: Dict[str, str]
    points: List[MetricPoint]


@dataclass
class MetricQueryRequest:
    project_id: str
    metric_type: str
    end_time: datetime
    minutes: int = 5
    filter: Optional[str] = None
    aggregation_function: Optional[str] = None


@dataclass
class MetricQueryResponse:
    time_series: List[MetricSeries]
    raw_response: Any
