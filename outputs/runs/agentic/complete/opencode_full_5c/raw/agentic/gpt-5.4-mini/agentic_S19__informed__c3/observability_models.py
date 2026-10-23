from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int = 300
    stat: str = "Average"
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeriesPoint:
    timestamp: datetime
    value: float


@dataclass
class MetricQueryResponse:
    metric_name: str
    points: List[MetricSeriesPoint]
    unit: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)


def normalize_dimensions(dimensions: Dict[str, str]) -> List[Dict[str, str]]:
    return [{"Name": k, "Value": v} for k, v in sorted(dimensions.items())]


def point_from_datapoint(datapoint: Dict[str, Any]) -> MetricSeriesPoint:
    value = datapoint.get("Average")
    if value is None:
        value = datapoint.get("Sum")
    if value is None:
        value = datapoint.get("Maximum")
    if value is None:
        value = datapoint.get("Minimum")
    return MetricSeriesPoint(
        timestamp=datapoint["Timestamp"], value=float(value or 0.0)
    )
