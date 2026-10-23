from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union
from urllib.parse import urlencode


def _isoformat_utc(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _coerce_datetime(value: Union[str, datetime, None]) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = value.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    parsed = datetime.fromisoformat(text)
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _to_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _normalize_mapping(value: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not value:
        return {}
    return {str(k): "" if v is None else str(v) for k, v in value.items()}


def _normalize_list(value: Optional[Iterable[Any]]) -> List[str]:
    if not value:
        return []
    return ["" if v is None else str(v) for v in value]


@dataclass(frozen=True)
class MetricQueryWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    resource: Optional[str] = None
    dimensions: Mapping[str, Any] = field(default_factory=dict)
    limit: Optional[int] = None

    def to_query_params(self) -> Dict[str, str]:
        params: Dict[str, str] = {
            "metric_name": self.metric_name,
            "start_time": _isoformat_utc(self.start_time),
            "end_time": _isoformat_utc(self.end_time),
        }
        if self.resource:
            params["resource"] = self.resource
        for key, value in _normalize_mapping(self.dimensions).items():
            params[f"dimension.{key}"] = value
        if self.limit is not None:
            params["limit"] = str(self.limit)
        return params


@dataclass(frozen=True)
class MetricDatum:
    timestamp: datetime
    value: float
    dimensions: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricDatum":
        return cls(
            timestamp=_coerce_datetime(payload.get("timestamp")) or datetime.now(timezone.utc),
            value=float(payload.get("value", 0.0)),
            dimensions=_normalize_mapping(payload.get("dimensions")),
        )


@dataclass(frozen=True)
class MetricWindowResponse:
    metric_name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    datapoints: Tuple[MetricDatum, ...] = ()
    unit: Optional[str] = None
    resource: Optional[str] = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricWindowResponse":
        datapoints = tuple(
            MetricDatum.from_payload(item)
            for item in payload.get("datapoints", [])
            if isinstance(item, Mapping)
        )
        return cls(
            metric_name=str(payload.get("metric_name", "")),
            start_time=_coerce_datetime(payload.get("start_time")),
            end_time=_coerce_datetime(payload.get("end_time")),
            datapoints=datapoints,
            unit=payload.get("unit"),
            resource=payload.get("resource"),
        )


@dataclass(frozen=True)
class MetricComparisonRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    left_resource: Optional[str] = None
    right_resource: Optional[str] = None
    left_dimensions: Mapping[str, Any] = field(default_factory=dict)
    right_dimensions: Mapping[str, Any] = field(default_factory=dict)

    def to_query_params(self) -> Dict[str, str]:
        params: Dict[str, str] = {
            "metric_name": self.metric_name,
            "start_time": _isoformat_utc(self.start_time),
            "end_time": _isoformat_utc(self.end_time),
        }
        if self.left_resource:
            params["left_resource"] = self.left_resource
        if self.right_resource:
            params["right_resource"] = self.right_resource
        for key, value in _normalize_mapping(self.left_dimensions).items():
            params[f"left_dimension.{key}"] = value
        for key, value in _normalize_mapping(self.right_dimensions).items():
            params[f"right_dimension.{key}"] = value
        return params


@dataclass(frozen=True)
class MetricComparisonPoint:
    timestamp: datetime
    left_value: Optional[float] = None
    right_value: Optional[float] = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricComparisonPoint":
        return cls(
            timestamp=_coerce_datetime(payload.get("timestamp")) or datetime.now(timezone.utc),
            left_value=_to_float(payload.get("left_value")),
            right_value=_to_float(payload.get("right_value")),
        )


@dataclass(frozen=True)
class MetricComparisonResponse:
    metric_name: str
    points: Tuple[MetricComparisonPoint, ...] = ()

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricComparisonResponse":
        points = tuple(
            MetricComparisonPoint.from_payload(item)
            for item in payload.get("points", [])
            if isinstance(item, Mapping)
        )
        return cls(metric_name=str(payload.get("metric_name", "")), points=points)


@dataclass(frozen=True)
class MetricSummary:
    metric_name: str
    count: int = 0
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    average_value: Optional[float] = None
    latest_value: Optional[float] = None
    latest_timestamp: Optional[datetime] = None

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "MetricSummary":
        return cls(
            metric_name=str(payload.get("metric_name", "")),
            count=_to_int(payload.get("count")) or 0,
            min_value=_to_float(payload.get("min_value")),
            max_value=_to_float(payload.get("max_value")),
            average_value=_to_float(payload.get("average_value")),
            latest_value=_to_float(payload.get("latest_value")),
            latest_timestamp=_coerce_datetime(payload.get("latest_timestamp")),
        )


@dataclass(frozen=True)
class NormalizedMetricSeries:
    metric_name: str
    timestamps: Tuple[datetime, ...]
    values: Tuple[float, ...]
    dimensions: Tuple[Mapping[str, str], ...] = ()


def normalize_metric_series(payload: Mapping[str, Any]) -> NormalizedMetricSeries:
    metric_name = str(payload.get("metric_name", ""))
    raw_points = payload.get("datapoints") or payload.get("points") or []
    timestamps: List[datetime] = []
    values: List[float] = []
    dimensions: List[Mapping[str, str]] = []
    for item in raw_points:
        if not isinstance(item, Mapping):
            continue
        ts = _coerce_datetime(item.get("timestamp"))
        val = _to_float(item.get("value"))
        if ts is None or val is None:
            continue
        timestamps.append(ts)
        values.append(val)
        dimensions.append(_normalize_mapping(item.get("dimensions")))
    return NormalizedMetricSeries(
        metric_name=metric_name,
        timestamps=tuple(timestamps),
        values=tuple(values),
        dimensions=tuple(dimensions),
    )


def normalize_metric_summary(payload: Mapping[str, Any]) -> MetricSummary:
    return MetricSummary.from_payload(payload)


def build_query_string(params: Mapping[str, Any]) -> str:
    flat: Dict[str, str] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, datetime):
            flat[key] = _isoformat_utc(value)
        elif isinstance(value, Mapping):
            for sub_key, sub_value in _normalize_mapping(value).items():
                flat[f"{key}.{sub_key}"] = sub_value
        elif isinstance(value, (list, tuple, set)):
            flat[key] = ",".join(_normalize_list(value))
        else:
            flat[key] = str(value)
    return urlencode(flat)
