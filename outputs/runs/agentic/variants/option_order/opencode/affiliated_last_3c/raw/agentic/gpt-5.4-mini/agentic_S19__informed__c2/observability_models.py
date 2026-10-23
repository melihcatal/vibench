from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def normalize_dimensions(dimensions: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not dimensions:
        return {}
    return {str(k): str(v) for k, v in dimensions.items() if v is not None}


def normalize_timestamps(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for item in items:
        normalized.append({k: item.get(k) for k in item})
    return normalized


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: str
    end_time: str
    period: int = 60
    statistic: str = "Average"
    dimensions: Optional[Dict[str, Any]] = None


@dataclass
class MetricSeriesPoint:
    timestamp: Any
    value: Optional[float]
    unit: Optional[str] = None


@dataclass
class MetricSeriesResponse:
    metric_name: str
    points: List[MetricSeriesPoint]
    dimensions: Dict[str, str]


@dataclass
class MetricStatsResponse:
    metric_name: str
    statistic: str
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum: Optional[float]
    sample_count: Optional[int]


def make_point(
    timestamp: Any, value: Any, unit: Optional[str] = None
) -> MetricSeriesPoint:
    return MetricSeriesPoint(timestamp=timestamp, value=_to_float(value), unit=unit)


def make_stats(
    metric_name: str, statistic: str, payload: Dict[str, Any]
) -> MetricStatsResponse:
    return MetricStatsResponse(
        metric_name=metric_name,
        statistic=statistic,
        minimum=_to_float(payload.get("minimum")),
        maximum=_to_float(payload.get("maximum")),
        average=_to_float(payload.get("average")),
        sum=_to_float(payload.get("sum")),
        sample_count=_to_int(payload.get("sample_count")),
    )
