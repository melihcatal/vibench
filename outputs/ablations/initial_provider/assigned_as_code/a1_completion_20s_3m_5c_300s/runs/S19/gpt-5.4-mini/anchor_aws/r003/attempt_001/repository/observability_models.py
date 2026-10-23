from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_dimensions(dimensions: Any) -> Dict[str, str]:
    if not dimensions:
        return {}
    if isinstance(dimensions, dict):
        return {str(k): str(v) for k, v in dimensions.items() if v is not None}
    normalized = {}
    for item in dimensions:
        if isinstance(item, dict) and "Name" in item and "Value" in item:
            normalized[str(item["Name"])] = str(item["Value"])
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            normalized[str(item[0])] = str(item[1])
    return normalized


def cloudwatch_dimensions(dimensions: Any) -> List[Dict[str, str]]:
    return [{"Name": k, "Value": v} for k, v in normalize_dimensions(dimensions).items()]


def datapoints_to_series(datapoints: Any) -> List[Dict[str, float]]:
    series = []
    for point in datapoints or []:
        timestamp = point.get("Timestamp")
        if hasattr(timestamp, "timestamp"):
            timestamp = timestamp.timestamp()
        value = _to_float(point.get("Average", point.get("Sum", point.get("Value"))))
        if timestamp is None or value is None:
            continue
        series.append({"timestamp": float(timestamp), "value": value})
    return sorted(series, key=lambda item: item["timestamp"])


@dataclass
class MetricQuery:
    metric: str
    start_time: float
    end_time: float
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeriesResponse:
    points: List[Dict[str, float]]
    metric: Optional[str] = None
    namespace: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)
