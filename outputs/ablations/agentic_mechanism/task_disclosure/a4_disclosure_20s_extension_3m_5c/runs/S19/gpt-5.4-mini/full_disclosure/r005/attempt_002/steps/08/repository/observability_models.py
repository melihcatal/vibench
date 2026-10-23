from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


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


def _normalize_dimensions(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return {str(k): str(v) for k, v in value.items() if v is not None}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        out: dict[str, str] = {}
        for item in value:
            if isinstance(item, Mapping):
                key = item.get("key", item.get("name"))
                if key is None:
                    continue
                out[str(key)] = str(item.get("value", item.get("val", "")))
            elif isinstance(item, Sequence) and len(item) == 2:
                out[str(item[0])] = str(item[1])
        return out
    raise TypeError(f"Unsupported dimensions value: {type(value)!r}")


def _normalize_tags(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Sequence):
        return [str(v) for v in value if v is not None]
    raise TypeError(f"Unsupported tags value: {type(value)!r}")


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    resource: str | None = None
    dimensions: dict[str, str] = field(default_factory=dict)
    locale: str | None = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricWindowRequest":
        return cls(
            metric_name=str(payload["metric_name"]),
            start_time=_to_utc_datetime(payload["start_time"]),
            end_time=_to_utc_datetime(payload["end_time"]),
            resource=str(payload["resource"]) if payload.get("resource") is not None else None,
            dimensions=_normalize_dimensions(payload.get("dimensions")),
            locale=str(payload["locale"]) if payload.get("locale") is not None else None,
        )

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "metric_name": self.metric_name,
            "start_time": self.start_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "end_time": self.end_time.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        }
        if self.resource is not None:
            payload["resource"] = self.resource
        if self.dimensions:
            payload["dimensions"] = dict(self.dimensions)
        if self.locale is not None:
            payload["locale"] = self.locale
        return payload


@dataclass(frozen=True)
class MetricPoint:
    timestamp: datetime
    value: float
    dimensions: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricPoint":
        return cls(
            timestamp=_to_utc_datetime(payload["timestamp"]),
            value=float(payload["value"]),
            dimensions=_normalize_dimensions(payload.get("dimensions")),
        )

    def to_payload(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "value": self.value,
            "dimensions": dict(self.dimensions),
        }


@dataclass(frozen=True)
class MetricTrendSummary:
    metric_name: str
    window_start: datetime
    window_end: datetime
    sample_count: int
    min_value: float | None = None
    max_value: float | None = None
    mean_value: float | None = None
    latest_value: float | None = None
    delta: float | None = None
    anomaly_score: float | None = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricTrendSummary":
        return cls(
            metric_name=str(payload["metric_name"]),
            window_start=_to_utc_datetime(payload["window_start"]),
            window_end=_to_utc_datetime(payload["window_end"]),
            sample_count=int(payload.get("sample_count", 0)),
            min_value=float(payload["min_value"]) if payload.get("min_value") is not None else None,
            max_value=float(payload["max_value"]) if payload.get("max_value") is not None else None,
            mean_value=float(payload["mean_value"]) if payload.get("mean_value") is not None else None,
            latest_value=float(payload["latest_value"]) if payload.get("latest_value") is not None else None,
            delta=float(payload["delta"]) if payload.get("delta") is not None else None,
            anomaly_score=float(payload["anomaly_score"]) if payload.get("anomaly_score") is not None else None,
        )

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "metric_name": self.metric_name,
            "window_start": self.window_start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "window_end": self.window_end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "sample_count": self.sample_count,
        }
        for key, value in (
            ("min_value", self.min_value),
            ("max_value", self.max_value),
            ("mean_value", self.mean_value),
            ("latest_value", self.latest_value),
            ("delta", self.delta),
            ("anomaly_score", self.anomaly_score),
        ):
            if value is not None:
                payload[key] = value
        return payload


@dataclass(frozen=True)
class MetricSeriesComparison:
    metric_name: str
    left_label: str
    right_label: str
    window_start: datetime
    window_end: datetime
    left_points: list[MetricPoint] = field(default_factory=list)
    right_points: list[MetricPoint] = field(default_factory=list)
    correlation: float | None = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricSeriesComparison":
        return cls(
            metric_name=str(payload["metric_name"]),
            left_label=str(payload["left_label"]),
            right_label=str(payload["right_label"]),
            window_start=_to_utc_datetime(payload["window_start"]),
            window_end=_to_utc_datetime(payload["window_end"]),
            left_points=[MetricPoint.from_payload(item) for item in payload.get("left_points", [])],
            right_points=[MetricPoint.from_payload(item) for item in payload.get("right_points", [])],
            correlation=float(payload["correlation"]) if payload.get("correlation") is not None else None,
        )


@dataclass(frozen=True)
class MetricAnnotationSafetyResult:
    text: str
    is_safe: bool
    risk_score: float
    reasons: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricAnnotationSafetyResult":
        return cls(
            text=str(payload["text"]),
            is_safe=bool(payload.get("is_safe", False)),
            risk_score=float(payload.get("risk_score", 0.0)),
            reasons=[str(v) for v in payload.get("reasons", [])],
            tags=_normalize_tags(payload.get("tags")),
        )

    def to_payload(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "is_safe": self.is_safe,
            "risk_score": self.risk_score,
            "reasons": list(self.reasons),
            "tags": list(self.tags),
        }


@dataclass(frozen=True)
class MetricArchiveRecord:
    snapshot_id: str
    object_url: str
    created_at: datetime
    content_type: str | None = None
    checksum: str | None = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricArchiveRecord":
        return cls(
            snapshot_id=str(payload["snapshot_id"]),
            object_url=str(payload["object_url"]),
            created_at=_to_utc_datetime(payload["created_at"]),
            content_type=str(payload["content_type"]) if payload.get("content_type") is not None else None,
            checksum=str(payload["checksum"]) if payload.get("checksum") is not None else None,
        )


def normalize_metric_points(payload: Sequence[Mapping[str, Any]] | Sequence[Any]) -> list[MetricPoint]:
    return [MetricPoint.from_payload(item) for item in payload]


def normalize_metric_summary(payload: Mapping[str, Any]) -> MetricTrendSummary:
    return MetricTrendSummary.from_payload(payload)


def normalize_metric_annotation_safety(payload: Mapping[str, Any]) -> MetricAnnotationSafetyResult:
    return MetricAnnotationSafetyResult.from_payload(payload)
