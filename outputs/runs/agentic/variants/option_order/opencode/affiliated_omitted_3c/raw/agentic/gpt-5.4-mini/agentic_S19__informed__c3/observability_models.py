from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


def isoformat_utc(value: datetime) -> str:
    if value.tzinfo is None:
        return value.isoformat() + "Z"
    return value.astimezone().isoformat()


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@dataclass
class MetricQuery:
    metric_name: str
    start_time: datetime
    end_time: datetime
    namespace: Optional[str] = None
    period: Optional[int] = None
    statistic: Optional[str] = None
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class MetricPoint:
    timestamp: Optional[str]
    value: Optional[float]
    dimensions: Dict[str, str]


@dataclass
class MetricSeries:
    metric_name: str
    points: List[MetricPoint]


@dataclass
class MetricStats:
    metric_name: str
    start_time: str
    end_time: str
    statistics: Dict[str, float]


def normalize_dimensions(dimensions: Optional[Dict[str, Any]]) -> List[Dict[str, str]]:
    if not dimensions:
        return []
    return [
        {"Name": str(key), "Value": str(value)} for key, value in dimensions.items()
    ]


def normalize_cloudwatch_datapoints(
    datapoints: List[Dict[str, Any]],
) -> List[MetricPoint]:
    points: List[MetricPoint] = []
    for datapoint in sorted(datapoints, key=lambda item: item.get("Timestamp")):
        value = datapoint.get("Value")
        if value is None:
            for key in ("Average", "Sum", "Minimum", "Maximum", "SampleCount"):
                if key in datapoint:
                    value = datapoint.get(key)
                    break
        dimensions = datapoint.get("Dimensions") or []
        dims = {
            str(item.get("Name")): str(item.get("Value"))
            for item in dimensions
            if item.get("Name") is not None
        }
        points.append(
            MetricPoint(
                timestamp=datapoint.get("Timestamp").isoformat()
                if datapoint.get("Timestamp")
                else None,
                value=_to_float(value),
                dimensions=dims,
            )
        )
    return points
