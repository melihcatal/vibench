# [HELPER] observability_models.py
from pydantic import BaseModel
from datetime import datetime
import typing as t

class MetricDimension(BaseModel):
    Name: str
    Value: t.Optional[str]

class MetricRequest(BaseModel):
    metric_name: str
    namespace: t.Optional[str] = None
    dimensions: t.Optional[t.Dict[str, t.Union[str, t.List[str]]]] = None
    start_time: str  # ISO 8601 UTC string
    end_time: str    # ISO 8601 UTC string
    period: int      # seconds
    statistic: t.Optional[str] = None

    def copy(self):
        return MetricRequest(**self.dict())

class MetricDatapoint(BaseModel):
    Timestamp: datetime
    Value: float
    Unit: t.Optional[str]

class MetricResponse(BaseModel):
    # CloudWatch returns a list named 'Datapoints'
    datapoints: t.List[MetricDatapoint]
    label: t.Optional[str] = None

class MetricAggregateResponse(BaseModel):
    # Aggregated result (e.g., average, sum) across requested period(s)
    value: float
    unit: str
    label: t.Optional[str] = None
