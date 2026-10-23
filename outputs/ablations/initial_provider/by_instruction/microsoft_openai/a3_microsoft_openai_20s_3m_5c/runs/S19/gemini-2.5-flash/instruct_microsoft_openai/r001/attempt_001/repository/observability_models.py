import dataclasses
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclasses.dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float
    dimensions: Optional[Dict[str, str]] = None

@dataclasses.dataclass
class MetricQueryRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    interval: Optional[str] = None
    dimensions_filter: Optional[Dict[str, str]] = None

@dataclasses.dataclass
class MetricQueryResponse:
    metric_name: str
    data_points: List[MetricDataPoint]
    unit: Optional[str] = None
    resource_id: Optional[str] = None
