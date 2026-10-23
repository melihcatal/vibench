from typing import List, Dict, Any, Union
from pydantic import BaseModel, Field


class TimeSeriesPoint(BaseModel):
    timestamp: float
    value: float


class MetricData(BaseModel):
    metric_name: str
    points: List[TimeSeriesPoint]
    dimensions: Dict[str, str] = Field(default_factory=dict)


class MetricStatistic(BaseModel):
    name: str
    value: float


class MetricStatistics(BaseModel):
    metric_name: str
    statistics: List[MetricStatistic]
    dimensions: Dict[str, str] = Field(default_factory=dict)
