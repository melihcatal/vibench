from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional, Sequence


def _to_utc_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value, tz=timezone.utc)
    elif isinstance(value, str):
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
    else:
        raise TypeError(f"Unsupported datetime value: {type(value)!r}")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _normalize_labels(labels: Any) -> dict[str, str]:
    if labels is None:
        return {}
    if isinstance(labels, Mapping):
        return {str(k): str(v) for k, v in labels.items() if v is not None}
    if isinstance(labels, Sequence) and not isinstance(labels, (str, bytes, bytearray)):
        normalized: dict[str, str] = {}
        for item in labels:
            if isinstance(item, Mapping) and "key" in item and "value" in item:
                normalized[str(item["key"])] = str(item["value"])
        return normalized
    raise TypeError(f"Unsupported labels value: {type(labels)!r}")


def _normalize_points(points: Any) -> list[dict[str, Any]]:
    if points is None:
        return []
    normalized: list[dict[str, Any]] = []
    for point in points:
        if isinstance(point, Mapping):
            timestamp = point.get("timestamp") if "timestamp" in point else point.get("time")
            normalized.append(
                {
                    "timestamp": _to_utc_datetime(timestamp) if timestamp is not None else None,
                    "value": point.get("value"),
                }
            )
        elif isinstance(point, Sequence) and len(point) >= 2:
            normalized.append({"timestamp": _to_utc_datetime(point[0]), "value": point[1]})
        else:
            raise TypeError(f"Unsupported point value: {type(point)!r}")
    return normalized


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    resource: Optional[str] = None
    labels: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "start_time", _to_utc_datetime(self.start_time))
        object.__setattr__(self, "end_time", _to_utc_datetime(self.end_time))
        object.__setattr__(self, "labels", _normalize_labels(self.labels))


@dataclass(frozen=True)
class MetricSeriesRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    resource_a: Optional[str] = None
    resource_b: Optional[str] = None
    filter_a: dict[str, str] = field(default_factory=dict)
    filter_b: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "start_time", _to_utc_datetime(self.start_time))
        object.__setattr__(self, "end_time", _to_utc_datetime(self.end_time))
        object.__setattr__(self, "filter_a", _normalize_labels(self.filter_a))
        object.__setattr__(self, "filter_b", _normalize_labels(self.filter_b))


@dataclass(frozen=True)
class MetricQueryResult:
    metric_name: str
    start_time: datetime
    end_time: datetime
    points: list[dict[str, Any]] = field(default_factory=list)
    labels: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "start_time", _to_utc_datetime(self.start_time))
        object.__setattr__(self, "end_time", _to_utc_datetime(self.end_time))
        object.__setattr__(self, "labels", _normalize_labels(self.labels))
        object.__setattr__(self, "points", _normalize_points(self.points))


@dataclass(frozen=True)
class MetricTrendSummary:
    metric_name: str
    window_start: datetime
    window_end: datetime
    sample_count: int
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    average: Optional[float] = None
    latest_value: Optional[float] = None
    anomaly_count: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "window_start", _to_utc_datetime(self.window_start))
        object.__setattr__(self, "window_end", _to_utc_datetime(self.window_end))


@dataclass(frozen=True)
class AnnotationSafetyCheckRequest:
    text: str
    locale: Optional[str] = None
    context: Optional[str] = None


@dataclass(frozen=True)
class AnnotationSafetyCheckResult:
    safe: bool
    reasons: list[str] = field(default_factory=list)
    normalized_text: Optional[str] = None


@dataclass(frozen=True)
class DashboardNoteTranslationRequest:
    text: str
    target_locale: str
    source_locale: Optional[str] = None


@dataclass(frozen=True)
class DashboardNoteTranslationResult:
    translated_text: str
    source_locale: Optional[str] = None
    target_locale: Optional[str] = None


@dataclass(frozen=True)
class MetricArchiveRecord:
    snapshot_id: str
    metric_name: str
    archived_at: datetime
    object_uri: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "archived_at", _to_utc_datetime(self.archived_at))


def normalize_metric_window_payload(payload: Mapping[str, Any]) -> MetricQueryResult:
    return MetricQueryResult(
        metric_name=str(payload.get("metric_name") or payload.get("metric") or ""),
        start_time=payload.get("start_time") or payload.get("window_start"),
        end_time=payload.get("end_time") or payload.get("window_end"),
        points=payload.get("points") or payload.get("datapoints") or [],
        labels=payload.get("labels") or payload.get("dimensions") or {},
    )


def normalize_metric_series_payload(payload: Mapping[str, Any]) -> dict[str, MetricQueryResult]:
    series_a = payload.get("series_a") or payload.get("resource_a") or {}
    series_b = payload.get("series_b") or payload.get("resource_b") or {}
    return {
        "a": normalize_metric_window_payload(series_a),
        "b": normalize_metric_window_payload(series_b),
    }
