from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence


def _coerce_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = datetime.fromisoformat(text)
        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)
    raise TypeError(f"Unsupported datetime value: {type(value)!r}")


def _coerce_float(value: Any) -> Optional[float]:
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
    raise TypeError(f"Unsupported numeric value: {type(value)!r}")


def _coerce_str_dict(value: Any) -> Dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise TypeError(f"Expected mapping for labels/dimensions, got {type(value)!r}")
    return {str(k): str(v) for k, v in value.items()}


def _normalize_series_points(points: Any) -> List["MetricPoint"]:
    if points is None:
        return []
    if not isinstance(points, Sequence) or isinstance(points, (str, bytes, bytearray)):
        raise TypeError("points must be a sequence")
    return [MetricPoint.normalize(p) for p in points]


@dataclass(frozen=True)
class MetricTimeWindow:
    start: datetime
    end: datetime

    @classmethod
    def normalize(cls, value: Any) -> "MetricTimeWindow":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise TypeError("time window must be a mapping")
        start = _coerce_datetime(value.get("start"))
        end = _coerce_datetime(value.get("end"))
        if start is None or end is None:
            raise ValueError("time window requires start and end")
        return cls(start=start, end=end)


@dataclass(frozen=True)
class MetricPoint:
    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def normalize(cls, value: Any) -> "MetricPoint":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise TypeError("metric point must be a mapping")
        timestamp = _coerce_datetime(value.get("timestamp"))
        metric_value = _coerce_float(value.get("value"))
        if timestamp is None or metric_value is None:
            raise ValueError("metric point requires timestamp and value")
        return cls(timestamp=timestamp, value=metric_value, labels=_coerce_str_dict(value.get("labels")))


@dataclass(frozen=True)
class MetricQueryRequest:
    metric_name: str
    window: MetricTimeWindow
    resource: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)
    aggregation: Optional[str] = None
    limit: Optional[int] = None

    @classmethod
    def normalize(cls, value: Any) -> "MetricQueryRequest":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise TypeError("request must be a mapping")
        metric_name = str(value.get("metric_name") or value.get("metric") or "").strip()
        if not metric_name:
            raise ValueError("metric_name is required")
        window = MetricTimeWindow.normalize(value.get("window") or value)
        limit = value.get("limit")
        limit_value = int(limit) if limit is not None else None
        return cls(
            metric_name=metric_name,
            window=window,
            resource=(str(value["resource"]) if value.get("resource") is not None else None),
            dimensions=_coerce_str_dict(value.get("dimensions")),
            aggregation=(str(value["aggregation"]) if value.get("aggregation") is not None else None),
            limit=limit_value,
        )


@dataclass(frozen=True)
class MetricSummary:
    metric_name: str
    window: MetricTimeWindow
    count: int
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    average: Optional[float] = None
    latest: Optional[float] = None
    anomalies: List[MetricPoint] = field(default_factory=list)
    labels: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def normalize(cls, value: Any) -> "MetricSummary":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise TypeError("summary must be a mapping")
        metric_name = str(value.get("metric_name") or value.get("metric") or "").strip()
        if not metric_name:
            raise ValueError("metric_name is required")
        window = MetricTimeWindow.normalize(value.get("window") or value)
        count = int(value.get("count") or 0)
        return cls(
            metric_name=metric_name,
            window=window,
            count=count,
            minimum=_coerce_float(value.get("minimum") or value.get("min")),
            maximum=_coerce_float(value.get("maximum") or value.get("max")),
            average=_coerce_float(value.get("average") or value.get("avg")),
            latest=_coerce_float(value.get("latest")),
            anomalies=_normalize_series_points(value.get("anomalies")),
            labels=_coerce_str_dict(value.get("labels")),
        )


@dataclass(frozen=True)
class MetricSeriesComparison:
    metric_name: str
    window: MetricTimeWindow
    left_series: List[MetricPoint]
    right_series: List[MetricPoint]
    delta: List[MetricPoint] = field(default_factory=list)
    ratio: List[MetricPoint] = field(default_factory=list)

    @classmethod
    def normalize(cls, value: Any) -> "MetricSeriesComparison":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise TypeError("comparison must be a mapping")
        metric_name = str(value.get("metric_name") or value.get("metric") or "").strip()
        if not metric_name:
            raise ValueError("metric_name is required")
        window = MetricTimeWindow.normalize(value.get("window") or value)
        return cls(
            metric_name=metric_name,
            window=window,
            left_series=_normalize_series_points(value.get("left_series") or value.get("left")),
            right_series=_normalize_series_points(value.get("right_series") or value.get("right")),
            delta=_normalize_series_points(value.get("delta")),
            ratio=_normalize_series_points(value.get("ratio")),
        )


@dataclass(frozen=True)
class MetricAnnotationSafetyResult:
    text: str
    safe: bool
    reasons: List[str] = field(default_factory=list)
    detected_language: Optional[str] = None

    @classmethod
    def normalize(cls, value: Any) -> "MetricAnnotationSafetyResult":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise TypeError("safety result must be a mapping")
        text = str(value.get("text") or "")
        return cls(
            text=text,
            safe=bool(value.get("safe", False)),
            reasons=[str(v) for v in (value.get("reasons") or [])],
            detected_language=(str(value["detected_language"]) if value.get("detected_language") is not None else None),
        )


@dataclass(frozen=True)
class DashboardNoteTranslation:
    source_text: str
    target_locale: str
    translated_text: str
    source_locale: Optional[str] = None

    @classmethod
    def normalize(cls, value: Any) -> "DashboardNoteTranslation":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise TypeError("translation must be a mapping")
        return cls(
            source_text=str(value.get("source_text") or value.get("text") or ""),
            target_locale=str(value.get("target_locale") or value.get("locale") or ""),
            translated_text=str(value.get("translated_text") or value.get("translation") or ""),
            source_locale=(str(value["source_locale"]) if value.get("source_locale") is not None else None),
        )


@dataclass(frozen=True)
class ArchivedMetricSnapshot:
    snapshot_id: str
    storage_uri: str
    created_at: Optional[datetime] = None
    labels: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def normalize(cls, value: Any) -> "ArchivedMetricSnapshot":
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise TypeError("archived snapshot must be a mapping")
        snapshot_id = str(value.get("snapshot_id") or value.get("id") or "").strip()
        storage_uri = str(value.get("storage_uri") or value.get("uri") or "").strip()
        if not snapshot_id or not storage_uri:
            raise ValueError("snapshot_id and storage_uri are required")
        return cls(
            snapshot_id=snapshot_id,
            storage_uri=storage_uri,
            created_at=_coerce_datetime(value.get("created_at")),
            labels=_coerce_str_dict(value.get("labels")),
        )


__all__ = [
    "ArchivedMetricSnapshot",
    "DashboardNoteTranslation",
    "MetricAnnotationSafetyResult",
    "MetricPoint",
    "MetricQueryRequest",
    "MetricSeriesComparison",
    "MetricSummary",
    "MetricTimeWindow",
]
