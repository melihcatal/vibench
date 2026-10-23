from pydantic import BaseModel, Field
from typing import List, Dict, Any

class TimeSeriesPoint(BaseModel):
    timestamp: str
    value: float

class MetricSeries(BaseModel):
    metric_kind: str
    value_type: str
    points: List[TimeSeriesPoint]
    metric_labels: Dict[str, str] = Field(default_factory=dict)
    resource_labels: Dict[str, str] = Field(default_factory=dict)

class QueryResult(BaseModel):
    series: List[MetricSeries]

def normalize_to_models(response: Any) -> QueryResult:
    """Normalizes a Google Cloud Monitoring API response to local models."""
    result_list = []
    for series in response.time_series:
        points = []
        for point in series.points:
            # The value can be of different types, we handle double and int here.
            value = getattr(point.value, 'double_value', None) or getattr(point.value, 'int64_value', 0)
            points.append(
                TimeSeriesPoint(
                    timestamp=point.interval.end_time.isoformat(),
                    value=value
                )
            )
        
        result_list.append(
            MetricSeries(
                metric_kind=str(series.metric_kind),
                value_type=str(series.value_type),
                points=points,
                metric_labels=dict(series.metric.labels),
                resource_labels=dict(series.resource.labels)
            )
        )
    return QueryResult(series=result_list)
