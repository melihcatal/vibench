from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class MetricQueryRequest(BaseModel):
    metric_type: str
    project_id: str
    hours: int = 1

class MetricDataPoint(BaseModel):
    timestamp: datetime
    value: float
    resource_labels: Dict[str, str]

class MetricStatsRequest(BaseModel):
    metric_type: str
    project_id: str
    hours: int = 1
    group_by_fields: Optional[List[str]] = None

class MetricStatsResponse(BaseModel):
    stats: List[Dict[str, object]]

class DimensionFilterRequest(BaseModel):
    metric_type: str
    project_id: str
    dimensions: Dict[str, str]
    hours: int = 1

class MetricComparisonRequest(BaseModel):
    metric_type: str
    project_id: str
    dimensions_a: Dict[str, str]
    dimensions_b: Dict[str, str]
    hours: int = 1

class MetricComparisonResult(BaseModel):
    series_a_values: List[float]
    series_b_values: List[float]
    mean_a: float
    mean_b: float