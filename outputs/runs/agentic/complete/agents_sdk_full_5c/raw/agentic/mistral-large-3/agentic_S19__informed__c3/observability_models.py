from pydantic import BaseModel
from datetime import datetime
from typing import Dict, List, Optional

class MetricQueryRequest(BaseModel):
    metric_type: str
    window_seconds: int
    resource_labels: Optional[Dict[str, str]] = None

class MetricDataPoint(BaseModel):
    timestamp: datetime
    value: float
    labels: Dict[str, str]

class MetricStatsRequest(BaseModel):
    metric_type: str
    window_seconds: int
    alignment_period: int = 60
    resource_labels: Optional[Dict[str, str]] = None

class MetricStatsResponse(BaseModel):
    metric_type: str
    window_seconds: int
    count: int
    mean: float
    min: float
    max: float

class DimensionFilterRequest(BaseModel):
    metric_type: str
    window_seconds: int
    dimension_filters: Optional[Dict[str, str]] = None

class MetricComparisonRequest(BaseModel):
    metric_type: str
    window_seconds: int
    labels_a: Dict[str, str]
    labels_b: Dict[str, str]

class MetricComparisonResult(BaseModel):
    metric_type: str
    window_seconds: int
    average_a: float
    average_b: float
    difference: float
    labels_a: Dict[str, str]
    labels_b: Dict[str, str]