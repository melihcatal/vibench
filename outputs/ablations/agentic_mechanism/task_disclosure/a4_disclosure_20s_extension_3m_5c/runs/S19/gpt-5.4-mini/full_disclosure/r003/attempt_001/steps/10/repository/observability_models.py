from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        return float(text)
    raise TypeError(f"Cannot convert {type(value).__name__} to float")


def _to_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return int(value)
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        return int(float(text))
    raise TypeError(f"Cannot convert {type(value).__name__} to int")


def _to_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        text = text.replace("Z", "+00:00")
        dt = datetime.fromisoformat(text)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    raise TypeError(f"Cannot convert {type(value).__name__} to datetime")


def _normalize_tags(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return {str(k): str(v) for k, v in value.items()}
    raise TypeError("tags must be a mapping")


def _normalize_dimensions(value: Any) -> dict[str, str]:
    return _normalize_tags(value)


@dataclass(frozen=True)
class MetricWindow:
    metric_name: str
    start_time: datetime
    end_time: datetime
    granularity_seconds: Optional[int] = None
    dimensions: dict[str, str] = field(default_factory=dict)
    resource_id: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "start_time", _to_datetime(self.start_time))
        object.__setattr__(self, "end_time", _to_datetime(self.end_time))
        object.__setattr__(self, "granularity_seconds", _to_int(self.granularity_seconds))
        object.__setattr__(self, "dimensions", _normalize_dimensions(self.dimensions))


@dataclass(frozen=True)
class MetricQueryResult:
    metric_name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    points: list[dict[str, Any]] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "start_time", _to_datetime(self.start_time))
        object.__setattr__(self, "end_time", _to_datetime(self.end_time))


@dataclass(frozen=True)
class AggregatedMetricStats:
    metric_name: str
    window_start: Optional[datetime] = None
    window_end: Optional[datetime] = None
    count: int = 0
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    average: Optional[float] = None
    sum: Optional[float] = None
    p50: Optional[float] = None
    p90: Optional[float] = None
    p95: Optional[float] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "window_start", _to_datetime(self.window_start))
        object.__setattr__(self, "window_end", _to_datetime(self.window_end))
        object.__setattr__(self, "count", _to_int(self.count) or 0)
        object.__setattr__(self, "minimum", _to_float(self.minimum))
        object.__setattr__(self, "maximum", _to_float(self.maximum))
        object.__setattr__(self, "average", _to_float(self.average))
        object.__setattr__(self, "sum", _to_float(self.sum))
        object.__setattr__(self, "p50", _to_float(self.p50))
        object.__setattr__(self, "p90", _to_float(self.p90))
        object.__setattr__(self, "p95", _to_float(self.p95))


@dataclass(frozen=True)
class MetricTrendSummary:
    metric_name: str
    window_start: Optional[datetime] = None
    window_end: Optional[datetime] = None
    trend: Optional[str] = None
    anomaly_score: Optional[float] = None
    latest_value: Optional[float] = None
    baseline_value: Optional[float] = None
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "window_start", _to_datetime(self.window_start))
        object.__setattr__(self, "window_end", _to_datetime(self.window_end))
        object.__setattr__(self, "anomaly_score", _to_float(self.anomaly_score))
        object.__setattr__(self, "latest_value", _to_float(self.latest_value))
        object.__setattr__(self, "baseline_value", _to_float(self.baseline_value))


def normalize_metric_point(point: Mapping[str, Any]) -> dict[str, Any]:
    ts = point.get("timestamp") if isinstance(point, Mapping) else None
    value = point.get("value") if isinstance(point, Mapping) else None
    normalized = dict(point)
    if ts is not None:
        normalized["timestamp"] = _to_datetime(ts)
    if value is not None:
        normalized["value"] = _to_float(value)
    if "dimensions" in normalized:
        normalized["dimensions"] = _normalize_dimensions(normalized["dimensions"])
    return normalized


def normalize_metric_query_result(payload: Mapping[str, Any]) -> MetricQueryResult:
    points = payload.get("points") or []
    return MetricQueryResult(
        metric_name=str(payload.get("metric_name", "")),
        start_time=payload.get("start_time"),
        end_time=payload.get("end_time"),
        points=[normalize_metric_point(p) for p in points],
        summary=dict(payload.get("summary") or {}),
    )


def normalize_aggregated_metric_stats(payload: Mapping[str, Any]) -> AggregatedMetricStats:
    return AggregatedMetricStats(
        metric_name=str(payload.get("metric_name", "")),
        window_start=payload.get("window_start") or payload.get("start_time"),
        window_end=payload.get("window_end") or payload.get("end_time"),
        count=payload.get("count", 0),
        minimum=payload.get("minimum") or payload.get("min"),
        maximum=payload.get("maximum") or payload.get("max"),
        average=payload.get("average") or payload.get("mean"),
        sum=payload.get("sum"),
        p50=payload.get("p50") or payload.get("median"),
        p90=payload.get("p90"),
        p95=payload.get("p95"),
    )


def normalize_metric_trend_summary(payload: Mapping[str, Any]) -> MetricTrendSummary:
    return MetricTrendSummary(
        metric_name=str(payload.get("metric_name", "")),
        window_start=payload.get("window_start") or payload.get("start_time"),
        window_end=payload.get("window_end") or payload.get("end_time"),
        trend=payload.get("trend"),
        anomaly_score=payload.get("anomaly_score"),
        latest_value=payload.get("latest_value"),
        baseline_value=payload.get("baseline_value"),
        details=dict(payload.get("details") or {}),
    )
