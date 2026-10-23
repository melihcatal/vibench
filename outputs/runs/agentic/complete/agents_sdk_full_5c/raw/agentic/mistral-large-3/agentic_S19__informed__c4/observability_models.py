from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class MetricPoint(BaseModel):
    timestamp: str
    value: float
    resource: str
    labels: Dict[str, str]


class MetricStats(BaseModel):
    resource: str
    labels: Dict[str, str]
    count: int
    mean: float
    min: float
    max: float


class MetricSeriesComparison(BaseModel):
    series_a: List[MetricPoint]
    series_b: List[MetricPoint]


def normalize_metric_response(data: List[Dict[str, Any]]) -> List[MetricPoint]:
    """Normalize raw metric data into MetricPoint models."""
    return [
        MetricPoint(
            timestamp=point["timestamp"].isoformat(),
            value=point["value"],
            resource=point["resource"],
            labels=point["labels"]
        )
        for point in data
    ]